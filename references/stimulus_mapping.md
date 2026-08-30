# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `unflanked` | array | fixation,target | central black square; one peripheral lowercase Courier-derived letter | BOUMA1970,COATES2021 | 2021 p.3 historical method reconstruction | generated_reference_asset | assets/glyphs/a.png throughz.png | 25targets excludingx; actual cell layout audited |
| `spacing_025` | array | fixation,target,inner_x,outer_x | target between two simultaneous lowercase x,center separation .25E | PELLI2004,COATES2021 | horizontal simultaneous flankers; center-spacing analysis | generated_reference_asset | assets/glyphs/*.png | E=3/6,left/right; no response compatibility manipulation |
| `spacing_040` | array | fixation,target,inner_x,outer_x | same array,center separation .40E | PELLI2004,COATES2021 | same source | generated_reference_asset | assets/glyphs/*.png | samefont/color/size |
| `spacing_055` | array | fixation,target,inner_x,outer_x | same array,center separation .55E | PELLI2004,COATES2021 | same source | generated_reference_asset | assets/glyphs/*.png | exact individualcenter projection |
| `spacing_075` | array | fixation,target,inner_x,outer_x | same array,center separation .75E | PELLI2004,COATES2021 | same source | generated_reference_asset | assets/glyphs/*.png | boundschecked beforedisplay |
| all | fixation/intertrial | fixation | centered black square | PELLI2004 | Methods peripheral fixation | psychopy_builtin | none | .15 nominal degree square |
| all | report | fixation,report_prompt | fixation plus Chinese request belowcenter; target absent | PELLI2004 | postarray report in Methods | psychopy_builtin | none | keys taughtin instruction;F8 for noticedgaze departure |
| all | instruction/rest/completion | instruction,block_break,good_bye | Chinese explanations,rest and explicit unverified gaze/no norms note | adaptation | acquisition instructions | psychopy_builtin | none | SimHei,explicit wrapping |

Static glyph assets are non-placeholder task material. File alpha extents, shared baseline/cell center and x-height measurement are recorded in assets/glyph_metrics.json. Exact counts/parameter values are author adaptations and do not imply those values were all tested together in the cited papers.
