# Scope and evidence

This release validates a bounded subset with actual Home Assistant triggers, conditions, timers, reload and script action dispatch. The actuator sinks and input states are synthetic. It does not prove wire protocols, current draw, sensor accuracy, a relay's physical state, safety, or behavior of every possible HA configuration.

The clock is real elapsed monotonic time. Tests intentionally use short intervals and scheduling margin. We do not patch internal HA delay methods, rewrite production timer durations or claim virtual-time equivalence. DST, wall-clock scheduling, full HA process restart and Recorder persistence are outside v1. Reload is tested; it is not a process restart.

Input contains no executable templates or integration configuration. Each worker uses a clean temporary directory, a stripped environment and a global audit guard. This prevents accidental Python network/subprocess I/O through the admitted path. It is not a hostile-code sandbox: Python/native dependencies, the interpreter and host are trusted. Run untrusted source or dependencies only in a separately secured environment. The optional Docker network-none recipe strengthens network isolation but does not prove hardware behavior.

Public reports should contain only synthetic fixtures. Real state timelines reveal occupancy and habits even without a token. No household inventory, recordings or production configuration is included here. All diagrams are labelled synthetic and reproducible with `python scripts/render_diagrams.py`.

See [validation](validation.md) for the measured checks performed on this release. Installation support is limited to environments in that record; the container recipe is not a claim that every platform was tested.
