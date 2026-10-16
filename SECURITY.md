# Security

Report vulnerabilities privately through the repository's security reporting facility when enabled, rather than posting exploitable details or credentials in public issues. If unavailable, ask the maintainer for a private channel without attaching secrets.

The runner accepts a restricted JSON format and starts a fresh installed Python worker with a temporary HA configuration. Python audit hooks reject network/DNS/subprocess attempts, including attempts from background tasks. No URL/token/live config option exists. Templates, custom integrations, arbitrary service data and real entity names are deliberately excluded.

The interpreter and dependencies are trusted. This is not a native-code or filesystem sandbox. For an additional OS network boundary use the documented non-root container with `--network none`, no production volumes and read-only root. Never mount Docker or host sockets. Installation and container building need network access; runtime containment does not apply to package installation.

Only publish synthetic reports. Even token-free real timelines can reveal household behavior. CLI errors avoid echoing raw input; direct worker tracebacks are for local diagnosis and need review before sharing.


## Private reports and handling

Use [the private vulnerability form](https://github.com/ha-homelab/ha-scenario-tests/security/advisories/new)
or email **alvit.work@gmail.com**. Include the affected revision, impact and a
minimal synthetic reproduction. Never send live credentials or household data.
The latest source on the 0.1 maintenance line receives fixes; update to the latest
reviewed revision before filing a report when possible.

The maintainer aims to acknowledge reports within 14 days, assess severity and
reproduce them privately, agree on disclosure timing with the reporter, and test
the fix before release. Confirmed critical issues are addressed immediately;
other medium-or-higher issues should be fixed within 60 days. Release notes list
available CVE/GHSA identifiers and upgrade instructions. Reporters receive credit
unless they request anonymity. If the first contact receives no response, retry
the other private channel. There is currently no independent security team or
backup maintainer; [governance](GOVERNANCE.md) records that limitation.
