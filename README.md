# Visual Crowding Task

| Field | Value |
|---|---|
| ID / slug | T000133 / visual-crowding-task |
| Name | Visual Crowding Task |
| URL / Repository | https://github.com/TaskBeacon/T000133-visual-crowding-task |
| Short Description | Peripheral letter identification across target-flanker spacing and eccentricity |
| Created By | TaskBeacon |
| Date Updated | 2026-08-31 |
| PsyFlow Version | 0.1.12 (installed workspace build; runtime commit recorded in validation) |
| PsychoPy Version | 2025.2.4 |
| Modality | visual, behavioral |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (disabled) |
| Version | 0.1.0; 2026-08-31 |
| Acquisition | behavioral, Chinese instructions (SimHei) |
| Canonical / web | Python canonical; H000133 derived |
| Status | synthetic software validation passed; no physical calibration or human pilot |

## 1. Task Overview

Identify a200ms peripheral lowercase target alone or between two simultaneous x flankers. Varying target eccentricity and center-to-center spacing supports an accuracy–spacing function. This is spatial crowding, distinct from response-conflict Flanker. It is an explicitly adapted Bouma-family paradigm, not a replication, visual screening tool or established norm.

The provided Bouma1970 publisher page did not supply full text. Historical Courier/letter/x-flanker details are reconstructed through the explicit Coates2021 reanalysis. Pelli2004 primary Methods supplies a directly checked200ms simultaneous-letter precedent; its Sloan letters and contrast staircase are not reproduced. Every adapted/inferred decision appears in references/task_logic_audit.md and parameter_mapping.md.

## 2. Task Flow

![Task Flow](task_flow.png)

The figure shows one representative flanked trial, not every spatial condition. In an unflanked trial both x flankers are removed; fixation, target eccentricity and the entire phase/response sequence are unchanged. The drawing is schematic and does not demonstrate physically calibrated angular spacing.

### Block-Level Flow

| Step | Behavior |
|---|---|
| Calibration | collect real operator inputs; reject unconfirmed/invalid geometry before fullscreen initialization |
| Setup | read actual framebuffer; project all conditions and reject bounds/overlap/sampling failures; preload every target glyph |
| Instructions | instruction text, space to start |
| Blocks | five blocks of100; factorial preplan shuffled before partition; rest between blocks |
| Completion | persist all trial rows and cell summaries; good_bye then space |

### Trial-Level Flow

| Phase | Stimuli | Duration / response |
|---|---|---|
| fixation | fixation square |600ms;no response |
| array | fixation + target + optional inner_x/outer_x |200ms fixed;no response |
| report | fixation + report_prompt |4000ms maximum;letter orF8 terminates |
| intertrial | fixation |300ms;no response |

### Controller Logic

| Component | Rule |
|---|---|
| Adaptive controller | none |
| Geometry | exacttan projection and independent axis scaling; every condition checked before acquisition |
| Summary | accuracy by spatial cell,omissions andself-reported violations separately;no fitted threshold |

Block flow: measured-input validation → fullscreen geometry/bounds checks → instructions → five100-trial blocks, with self-paced rests → save/completion. A complete factorial of2eccentricities ×2sides ×5spacing cells ×25letters yields500trials. A single PythonRandom-compatible preplan shuffles the full design before block partitioning. BlockUnit owns trial execution; no adaptive controller is used.

Trial flow: central fixation600ms → same fixation plus peripheral letter array200ms → target absent, report screen up to4000ms → fixation-only intertrial300ms. Array display is fixed duration and accepts no response. First valid report key ends only the report stage. Responses during array are not registered. RT starts at report onset, not array onset.

Keys: the corresponding lowercase letter (all English letters exceptx), F8 for a noticed fixation departure, space for instruction/rest screens. Plainq is a target response; Ctrl+Q is framework quit. No correctness feedback. F8 invalidates that trial for accuracy but is only a self-report: no eye tracker verifies gaze, and unreported violations may remain.

## 3. Configuration Summary

All settings below come from config/config.yaml. Diagnostic mode profiles alter counts/provenance only,not single-trial timing.

### a. Subject Info

| Field | Meaning |
|---|---|
| subject_id |101–999 numeric identity |
| screen_width_cm / screen_height_cm | ruler/tape measurements of active visible display |
| viewing_distance_cm | centered eye-to-screen distance |
| measurement_date / measurement_method / measurement_ack | measurement provenance andexplicit confirmation |

