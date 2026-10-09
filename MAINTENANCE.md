# Research maintenance

Markdown is the editable research record. Python source and tests define executable behavior; historical CSVs, figures and reports are retained as historical evidence, not current validation.

## Offline validation

```bash
python3 scripts/verify_research.py
```

This standard-library entry runs all unit tests, checks the offline optimum against its five explicit strategies and checks fixed-input repeatability and finite costs on a bounded integer-demand grid. It exits nonzero on a regression. The JSON result describes only that grid; it is neither a Monte Carlo study nor a general competitive-ratio proof. No model API, network or paid service is required.

## Research status and next work

The general competitive-ratio proof is incomplete. Existing methods use total demands in decision costs and guards; their status as online algorithms therefore still requires analysis of what information is available at each decision. `PurelyLocalAlgorithm` uses `min(duration, price)` and should not be treated as a verified online policy. Fractional-duration behavior is outside the integer-demand verification scope.

The previous comprehensive report stopped at section 2.1. Its listed sample size, confidence intervals and accuracy targets were claims in an unfinished draft; this repair does not supply missing runs or prove their statistical validity.

Fixed random input in the correlated implementation was ignored, and hybrid individual purchases omitted past rent of the other item while counting an extra future rental day. Both implementation defects are corrected with regression checks. Existing numeric results have not been regenerated after these fixes and must not be cited as current candidate results. Preserve these historical artifacts until a separately scoped reproducible experiment is run.

For further work, record input assumptions, seed, source revision, commands, actual outputs and remaining theoretical gaps in Markdown with machine-readable JSON alongside it. Keep simulation, bounded implementation checks and mathematical proof as distinct evidence.
