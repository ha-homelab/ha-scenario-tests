#!/usr/bin/env python3
"""Rebuild original SVGs from the checked-in, synthetic scenario example."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/images"


def esc(value):
    return html.escape(str(value), quote=True)


def text(x, y, value, size=18, fill="#dfebf6", weight=400):
    return (
        f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}">{esc(value)}</text>'
    )


def box(x, y, w, h, title, lines, color="#163149"):
    result = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{color}" stroke="#47657c"/>',
        text(x + 20, y + 33, title, 20, weight=600),
    ]
    for i, line in enumerate(lines):
        result.append(text(x + 20, y + 65 + i * 26, line, 16))
    return "".join(result)


def svg(name, title, desc, elements, height):
    output = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1120" '
        f'height="{height}" viewBox="0 0 1120 {height}" role="img" '
        f'aria-labelledby="title desc"><title id="title">{esc(title)}</title>'
        f'<desc id="desc">{esc(desc)}</desc>'
        f'<rect width="1120" height="{height}" fill="#0b1725"/>' + "".join(elements) + "</svg>\n"
    )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(output, encoding="utf-8")


def architecture():
    elements = [
        text(40, 48, "Actual HA engine · synthetic inputs and actuators", 28, weight=600),
        text(
            40, 78, "Architecture illustration — no live Home Assistant connection", 17, "#97bed8"
        ),
        box(
            40,
            120,
            265,
            170,
            "Bounded JSON",
            [
                "Seed + state/event timeline",
                "Allowed HA automation subset",
                "Expected / forbidden calls",
            ],
        ),
        box(
            355,
            120,
            355,
            170,
            "Fresh Python worker",
            [
                "Home Assistant 2026.10.1",
                "Real triggers, timers and reload",
                "In-memory actuator callbacks",
            ],
        ),
        box(
            760,
            120,
            320,
            170,
            "Evidence",
            [
                "Ordered calls and final states",
                "Stable JSON report + pytest",
                "Physical validation: false",
            ],
        ),
        box(
            355,
            335,
            355,
            145,
            "Temporary configuration",
            ["No existing config directory", "No custom integrations or tokens"],
        ),
        box(
            40,
            525,
            1040,
            145,
            "Execution boundary",
            [
                "Python audit guard: block network / DNS / subprocess attempts; fail the scenario.",
                "Trusted native dependencies: this is not an OS security sandbox.",
                "Optional Docker --network none provides a separate OS network boundary.",
            ],
            "#20322f",
        ),
    ]
    for x1, x2 in [(305, 355), (710, 760)]:
        elements.append(
            f'<path d="M{x1} 200 H{x2 - 8} l-10 -6 m10 6 l-10 6" '
            'fill="none" stroke="#63d6ba" stroke-width="3"/>'
        )
    elements.append(
        '<path d="M532 335 V300 l-6 10 m6 -10 l6 10" fill="none" '
        'stroke="#63d6ba" stroke-width="3"/>'
    )
    svg(
        "isolation.svg",
        "Synthetic HA scenario isolation architecture",
        "A bounded scenario enters a fresh guarded Python worker running actual Home Assistant. "
        "Synthetic callbacks record ordered calls and states. A temporary config is used. "
        "The audit guard is not an OS sandbox.",
        elements,
        710,
    )


def timeline():
    document = json.loads((ROOT / "examples/presence_timeout.json").read_text())
    current = 0
    times = []
    for step in document["timeline"]:
        current += step["after"]
        times.append(current)
    end = current + document["settle_seconds"]
    timer = document["automations"][1]["triggers"][0]["for_seconds"]
    on, absent = times
    off = absent + timer

    def x(seconds):
        return round(210 + 830 * seconds / end, 2)

    elements = [
        text(40, 48, "Presence → absence hold → light off", 28, weight=600),
        text(
            40, 78, "Synthetic expected timeline from examples/presence_timeout.json", 17, "#97bed8"
        ),
        text(
            40,
            111,
            "Illustration, not measured runtime or proof of a production timer",
            16,
            "#ffcc85",
        ),
    ]
    for at in [0, on, absent, off, end]:
        xx = x(at)
        elements.append(f'<path d="M{xx} 165 V370" stroke="#33475b" stroke-dasharray="5 5"/>')
        elements.append(text(xx - 18, 405, f"{at:.2f}s", 15))
    for label, yy, finish in [("Presence", 200, absent), ("Light", 280, off)]:
        elements.append(text(40, yy + 7, label, 22, weight=600))
        elements.append(
            f'<path d="M210 {yy + 20} H{x(on)} V{yy - 20} H{x(finish)} '
            f'V{yy + 20} H1040" fill="none" stroke="#63d6ba" stroke-width="5"/>'
        )
    elements += [
        text(x(on) + 7, 163, "on", 16, "#63d6ba"),
        text(x(absent) + 7, 163, "off", 16, "#63d6ba"),
        text(x(off) + 7, 255, "turn_off", 16, "#63d6ba"),
        f'<path d="M{x(absent)} 335 H{x(off)}" stroke="#ffcc85" stroke-width="5"/>',
        text(x(absent) + 10, 365, f"HA for: {timer:.2f}s", 17, "#ffcc85"),
        box(
            40,
            445,
            1040,
            145,
            "Assertions",
            [
                "Exact ordered service calls: light.turn_on, then light.turn_off.",
                "Final synthetic light state: off. Actual execution reports elapsed timestamps.",
                "Real elapsed clock. Reload, manual override and stale input have own scenarios.",
            ],
            "#20322f",
        ),
    ]
    svg(
        "timeline.svg",
        "Synthetic expected presence timeout timeline",
        f"Presence starts at {on} seconds and ends at {absent} seconds. "
        f"The expected lamp off action is after a {timer} second HA timer. "
        "This is synthetic expected behavior, not measured runtime.",
        elements,
        625,
    )


if __name__ == "__main__":
    architecture()
    timeline()
