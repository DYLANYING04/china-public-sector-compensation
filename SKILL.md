---
name: china-public-sector-compensation
description: Research a named Chinese enterprise or public-sector institution, exhaust official reports and staffing sources, and calculate compensation step by step using the specified expert methodology. Use when the user asks about a unit's 工资、待遇、人均工资福利、普通员工收入 or salary structure; report 搜不到 when the required real data cannot be found.
---

# China Enterprise and Public-Institution Compensation

Given only a unit name, independently identify the unit, search the available reports, reconcile the data scope, and calculate its compensation. Use real source figures and the expert rules in this skill. Do not substitute a different salary model.

## Zero-Setup User Path

The user should be able to send only `研究：单位全称的待遇` and receive a result. Do not ask the user to prepare links, JSON, source files, route labels, or accounting codes.

- If no year is supplied, start with the latest completed fiscal year available as of today; if that final account is not published, step back to the newest usable final account and label the year explicitly.
- If the name maps to one clear official entity, proceed without a confirmation question. If it maps to multiple entities, ask one concise question listing the ambiguous candidates.
- If the user gives a city, alias, former name, supervisor, or unit type, use it as a search constraint but do not require any other setup.
- Choose the expert route from the evidence. Never ask the user to choose route A/B/C/D unless the official evidence genuinely leaves two incompatible entities.
- Never block the first result only because headcount is missing: return a sourced `STRUCTURE_ONLY` judgment, list the missing field, and continue the headcount search when useful.
- Put a three-line quick result first: `单位/年度`, `证据状态`, and `结论或搜不到原因`. Put the audit trail and detailed calculation below it.

## Non-Negotiable Rules

1. Use the expert procedure in [references/expert-method.md](references/expert-method.md) step by step. The `2/3`, `1/2`, and salary-structure ratio rules are part of the requested method, not optional commentary.
2. Every input number must be traceable to a source. Never invent a missing amount, headcount, year, unit, or institutional classification.
3. Match the numerator and denominator before dividing. Confirm entity scope, reporting year, budget versus final account, amount unit, personnel category, funding scope, and whether the document is department-wide or unit-level.
4. If a required real figure cannot be found after completing the search checklist, say `搜不到` and identify the missing field. Do not fill the gap with a generic industry average.
5. Distinguish sourced inputs from calculated results. The expert conversion is the calculation method; the amounts and headcounts must still come from real documents.
6. Prefer final accounts (`决算`) to budgets (`预算`). If only a budget exists, calculate from it but label the result as a budget estimate.
7. Open and inspect the actual report or attachment. Search-result snippets and reposted tables are leads, not sufficient evidence by themselves.
8. Preserve the meaning of the result. A fiscal `工资福利支出` quotient is not automatically cash salary or take-home pay because it can include employer-paid social insurance, occupational annuity, and housing provident fund.
9. Treat blank cells as missing unless the table legend expressly defines blanks as zero. Never silently convert an unreadable or blank amount to `0`.

## Workflow

### 1. Resolve the Entity

- Establish the full official name, aliases or former names, supervising department, region, institution type, and whether the target is a unit, a department, or a subordinate body.
- When names collide, use official addresses, duties, organization codes, and supervising relationships to disambiguate.
- Read [references/institution-classification.md](references/institution-classification.md). Record `官方机构身份` and `作者方法分析路线` separately. Never infer an official `公益一类/二类`, `参公`, or enterprise-style status from the name, industry, funding source, or apparent salary structure.
- Select the closest expert route from the evidence without presenting that analytical route as the unit's legal classification.

### 2. Search Exhaustively

Read [references/source-playbook.md](references/source-playbook.md) and complete its source and query checklist. For local units, also read [references/city-coverage-patterns.md](references/city-coverage-patterns.md). Search the newest usable final account first, then adjacent years and supplementary staffing records. Follow attachment links, inspect spreadsheets and archives, and OCR scanned PDFs when needed.

Maintain a search log with the query, channel, result, document year, and reason a source was accepted or rejected. `Exhaustive` means every relevant channel and query family in the playbook was attempted, not that the search runs without a stopping condition.

