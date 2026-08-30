# Native visual review

2026-08-31. Inspected the actual PsychoPy PNGs, not a reconstructed browser rendering.

- native_instruction.png: all Chinese instructions and synthetic-only warning readable; no overlap or clipping.
- native_near.png: central fixation and right peripheral x-a-x cluster; common x-height baseline and separated ink.
- native_far.png: left peripheral outer-x / g / inner-x, larger radial spacing; fixation remains central.
- native_unflanked.png: right peripheral q and central fixation, no flankers.
- native_report.png: target removed, fixation retained, lower report instructions readable.

PASS for display structure and readability. Synthetic dimensions are computational fixtures, not physical measurements. No human fixation, photodiode timing, luminance or clinical validity was measured. Parent independently inspected three array screenshots and instruction PNG, with measured black-pixel bounds within 2.5 px of synthetic geometry.

Five gates passed on the first complete run. Five actual native semantic trials passed ten checks. The native array-to-report software intervals ranged 0.18825–0.21616 s (within two frames of the requested 200 ms); these are software timestamps, not verified physical exposure. The research startup test supplied identity via a mocked form and confirmed missing-calibration refusal before window construction; it is not a physical pilot.
