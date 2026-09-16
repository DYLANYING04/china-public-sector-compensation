# Output Template

Use concise Chinese. Preserve this information structure, while adapting headings to the case.

## 快速结论

Put this block before all tables and detail:

```text
单位/年度：
检索截至：YYYY-MM-DD
证据状态：FULL / STRUCTURE_ONLY / BUDGET_ONLY / NO_USABLE_DATA
结论：作者方法下年度/月度等效估算，或搜不到原因
```

If the result is incomplete, name the exact missing field in the conclusion line. Do not make the reader search the calculation section to learn whether the amount is a final account, a budget estimate, or a structure-only judgment.

## 结论

- 单位：full official name
- 采用年度：year
- 官方机构身份：sourced official wording, or `未查明（不得推断）`
- 作者方法分析路线：A/B/C/D and evidence reason
- 证据状态：`FULL` / `STRUCTURE_ONLY` / `BUDGET_ONLY` / `NO_USABLE_DATA`, and why
- 结果含义：财政工资福利支出/全口径工资总额/预算估算；是否包含单位缴费
- 作者方法下普通员工年度/月度等效估算：annual and monthly result, or `搜不到，无法按该方法计算`
- 单位人均值：annual and monthly result when available
- 工资结构判断：ratio and expert interpretation when route C or fallback applies

Never label the result `到手工资` or `税后工资` unless the source directly establishes that meaning.

## 一步一步计算

Show every source input and arithmetic step. Example:

```text
工资项目合计 = A + B + C = X 万元
匹配人数 = N 人
单位人均 = X / N = Y 万元/人/年
普通员工估算 = Y x 2/3 = Z 万元/年
月均 = Z / 12 = M 万元/月
```

For route D, use `x 1/2`. For route C, show the exact structure numerator before dividing by basic wage.

## 数据来源与口径

| 数据项 | 原始数值 | 年度 | 口径 | 来源与定位 |
|---|---:|---:|---|---|
| 工资福利或组成项 | | | 决算/预算；单位本级/部门汇总 | direct link, page/table/row |
| 人员数 | | | 编制/实有/年末/全年平均 | direct link, page/section |
| 公积金/职业年金 | | | | direct link, page/table/row |

State explicitly whether the numerator and denominator match. Name the funding scope, employer-paid contribution treatment, denominator basis and quality, and `301xx`-to-`301` reconciliation status. Explain any adjustment for awards, subordinate units, non-establishment staff, or amount units. A special award may be excluded only when a source identifies it as special or one-off.

## 作者经验判断

State the applied rule without replacing it:

- local ordinary staff: `单位人均 x 2/3`;
- leadership-skew/enterprise-style ordinary staff: `单位人均 x 1/2`;
- structure route: apply the author's `>= 4`, `< 3`, and intermediate thresholds.

## 搜索记录

Use a compact log:

| 渠道/查询 | 结果 | 是否采用 | 原因 |
|---|---|---|---|
| 市级财政索引 | | | |
| 主管部门所属单位页面 | | | |
| 单位官网及附件 | | | |
| 编制/登记年报/绩效报告 | | | |
| 补充渠道 | | | |

Mention inaccessible pages, missing attachments, preview failures, downloaded XLSX/ZIP files, and name aliases tried.

## 未找到的数据

List only genuinely missing or incompatible fields. Use `搜不到` plainly. Add one or more reason codes: `NOT_DISCLOSED`, `NOT_FOUND_AFTER_CHECKLIST`, `ACCESS_BLOCKED`, `SCOPE_MISMATCH`, or `YEAR_MISMATCH`. Do not replace them with invented figures.
