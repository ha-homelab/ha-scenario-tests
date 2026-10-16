"""Private child entry point. Uses HA's actual triggers, conditions and Script."""

import asyncio
import contextlib
import importlib.metadata
import io
import json
import logging
import platform
import socket
import sys
import tempfile
import time
from pathlib import Path

from .isolation import install_guard
from .schema import ACTIONS, MAX_BYTES, ha_config, unique_pairs, validate

HA_VERSION = "2026.10.0"


async def execute(document, violations):
    from homeassistant import loader
    from homeassistant.bootstrap import async_load_base_functionality
    from homeassistant.config_entries import ConfigEntries
    from homeassistant.core import HomeAssistant
    from homeassistant.setup import async_setup_component

    if importlib.metadata.version("homeassistant") != HA_VERSION:
        raise RuntimeError("unsupported Home Assistant version")
    calls, errors = [], []

    class ErrorCollector(logging.Handler):
        def emit(self, record):
            # Error details may include environment data; the public report uses a code.
            errors.append("ha_logged_error")

    error_handler = ErrorCollector(level=logging.ERROR)
    logging.getLogger().addHandler(error_handler)
    loop = asyncio.get_running_loop()
    loop.set_exception_handler(lambda loop, context: errors.append("background_exception"))
    with tempfile.TemporaryDirectory(prefix="ha-scenario-") as directory:
        hass = HomeAssistant(directory)
        loader.async_setup(hass)
        hass.config_entries = ConfigEntries(hass, {})
        hass.config.skip_pip = True
        hass.config.time_zone = "UTC"
        config = ha_config(document)
        # JSON is valid YAML; no user-supplied filesystem paths or YAML tags.
        Path(directory, "configuration.yaml").write_text(json.dumps(config), encoding="utf-8")
        start = time.monotonic()

        async def command(call):
            targets = call.data.get("entity_id", [])
            targets = [targets] if isinstance(targets, str) else targets
            if len(targets) != 1 or targets[0] not in document["seed"] or len(calls) >= 256:
                errors.append("sink_contract")
                raise RuntimeError("invalid synthetic sink call")
            target = targets[0]
            calls.append(
                {
                    "action": f"{call.domain}.{call.service}",
                    "entity_id": target,
                    "elapsed_seconds": round(time.monotonic() - start, 6),
                }
            )
            previous = hass.states.get(target)
            state = "on" if call.service == "turn_on" else "off"
            if call.service == "toggle":
                state = "off" if previous and previous.state == "on" else "on"
            # This is a synthetic actuator ACK, never evidence of physical behavior.
            hass.states.async_set(target, state, context=call.context)

        try:
            if not await async_load_base_functionality(hass):
                raise RuntimeError("base setup failed")
            for full in sorted(ACTIONS):
                domain, service = full.split(".")
                hass.services.async_register(domain, service, command)
            for entity_id, state in document["seed"].items():
                hass.states.async_set(entity_id, state)
            if not await async_setup_component(hass, "automation", config):
                raise RuntimeError("automation setup failed")
            await hass.async_start()
            await hass.async_block_till_done()
            if len(hass.states.async_entity_ids("automation")) != len(document["automations"]):
                raise RuntimeError("not all automations loaded")
            start = time.monotonic()
            timeline = []
            for step in document["timeline"]:
                await asyncio.sleep(step["after"])
                if "set" in step:
                    item = step["set"]
                    hass.states.async_set(item["entity_id"], item["state"])
                    kind = "set"
                elif "event" in step:
                    hass.bus.async_fire(step["event"])
                    kind = "event"
                else:
                    await hass.services.async_call("automation", "reload", blocking=True)
                    kind = "reload"
                await hass.async_block_till_done()
                timeline.append(
                    {"operation": kind, "elapsed_seconds": round(time.monotonic() - start, 6)}
                )
            await asyncio.sleep(document.get("settle_seconds", 0.1))
            await hass.async_block_till_done()
            actual = [{k: call[k] for k in ("action", "entity_id")} for call in calls]
            failures = []
            if actual != document["expect"]["calls"]:
                failures.append("calls_mismatch")
            if any(call in document["expect"].get("forbidden", []) for call in actual):
                failures.append("forbidden_call")
            states = {key: hass.states.get(key).state for key in document["seed"]}
            if any(
                states[key] != expected
                for key, expected in document["expect"].get("states", {}).items()
            ):
                failures.append("states_mismatch")
            components = sorted(hass.config.components)
        finally:
            await hass.async_stop(force=True)
        if violations:
            failures.append("blocked_io")
        if errors:
            failures.extend(sorted(set(errors)))
        return {
            "schema": "ha-scenario-report/v1",
            "name": document["name"],
            "passed": not failures,
            "failures": failures,
            "ha_version": HA_VERSION,
            "clock": "elapsed_monotonic",
            "physical_validation": False,
            "isolation": "fresh_worker_temp_config_python_audit_guard",
            "calls": calls,
            "states": states,
            "timeline": timeline,
            "blocked_io": violations,
            "components": components,
        }


def main():
    payload = sys.stdin.read(MAX_BYTES + 1)
    if len(payload.encode("utf-8")) > MAX_BYTES:
        raise ValueError("input too large")
    document = validate(json.loads(payload, object_pairs_hook=unique_pairs))
    logging.getLogger().setLevel(logging.ERROR)
    # HA primes this cached property using `uname -p` on some platforms. Provide
    # synthetic CPU metadata so no subprocess exception is needed in the guard.
    # This affects environment metadata only, not HA automation semantics.
    platform.uname().__dict__["processor"] = "synthetic"
    # urllib3 probes IPv6 support by binding a localhost socket during import.
    # IPv6 is intentionally unavailable in this network-free worker.
    socket.has_ipv6 = False
    # Build the event loop before installing the socket guard (self-pipe).
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    violations = install_guard()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            report = loop.run_until_complete(asyncio.wait_for(execute(document, violations), 20))
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.run_until_complete(loop.shutdown_default_executor())
        finally:
            loop.close()
            asyncio.set_event_loop(None)
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
