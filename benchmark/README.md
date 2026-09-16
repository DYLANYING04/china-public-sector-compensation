# Launch Benchmark v0.1

This is a reproducible, curated launch corpus of 30 Chinese enterprise and public-institution inputs. It measures whether a public official disclosure path was found and what result state the skill can responsibly reach from that path.

It is **not** a population estimate for all Chinese institutions: the corpus deliberately spans national, municipal, county, special-zone, hospital, school, museum, and remote-area disclosure systems. It is published so that future contributions can be reviewed against a fixed baseline rather than anecdotes.

## Snapshot

Checked: 2026-09-16. Source records and outcomes are in [cases.json](cases.json).

| Metric | Result |
|---|---:|
| Inputs | 30 |
| Official landing page or attachment found | 30 / 30 (100.0%) |
| Usable wage breakdown found | 28 / 30 (93.3%) |
| `FULL` | 2 / 30 (6.7%) |
| `STRUCTURE_ONLY` | 24 / 30 (80.0%) |
| `BUDGET_ONLY` | 2 / 30 (6.7%) |
| `NO_USABLE_DATA` | 2 / 30 (6.7%) |
| Accepted cross-scope divisions | 0 |
| Rejected cross-scope / inaccessible cases | 3 |

`FULL` is intentionally rare because the standard requires a same-year, same-scope headcount. A public `公开06表` alone is useful evidence, but it is not permission to manufacture a per-person result.

The initial corpus does not publish a median end-to-end search time. An interactive research agent's elapsed time depends on portal latency, CAPTCHA and document format; presenting a fabricated number would be misleading. The next benchmark revision will add a deterministic browser harness and separately report median source-fetch time and median end-to-end research time.

## Reproduce

```text
python scripts/benchmark_summary.py benchmark/cases.json
```

The script validates the case schema and prints the table above. It does not fetch sources or claim that a landing page will remain available indefinitely. Open the official URL in each record to reproduce the source inspection.

## Interpretation

- `FULL`: final-account wage inputs and a matched same-year headcount were found.
- `STRUCTURE_ONLY`: a current final-account wage breakdown was found, but a matched headcount was not. The skill can still apply the author's wage-structure route when all required component values are available.
- `BUDGET_ONLY`: no usable final account was retained for the case; any result must be labelled as a budget estimate.
- `NO_USABLE_DATA`: the sweep retained an official lead, but did not obtain a usable wage breakdown. The reason code distinguishes access barriers from non-disclosure.

The corpus rejects scope mismatches instead of forcing a quotient. Examples include a department-wide amount paired with a center-only staff count, and a source accessible only through an unverified JavaScript portal.
