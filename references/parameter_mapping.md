# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| eccentricity | task.eccentricities_deg | [3,6] | COATES2021 | historical reanalysis p.3 left/right peripheral letters | adapted | nominal screen positions; no eye-tracked retinal locations |
| spacing | task.spacing_ratios | [.25,.40,.55,.75] plus unflanked | PELLI2004 | Methods p.1141 center spacing | adapted | not Bouma empty-slot spacing |
| exposure | timing.array_duration | .2s | PELLI2004 | Methods pp.1141-1142 | direct | fixed exposure,no early response |
| glyph_size | task.xheight_deg | .50deg | COATES2021 | p.3 documents smaller historical Courier x-height | adapted | larger print,constant angular x-height; baseline visibility unvalidated |
| material | task.alphabet | 25lowercase letters excludingx | BOUMA1970,COATES2021 | 2021 pp.3,6 explicit historical reconstruction | adapted | CourierNew derivatives,not direct1970replication |
| fixation | timing.fixation_duration | .6s | PELLI2004 | Methods continuous peripheral fixation | inferred | no eye tracking |
| report | timing.report_duration | 4s | PELLI2004 | Methods poststimulus response | adapted | keyboard report,RT from report onset |
| intertrial | timing.intertrial_duration | .3s | PELLI2004 | repeated trials | inferred | fixation only |
| count | task.total_trials / total_blocks | 500 / 5 | COATES2021 | p.16 constant-stimulus procedure | adapted |20spatialcells x25targets;100trial rests |
| geometry | task.calibration / subject fields | null/unconfirmed research;separate synthetic fixture | geometry definition | x=Dtan(theta),separate axis scales | inferred | no physical measurement made by this agent |
| gaze report | task.fixation_break_key | f8 | adaptation | compensate partially for absent eye tracking | inferred | self-reported departures excluded;unreported departures undetected |
| trigger map | triggers.map |1,10,20,30,31,32,33,40,99 | adaptation | behavioral acquisition lifecycle | inferred | mockdriver,no hardware timing |

All spatial/layout,source-access andinference decisions are detailed in task_logic_audit.md. No exact1970replication claim. Array removal is the report flip; the framework array offset stamp is the final array frame,so array_to_report_software_interval_s uses the two phase flip timestamps instead. This is software timing,not photodiode evidence.
