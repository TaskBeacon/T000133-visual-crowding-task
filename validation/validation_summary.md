# Validation scope and evidence

Five real task-build gates passed on their first complete run: standard, TAPS, native QA, scripted simulation and sampler simulation. gate_report.json preserves commands, outputs and return codes. Later static checks passed after documentation/release metadata changes. Native experiment code, stimuli and timing were not changed after gate completion.

Six pure tests verify schedule/geometry/calibration/scoring; five actual PsychoPy trial cases verify ten semantic checks, including correct/wrong/omission/F8/plainq, report-onset response and fixed200ms array. Native screenshots of instructions, report and near/far/unflanked displays were actually inspected. Human startup with a mocked identity form refused missing calibration before window creation; it is not a human physical pilot.

Full citation/feasibility audit precedes implementation. The accepted plot required four imagegen rounds; three incorrect images were rejected, and a single representative flanked trial was accepted with explicit notes describing all remaining variants. Parent independently reviewed native screenshots,54 data/geometry checks and the final plot.

The H000133 derivative passed20 TypeScript/shared-runtime tests, owned-source-and-test typechecking, production bundling, actual cold browser execution and47 downloaded-data/DOM checks. Actual20trial/82stage browser JSON/CSV/JSONL contain synthetic behavior only. Pixel-level DOM projection agrees with canonical code within0.0102 CSSpx. See the paired H repository validation/ for raw evidence, actual screenshots, guard-abort evidence and genuine harness failures.

No actual screen dimensions or viewing distance were measured, and no physical pilot, eye tracking, display timing, luminance/gamma or clinical norm validation is claimed. Physical input fields remain null in research configuration. Measured-input research refusal and explicit synthetic software QA are both intentional successful behaviors, not a substitution of guessed physical calibration.

Runtime: installed psyflow0.1.12 at43e52fbfb5900e894d51ee7551cae971bb01f34e, PsychoPy2025.2.4, Python3.10. Web: published psyflow-web91d0537eb874933cb504fe675203c83b598c1514 (includes08041fd audio preload and6a03630 monotonic/textarea changes), Node at C:/nvm4w/nodejs/node.exe.
