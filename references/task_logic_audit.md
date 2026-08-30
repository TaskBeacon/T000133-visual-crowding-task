# Task Logic Audit

Written before any implementation on 2026-08-31. This is a Bouma-family behavioral adaptation, not a replication or a calibrated vision test. Source availability: Bouma (1970), DOI 10.1038/226177a0, publisher bibliographic page only; the full article was not obtained. Pelli, Palomares & Majaj (2004), DOI 10.1167/4.12.12, author-hosted primary article Methods pp.1141–1142 reviewed. Coates, Ludowici & Chung (2021), DOI 10.1167/jov.21.11.18, institutional full-text primary study/reanalysis pp.3–7 and16–18 reviewed. Bouma-specific method details are secondary reconstruction from that explicit reanalysis, not represented as direct access to the 1970 original.

## 1. Paradigm Intent

Identify a briefly presented peripheral lowercase letter, either alone or between two simultaneous radial x flankers. Manipulations are target eccentricity, hemifield and flanker separation. This concerns spatial crowding, not the response compatibility of T000004 Flanker. Report identification accuracy and omissions by spatial cell, plus response latency after stimulus offset. No clinical screening, acuity norm or automatic critical spacing estimate is provided. A coarse accuracy curve cannot establish a participant's threshold.

## 2. Block/Trial Workflow

Research starts only with operator-measured visible-screen width/height and viewing distance, an explicit measurement provenance record, and fullscreen presentation. Human configuration contains no invented measurements. Pixel dimensions supply only the denominator for conversion. A missing or invalid calibration refuses research before stimulus presentation. QA and simulation use a separate synthetic_geometry configuration and every row declares that provenance.

Five blocks of 100 trials: the complete 2 eccentricities × 2 sides × 5 spacing conditions × 25 target letters design is preplanned, shuffled with Python random.Random overall_seed, then divided into five blocks. This custom preplan is needed to balance target identity within every spatial cell across block boundaries. BlockUnit consumes the preplanned hashable condition tokens sequentially; it retains trial identity and execution ownership. Diagnostic profiles keep all 20 spatial cells with deterministically cycling target identities, unchanged single-trial timings, and explicitly do not estimate human effects. Rest between blocks is self-paced. No adaptive controller.

Trial states: fixation (600 ms, center black square, no keys) → array (200 ms, same fixation plus target and optional x flankers, no responses accepted) → report (same fixation and a low central response prompt, up to4000 ms; one lowercase target key or F8) → intertrial (300 ms, fixation only). A registered report ends the report period; deadline records omission. F8 means the participant noticed leaving fixation, invalidates the trial for accuracy and is self-report only. No correctness feedback. Array onset, array offset/report onset and software timestamps are retained; no hardware timing claim.

## 3. Condition Semantics

Eccentricities 3 and6 nominal degrees, left or right horizontal meridian. Spacing conditions: unflanked and target-to-flanker center separation .25, .40, .55 or .75 times eccentricity. Thus the smallest flanked separation is .75 nominal degrees. For a right target at E, inner and outer flanker angular positions are E−S and E+S; left displays mirror this. Each position is separately projected by x=D*tan(theta), not by adding a central pixels-per-degree approximation. The 1970 empty letter-slot convention is not mislabeled as center spacing.

Targets are all lowercase English letters except x; both flankers are x. Shared raster glyph assets derived from Courier New preserve font cell/baseline geometry and are used by both runtimes. Nominal x-height .50 degrees is an explicit visibility adaptation from Bouma's smaller print. It is held constant across eccentricity. Unflanked trials measure the baseline limitation; poor baseline identification prevents any crowding-threshold interpretation. Chinese participant prose uses SimHei. All prose and keys live in YAML; glyphs are task material, not Chinese prose.

## 4. Response and Scoring Rules

The first registered a–z key except x selects a target identity. F8 records a noticed fixation violation. Correct is response==target and no reported violation; missing responses are omissions; reported violations and omissions remain separate fields. Accuracy summaries exclude reported fixation violations, count omissions incorrect, and separately report omission rate and each denominator. Correctness is not response-conflict congruency. RT is measured from the post-array response screen; it is not perceptual processing latency. QA/simulation values are synthetic, never human results.

## 5. Stimulus Layout Plan

Fixation is centered. Array glyph x-height is converted separately using the measured vertical pixel scale; horizontal widths use the horizontal scale, preserving physical glyph aspect. Their cell centers use exact horizontal projection. All glyph extents must fit within the available screen with a margin and must not overlap. Display aspect mismatch, invalid distances, too-small glyph sampling and clipping fail closed. The task will retain the nominal angles, projected pixel coordinates, physical-input provenance and runtime pixel dimensions. Fullscreen CSS pixels are not physical pixels; devicePixelRatio is not physical calibration. Actual research measurement remains an operator responsibility. No calibration has been physically performed in this build session.

Report prompt is below fixation at y=−150 pixels, font24, wrap width1000; no array letters remain during report. Instruction/rest/goodbye screens use explicit line breaks, font24 and wrap width1100. QA captures actual native and web rendering to inspect glyphs and text.

## 6. Trigger Plan

Mock behavioral trigger driver. Experiment start1, fixation10, array20, report30, key response31, self-reported fixation violation32, report omission33, intertrial40, experiment end99. StimUnit owns phase/response/timeout events; no manual phase timing loop.

## 7. Architecture Decisions (Auditability)

main.py/main.ts visibly perform configuration, research-versus-synthetic validation, initialization, instructions, block construction, trial execution, breaks and completion. Pure helpers in utils own the factorial schedule, geometric projection/bounds and score summary. run_trial only orchestrates audited stages using StimUnit/TrialBuilder. No custom controller or private framework methods. Shared degree conversion is not used: this task requires exact eccentric-position projection and independent physical x/y scales; it emits documented pix coordinates. Generic fullscreen/force-quit/export remain framework-owned. No unrelated framework mutation planned.

## 8. Inference Log

Adapted: Courier New rendered bitmap rather than 1970 printed Courier; .50-degree x-height; center spacing levels and E=3/6; explicit keyboard report and F8; no audio; fixed high-contrast black/white rather than Pelli contrast staircase. Inferred: .6s fixation,4s report,.3s intertrial,500-trial balance and100-trial rests. Supported family features: peripheral letter identification with simultaneous flankers,200ms exposure, constant-stimulus spacing and unflanked baseline. These decisions are not attributed as exact Bouma or Pelli methods. Eye tracking is absent; instructions, brief exposure and F8 can neither prove fixation nor detect unreported anticipatory saccades. Luminance/gamma, physical timing and actual geometry have not been instrument-validated. Computational geometry QA and real raster screenshots establish software behavior only.
