# Expert Method

This reference operationalizes the method supplied by the user. Apply it in the stated order. The inputs must be real sourced figures; the conversion factors and thresholds are the expert's judgment rules.

## Route A: Local Public Institutions

This is the default route for Beijing municipal public institutions and analogous local units whose staffing is disclosed clearly.

1. Find the unit's final-account report and its detailed basic-expenditure table.
2. Find the public-establishment or actual-staff headcount for the same entity and year.
3. Identify the recurring wage figures used by the author. Add the comparable wage components and divide by the headcount:

   `organization average = sum(comparable wage components) / matched headcount`

4. Identify a conspicuous unit-specific or task-completion award separately. Do not treat it as recurring compensation for comparisons with units that do not have it. Show both the recurring calculation and the award amount when present.
5. Estimate an ordinary section-level employee (`科级大头兵`) at two thirds of the comparable organization average:

   `ordinary employee estimate = organization average x 2/3`

6. Convert the annual figure to a monthly figure by dividing by 12.

### Screenshot Example

Using the author's example values, all in `万元`:

- comparable wage components: `503 + 1764`;
- matched staff count: `88`;
- separately identified award: `196`;
- organization average: `(503 + 1764) / 88 = 25.7614 万元/人/年`;
- ordinary employee estimate: `25.7614 x 2/3 = 17.1742 万元/年`;
- monthly equivalent: `17.1742 / 12 = 1.4312 万元/月`.

When working on a real unit, replace every example value with the latest matched source data. Do not copy these figures into another unit.

## Route B: Ministry-Affiliated Public-Welfare Class I

Use this route when non-establishment staff are few and the final-account wage total mainly corresponds to registered staff.

1. Search the institution-registration or establishment-information system using the full official name.
2. Inspect the unit's annual report for its total staff count.
3. Cross-check that count against budget/final-account establishment disclosures, recruitment notices, or other official staff statements.
4. Divide the matched wage-welfare total by the matched staff count directly:

   `per-person treatment = matched wage-welfare total / matched headcount`

5. If the staff figure is a year-end count rather than an annual average, state that exact denominator basis.

## Route C: Public-Welfare Class II or Mixed-Staff Institutions

Use this route when annual-report headcount commonly includes substantial non-establishment staff or when no reliable matched denominator exists.

1. Extract `基本工资`.
2. Add the disclosed `奖金 + 绩效工资 + 津贴补贴` items that belong to the same report scope.
3. Calculate:

   `structure multiple = (奖金 + 绩效工资 + 津贴补贴) / 基本工资`

4. Apply the expert interpretation:

   - `>= 4`: 待遇不错;
   - `< 3`: 待遇较差;
   - `3 to < 4`: intermediate; continue with the following ratios.

5. Calculate and compare, when the source provides the components:

   - `住房公积金 / 工资基数`;
   - `职业年金 / 工资基数`.

The source may not disclose the legally relevant contribution base. In that case use the specific wage denominator available in the same table and name it exactly.

## Route D: Enterprise-Managed Public Bodies

Use this route for bodies such as the National Council for Social Security Fund or People's Bank branches when the organization is managed more like an enterprise and leadership pay raises the average.

1. Find the total wage or salary amount for the target year.
2. Find the matched total employee count for the same entity scope.
3. Calculate the organization average:

   `organization average = total wage amount / total employee count`

4. Estimate ordinary staff at about half of that average:

   `ordinary employee estimate = organization average x 1/2`

5. For branches or systems with many subordinate units, reduce the denominator to the target branch's verified or best-supported staffing scope before dividing.

### Screenshot Example

- total wage amount: `9600 万元`;
- total staff count: `200`;
- organization average: `9600 / 200 = 48 万元/人/年`;
- ordinary employee estimate: `48 x 1/2 = 24 万元/年`;
- monthly equivalent: `24 / 12 = 2 万元/月`.

## When Headcount Cannot Be Found

Follow the author's fallback order:

1. analyze the wage structure multiple;
2. analyze the housing-provident-fund-to-wage ratio;
3. analyze the occupational-annuity-to-wage ratio.

Do not fabricate headcount to force a per-person result. Report the structural result even when no per-person number can be produced.

## Calculator Inputs

Save a UTF-8 JSON file and run:

```text
python scripts/calculate_compensation.py input.json
```

For routes A, B, and D:

```json
{
  "mode": "headcount",
  "route": "local_public_institution",
  "comparable_wage_components_wanyuan": [503, 1764],
  "special_awards_wanyuan": [196],
  "headcount": 88,
  "provenance": {
    "entity_name": "单位全称",
    "route_basis": "地方事业单位；按作者的地方单位路线计算",
    "report_year": 2024,
    "basis": "决算",
    "input_amount_unit": "万元",
    "normalized_amount_unit": "万元",
    "unit_conversion": "原表单位已为万元，无换算",
    "amount_scope_match_confirmed": true,
    "amount_scope_match_note": "决算封面和表内单位名称均为该单位本级",
    "amount_source": {
      "title": "单位全称2024年度单位决算",
      "url": "https://official.example/report.pdf",
      "publisher": "发布机关全称",
      "publication_date": "2025-08-20",
      "retrieved_date": "2026-09-16",
      "locator": "公开06表，第12页，301栏",
      "year": 2024,
      "entity_scope": "单位全称"
    },
    "headcount_source": {
      "title": "单位全称2024年度报告",
      "url": "https://official.example/annual-report.pdf",
      "publisher": "发布机关全称",
      "publication_date": "2025-03-31",
      "retrieved_date": "2026-09-16",
      "locator": "人员情况，第3页",
      "year": 2024,
      "entity_scope": "单位全称",
      "headcount_type": "年末实有人数"
    },
    "headcount_scope_match_confirmed": true,
    "headcount_scope_match_note": "人数来源法人名称、年度和单位范围与决算一致"
  }
}
```

Use `public_welfare_i` or `enterprise_managed` for the other headcount routes. Replace every placeholder with the real official source. All calculator amount fields are normalized to `万元`.

For route C or the no-headcount fallback:

```json
{
  "mode": "structure",
  "basic_wage_wanyuan": 100,
  "bonus_performance_allowance_wanyuan": [150, 200, 50],
  "ratio_wage_denominator_wanyuan": 500,
  "housing_fund_wanyuan": 60,
  "occupational_annuity_wanyuan": 40,
  "provenance": {
    "entity_name": "单位全称",
    "route_basis": "未取得同口径人数；按作者的工资结构路线计算",
    "report_year": 2024,
    "basis": "决算",
    "input_amount_unit": "元",
    "normalized_amount_unit": "万元",
    "unit_conversion": "原表金额除以10000",
    "amount_scope_match_confirmed": true,
    "amount_scope_match_note": "决算封面和表内单位名称均为该单位本级",
    "amount_source": {
      "title": "单位全称2024年度单位决算",
      "url": "https://official.example/report.pdf",
      "publisher": "发布机关全称",
      "publication_date": "2025-08-20",
      "retrieved_date": "2026-09-16",
      "locator": "公开06表，第12页，30101/30102/30103/30107栏",
      "year": 2024,
      "entity_scope": "单位全称"
    }
  }
}
```

The CLI rejects missing provenance, mismatched years, unrecorded unit conversion, and amount or headcount scopes that have not been explicitly reconciled. Only include a numeric field when its source and scope have been verified.
