"""CLI: translated human output and stable language-independent JSON reports."""

import argparse
import json
import sys
from functools import partial

from .i18n import MESSAGES
from .runner import run_scenario
from .schema import InvalidScenario, load


class Parser(argparse.ArgumentParser):
    def __init__(self, *args, labels=None, **kwargs):
        self.labels = labels or MESSAGES["en"]
        super().__init__(*args, **kwargs)
        self._positionals.title = self.labels["arguments"]
        self._optionals.title = self.labels["options"]

    def format_help(self):
        return super().format_help().replace("usage:", self.labels["usage"] + ":", 1)

    def error(self, message):
        raise InvalidScenario("arguments")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    lang = "en"
    for i, value in enumerate(argv):
        if value == "--lang" and i + 1 < len(argv) and argv[i + 1] in MESSAGES:
            lang = argv[i + 1]
        elif value.startswith("--lang=") and value.split("=", 1)[1] in MESSAGES:
            lang = value.split("=", 1)[1]
    msg = MESSAGES[lang]
    parser = Parser(description=msg["description"], add_help=False, labels=msg)
    parser.add_argument("-h", "--help", action="help", help=msg["help"])
    parser.add_argument("--lang", choices=sorted(MESSAGES), default="en", help=msg["language"])
    sub = parser.add_subparsers(
        dest="command",
        required=True,
        title=msg["commands"],
        parser_class=partial(Parser, labels=msg),
    )
    for command in ("validate", "run"):
        child = sub.add_parser(command, help=msg[command], add_help=False)
        child.add_argument("-h", "--help", action="help", help=msg["help"])
        child.add_argument("path", help=msg["path"])
        if command == "run":
            child.add_argument("--report", help=msg["report"])
    try:
        args = parser.parse_args(argv)
        document = load(args.path)
        if args.command == "validate":
            print(msg["valid"])
            return 0
        report = run_scenario(document)
        if args.report:
            with open(args.report, "x", encoding="utf-8") as output:
                json.dump(report, output, indent=2, sort_keys=True)
                output.write("\n")
        print(msg["ok"] if report["passed"] else msg["failed"])
        return 0 if report["passed"] else 1
    except (ValueError, OSError, RuntimeError) as exc:
        print(msg["error"] + " (" + type(exc).__name__ + ")", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
