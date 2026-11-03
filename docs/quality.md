# Quality and security evidence

The [Check workflow](../.github/workflows/check.yml) runs on every pull request
and main-branch push. It installs the package, runs Ruff E4/E7/E9/F diagnostics,
runs the automated tests, checks relative documentation links and SVG syntax,
builds an sdist and wheel, and scans the full Git history using Gitleaks with
redacted output. Failures must be investigated before release; green checks are
bounded evidence, not proof that every defect is absent.

The tests exercise this bounded synthetic scenario runner using an isolated Home Assistant engine with synthetic inputs and negative cases.
See [the interface guide](../docs/install.md) and [security policy](../SECURITY.md) for
boundaries. No whole-repository coverage percentage, fuzzing campaign, complete
secure-design assurance case, signed release or independent continuity is claimed.
English, Russian, German and Spanish CLI catalogs and README entry points are
maintained with parity checks; detailed translations have their documented scope.

## Home Assistant beta evaluation on 2026-11-03

The development dependency is Home Assistant 2026.11.0b3, with its upstream
Pillow 13.0.0 and cryptography 50.0.2 requirements preserved in the complete
hash lock. This package runs the real HA engine in isolated synthetic workers;
it uses its own `scenario_runner` pytest plugin, not
`pytest-homeassistant-custom-component`. No deployed HA configuration changes.

The local Python 3.14.7/macOS dependency check passed for 114 installed packages.
The cryptography backend reported OpenSSL 4.0.3. The source archive and wheel
passed the package-content checks. A metadata audit of all 126 exact lock pins,
including dependencies conditional on other platforms, found no known
vulnerabilities and skipped no packages. This point-in-time result does not
prove absence of undisclosed flaws. Local runtime validation was not uniformly
successful: an initial run had a 30-second `manual_override` worker timeout;
a second full run passed 68 tests but `stale_sensor` returned worker exit 1.
A separate diagnostic invocation of that scenario passed. A fresh environment
installed from the built wheel passed five of seven runtime cases;
`manual_override` and `presence_timeout` reached the same 30-second parent
bound. These observations do not establish a root cause or a complete passing
macOS suite. Worker limits,
I/O isolation and behavioral assertions are unchanged.

The complete Linux [Check run 41573711037](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/41573711037)
passed for dependency source `77641a75061336607815e236ee1d32153de738e3`:
69 tests in 16.67 seconds, all seven installed-wheel runtime tests in 15.69
seconds, and the packaged container under `--network none --read-only`, with
capabilities dropped. CodeQL also passed. This is synthetic software acceptance
for that exact source; it does not erase the local macOS failures above. The
versioned release source requires its own complete Check before publication.

The earlier [validation record](validation.md) is historical evidence for its
specified source and runtime. The new dependency requires its own successful
full Linux Check workflow, including installed-wheel runtime tests and the
network-disabled container, before a beta is accepted. A beta dependency or
local package build alone does not qualify an RC or stable release or close
[issue #27](https://github.com/ha-homelab/ha-scenario-tests/issues/27).

## Dependency review on 2026-10-16

CI now uses pytest 9.0.3, which fixes local temporary-directory handling in
[GHSA-6w46-j5rx-g56g](https://github.com/advisories/GHSA-6w46-j5rx-g56g).
This concerns test tooling on a shared UNIX host, not a demonstrated remote flaw
in the offline application. Build metadata requires setuptools 83.0.0, which
contains the upstream Unicode MANIFEST pattern normalization
[fix](https://github.com/pypa/setuptools/commit/dd9f436a36486b4cb8a4c70a2321548b0be09b8f)
for [GHSA-h35f-9h28-mq5c](https://github.com/advisories/GHSA-h35f-9h28-mq5c).
The advisory's fixed-version field may lag the released upstream fix. Source
builds must still be checked for unwanted files; version changes alone do not
validate artifact contents.

The primary maintainer has personally confirmed familiarity with secure-design
principles and common Python/network-application vulnerabilities. The maintainer
also confirms no bug, enhancement or vulnerability reports outside GitHub in the
preceding 12 months. These are maintainer attestations, not automated test results.
The public issue history and current security findings must also be checked when
refreshing the badge assessment.