### b. Window Settings

| Parameter | Value |
|---|---|
| units / background | pix / white |
| fullscreen | required for research; diagnosticwindow1280×800 |
| screen |0 |
| pixel denominator |actual framebuffer for native; actualfullscreenCSSextent for web |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| fixation | rect | centeredblack .15degree square |
| glyph_a throughglyph_z,excludingx | image | sharedCourierNew-derived target material |
| inner_x / outer_x | image | concurrentradialflankers |
| instruction / report_prompt / block_break / good_bye | text | SimHeiChinese prose,explicitlinebreaks |

### d. Timing

| Phase | Duration |
|---|---|
| fixation |.6s |
| array |.2s |
| report |4s max |
| intertrial |.3s |

### e. Triggers

| Event | Code |
|---|---|
| experiment start/end |1/99 |
| fixation/array/report/intertrial onset |10/20/30/40 |
| identity response/self-reportedfixationbreak/omission |31/32/33 |

| Category | Values |
|---|---|
| Subject | numeric101–999 identity; experimenter measured screen width/heightcm, eye distancecm, measurement date/method and acknowledgement |
| Research window | fullscreen required; pixel dimensions read from actual initialized framebuffer |
| Geometry | E=3/6nominal degrees,L/R; center spacing .25/.40/.55/.75E or unflanked; exacttan projection of each center |
| Glyphs |25lowercase targets excludingx; two radialxflankers; shared Courier New raster derivatives; x-height .50nominal degrees |
| Timing | fixation .6s,array .2s,report4s,intertrial .3s |
| Triggers | experiment1/99,fixation10,array20,report30,response31,reported gaze departure32,omission33,intertrial40;mockbehavioral |
| Controller | none; fixed factorial design |

Run human: `python main.py human --config config/config.yaml`. The form requires actual ruler/tape measurements; missing/unconfirmed/implausible measurements fail closed. The research YAML contains null measurements and never falls back to EDID or assumed physical dimensions. Centered/perpendicular viewing and maintained head distance are operator responsibilities. The task verifies bounds and software coordinate consistency; it cannot verify the truth of measurements.

Run QA: `psyflow-qa . --config config/config_qa.yaml --no-maturity-update`. Simulations: `python main.py sim --config config/config_scripted_sim.yaml` and `config/config_sampler_sim.yaml`. All these use20spatially complete diagnostic trials and explicitly synthetic geometry. Every reduced row records geometry_provenance. Passing synthetic tests does not validate real centimeters, actual gaze, physical timing or a participant's crowding effect. Never reuse synthetic dimensions for research.

Raw phase traces remain standard PsyFlow data; reduced rows are one logical trial each. Additional fields preserve E,side,spacing,letter,projected pixel sizes/positions,geometry provenance,input measurements,accuracy eligibility,omission,self-reported fixation departure and report-onset RT. Summaries give cell counts/accuracy and explicitly leave critical_spacing_deg null. Omission counts remain visible; F8trials are excluded from the accuracy denominator. Physical display onset is not established by software timestamps.

## 4. Methods (for academic publication)

This authored adaptation presents a constant-size peripheral Courier-derived target either alone or between two concurrent radialxflankers. The preplanned factorial manipulates nominal eccentricity,hemifield and center separation. Target presentation lasts200ms,followed by a keyboard identity report. The larger .50degree x-height,spacing set,keyboard protocol,500trials andrest policy are explicit adaptations/inferences. Results require inspection of unflanked baselines; poor isolated-letter visibility and unverified fixation may confound any crowding interpretation. The task does not fit a critical spacing threshold or assert Bouma's proportionality as a universal constant.

Only operator-reported physical measurements support angular conversion; this release has no physical calibration or human pilot evidence. Luminance,gamma,display latency andgaze were not instrument-validated. Fixed brief exposure andF8reports cannot detect all anticipatory saccades. Browser CSSpixels/DPR differ from native framebufferpixels; both use actual coordinate extents only as denominators and must be matched to the measured visible display. See references/feasibility.md for source availability and all restrictions.

References: [Bouma1970](https://doi.org/10.1038/226177a0), [Pelli etal.2004](https://doi.org/10.1167/4.12.12), [Coates etal.2021](https://doi.org/10.1167/jov.21.11.18).