For a no-year request, treat “latest completed fiscal year” as a search default, not as permission to silently mix a budget and a final account. State the search cut-off date and chosen year before calculating.

Run the amount search and headcount search in parallel. As soon as the exact unit's public `公开06表` or equivalent breakdown is available, calculate the expert wage-structure multiple. Continue searching for matched headcount; do not delay the structure result until all personnel channels have failed.

### 3. Build the Evidence Ledger

For every number record:

- source title and direct URL;
- publisher and publication date;
- reporting year;
- page, table, row, or section;
- original label and value;
- original amount unit;
- entity and personnel scope;
- funding scope, such as general-public-budget appropriation only or total payroll;
- whether it is budgeted or realized.

Assign the case an evidence state that is separate from the expert route letters:

- `FULL`: final-account wage data and same-year matched headcount; calculate the full per-person result;
- `STRUCTURE_ONLY`: final-account wage components but no matched headcount; calculate the structure result and keep searching for headcount;
- `BUDGET_ONLY`: only budget wage data; calculate a budget estimate and label it as such;
- `NO_USABLE_DATA`: no usable wage breakdown; report `搜不到` after the stopping checklist.

For every incomplete case, add one or more reason codes: `NOT_DISCLOSED`, `NOT_FOUND_AFTER_CHECKLIST`, `ACCESS_BLOCKED`, `SCOPE_MISMATCH`, or `YEAR_MISMATCH`. Do not turn an inaccessible portal into a claim that the document does not exist.

Do not combine values across years or scopes unless the document explicitly makes them comparable. If a report is consolidated, do not divide it by the headcount of only one subordinate unit.

### 4. Apply the Expert Route

Use the route selected in step 1 and calculate in the order given in [references/expert-method.md](references/expert-method.md):

- local units: wage components divided by staff count, source-identified special awards handled separately, then ordinary staff estimated at `2/3` of the comparable average;
- public-welfare class I: find registered or annual-report headcount and divide the matched wage total directly;
- public-welfare class II or mixed-staff units: calculate the bonus/performance/allowance-to-basic-wage ratio; interpret `>= 4` as good, `< 3` as poor, and use provident-fund and occupational-annuity ratios for the remaining judgment;
- units meeting the author's leadership-skew/enterprise-style condition: total wage amount divided by the matched total headcount, then ordinary staff estimated at about `1/2` of the average.

Use `scripts/calculate_compensation.py` for arithmetic when the inputs fit its schema. Its CLI requires provenance and scope metadata; do not bypass that validation for a real case.

### 5. Cross-Check

- Recalculate all unit conversions, especially `元`, `万元`, and `亿元`.
- Compare at least two adjacent years when available and investigate abrupt changes.
- When the report is a department or center consolidation, read its listed budget-unit scope and personnel section before accepting any headcount. A center-only figure from a different year cannot denominator-match a consolidated report.
- Check whether `301 工资福利支出` contains employer social-insurance, housing-fund, occupational-annuity, medical, or one-off items.
- Determine whether the report covers only fiscal appropriations or total compensation. This is especially important for universities, hospitals, and institutions with operating or service income.
- Check whether labor dispatch, externally hired staff, retirees, or subordinate units are included in either side of the division.
- Rank the denominator explicitly: annual-average actual staff is strongest for annual expenditure; year-end actual staff, unspecified-date actual staff, and establishment count require progressively stronger caveats. Show a sensitivity range when a second credible denominator is available.
- Reconcile extracted `301xx` rows to the disclosed `301` total when the table provides all rows. Investigate differences beyond stated rounding.
- Exclude a special or one-off award only when the document or another reliable source identifies it as such; a large number alone is not enough.
- Use official recruitment materials and credible employee disclosures as consistency checks, while keeping their evidentiary role explicit.

### 6. Report

Follow [references/output-template.md](references/output-template.md). Lead with the result, show the author's calculation line by line, provide direct citations for every input, and state the exact data scope. Call the result an annual/monthly equivalent under the author's method unless the source directly proves cash or take-home salary.

If a result cannot be calculated, still provide the entity resolution, sources searched, figures found, and the specific missing or incompatible field, ending the conclusion with `搜不到，无法按该方法计算`.
