"""A deliberately small input language, not an arbitrary HA config loader."""

import json
import math
import os
import re
import stat
from pathlib import Path

SCHEMA = "ha-scenario/v1"
MAX_BYTES = 65536
DOMAINS = {"light", "switch", "input_boolean"}
ACTIONS = {f"{d}.{a}" for d in DOMAINS for a in ("turn_on", "turn_off", "toggle")}
ENTITY = re.compile(r"(?:light|switch|input_boolean|binary_sensor)\.scenario_[a-z0-9_]{1,48}\Z")
IDENTIFIER = re.compile(r"[a-z][a-z0-9_]{0,47}\Z")
EVENT = re.compile(r"scenario_[a-z0-9_]{1,48}\Z")


class InvalidScenario(ValueError):
    """Input is outside the supported, bounded scenario language."""


def fail(path):
    # Do not echo possibly private input values in errors.
    raise InvalidScenario(f"invalid field: {path}")


def obj(value, required, optional, path):
    if not isinstance(value, dict) or set(value) - required - optional or required - set(value):
        fail(path)


def seq(value, limit, path, minimum=0):
    if not isinstance(value, list) or not minimum <= len(value) <= limit:
        fail(path)


def duration(value, path):
    if type(value) not in (float, int) or not 0 <= value <= 5 or not math.isfinite(value):
        fail(path)


def state(value, path):
    if not isinstance(value, str) or value not in {"on", "off", "unknown", "unavailable"}:
        fail(path)


def entity(value, entities, path):
    if not isinstance(value, str) or value not in entities:
        fail(path)


def action(value, entities, path):
    obj(value, {"action", "entity_id"}, set(), path)
    if not isinstance(value["action"], str) or value["action"] not in ACTIONS:
        fail(path + ".action")
    entity(value["entity_id"], entities, path + ".entity_id")
    if value["entity_id"].split(".")[0] != value["action"].split(".")[0]:
        fail(path + ".entity_id")


def validate(document):
    obj(
        document,
        {"schema", "name", "seed", "automations", "timeline", "expect"},
        {"settle_seconds"},
        "root",
    )
    if document["schema"] != SCHEMA:
        fail("schema")
    if not isinstance(document["name"], str) or not IDENTIFIER.fullmatch(document["name"]):
        fail("name")
    seed = document["seed"]
    if not isinstance(seed, dict) or not 1 <= len(seed) <= 64:
        fail("seed")
    for key, value in seed.items():
        if not isinstance(key, str) or not ENTITY.fullmatch(key):
            fail("seed.entity")
        state(value, "seed.state")
    entities = set(seed)
    seq(document["automations"], 16, "automations", 1)
    ids = set()
    for spec in document["automations"]:
        obj(spec, {"id", "triggers", "actions"}, {"conditions", "mode"}, "automation")
        if not isinstance(spec["id"], str) or not IDENTIFIER.fullmatch(spec["id"]):
            fail("automation.id")
        if spec["id"] in ids:
            fail("automation.id.duplicate")
        ids.add(spec["id"])
        if not isinstance(spec.get("mode", "single"), str) or spec.get("mode", "single") not in {
            "single",
            "restart",
        }:
            fail("automation.mode")
        seq(spec["triggers"], 8, "triggers", 1)
        for trigger in spec["triggers"]:
            if not isinstance(trigger, dict):
                fail("trigger")
            if trigger.get("trigger") == "state":
                obj(trigger, {"trigger", "entity_id", "to"}, {"from", "for_seconds"}, "trigger")
                entity(trigger["entity_id"], entities, "trigger.entity_id")
                state(trigger["to"], "trigger.to")
                if "from" in trigger:
                    state(trigger["from"], "trigger.from")
                duration(trigger.get("for_seconds", 0), "trigger.for_seconds")
            elif trigger.get("trigger") == "event":
                obj(trigger, {"trigger", "event_type"}, set(), "trigger")
                ev = trigger["event_type"]
                if not isinstance(ev, str) or not (
                    EVENT.fullmatch(ev) or ev == "automation_reloaded"
                ):
                    fail("trigger.event_type")
            else:
                fail("trigger.trigger")
        seq(spec.get("conditions", []), 8, "conditions")
        for condition in spec.get("conditions", []):
            obj(condition, {"condition", "entity_id", "state"}, set(), "condition")
            if condition["condition"] != "state":
                fail("condition.condition")
            entity(condition["entity_id"], entities, "condition.entity_id")
            state(condition["state"], "condition.state")
        seq(spec["actions"], 16, "actions", 1)
        for item in spec["actions"]:
            action(item, entities, "action")
    seq(document["timeline"], 32, "timeline")
    total = document.get("settle_seconds", 0.1)
    duration(total, "settle_seconds")
    for step in document["timeline"]:
        obj(step, {"after"}, {"set", "event", "reload"}, "timeline.step")
        if len(set(step) & {"set", "event", "reload"}) != 1:
            fail("timeline.step.operation")
        duration(step["after"], "timeline.after")
        total += step["after"]
        if "set" in step:
            obj(step["set"], {"entity_id", "state"}, set(), "timeline.set")
            entity(step["set"]["entity_id"], entities, "timeline.set.entity_id")
            state(step["set"]["state"], "timeline.set.state")
        if "event" in step:
            if not isinstance(step["event"], str) or not EVENT.fullmatch(step["event"]):
                fail("timeline.event")
        if "reload" in step and step["reload"] is not True:
            fail("timeline.reload")
    if total > 5:
        fail("timeline.total_duration")
    expect = document["expect"]
    obj(expect, {"calls"}, {"forbidden", "states"}, "expect")
    for field in ["calls", "forbidden"]:
        seq(expect.get(field, []), 256, "expect." + field)
        for item in expect.get(field, []):
            action(item, entities, "expect." + field)
    states = expect.get("states", {})
    if not isinstance(states, dict):
        fail("expect.states")
    for key, value in states.items():
        entity(key, entities, "expect.states.entity_id")
        state(value, "expect.states.state")
    return document


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail("duplicate_json_key")
        result[key] = value
    return result


def load(path):
    path = Path(path)
    try:
        # Open once, reject the final symlink atomically, and never wait on a FIFO.
        # fstat checks the opened object rather than an earlier path lookup.
        if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_NONBLOCK"):
            fail("file_platform")
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                fail("file")
            data = b""
            while len(data) <= MAX_BYTES:
                chunk = os.read(fd, MAX_BYTES + 1 - len(data))
                if not chunk:
                    break
                data += chunk
        finally:
            os.close(fd)
        if len(data) > MAX_BYTES:
            fail("file")
        return validate(json.loads(data, object_pairs_hook=unique_pairs))
    except (OSError, ValueError, RecursionError) as exc:
        raise InvalidScenario("invalid scenario file") from exc


def ha_config(document):
    """Translate the admitted subset without evaluating templates or Python."""
    result = []
    for source in document["automations"]:
        spec = {"id": source["id"], "alias": source["id"], "mode": source.get("mode", "single")}
        spec["triggers"] = []
        for source_trigger in source["triggers"]:
            trigger = dict(source_trigger)
            seconds = trigger.pop("for_seconds", None)
            if seconds is not None:
                trigger["for"] = {"seconds": seconds}
            spec["triggers"].append(trigger)
        spec["conditions"] = source.get("conditions", [])
        spec["actions"] = [
            {"action": item["action"], "target": {"entity_id": item["entity_id"]}}
            for item in source["actions"]
        ]
        result.append(spec)
    return {"automation": result}
