# Genuine initial failures

- First standalone standard checker failed because assets/README contained the forbidden literal token in a sentence denying such assets, and stimulus mapping rows lacked the checker's required backticks. Prose and row formatting corrected; no scientific gate was removed. Subsequent checker passed with recommended README subsection warnings.
- An inline metadata-enrichment Python command had a mismatched closing bracket and did not run. Replaced with the inspectable scripts/register_support.py, then rebuilt the evidence bundle.
- build_reference_bundle.py overwrites parameter_mapping.md with generic auto-population; that generated draft is being replaced by the already authored source-specific mapping before final gates.
- Shared image-rendering seam needs optional objectFit:fill so calibrated x/y dimensions are not silently constrained by contain. The default remains unchanged. Parent coordinates publication; initial10DOM/coretests passed.

- Initial README metadata missed required Name/Date Updated/PsyFlow Version rows; added the actual metadata before five gates. TAPS warnings for unused Changed/Fixed changelog sections and absent legacy outputs/sim directory remain warnings, not hidden failures.
- Human-startup refusal was correctly recorded but first stdout printing failed under cp1252. Original log retained, ASCII-safe logging reran successfully; no experiment code changed.
