# 南京市佑安医院 2024

**Quick result:** `STRUCTURE_ONLY`. The official report supports a hospital wage-structure review, but it does **not** support a per-person estimate: no matched headcount was retained, and the bonus cell is blank without a legend defining blank as zero.

## Source Facts

The [official 2024 final-account PDF](https://mzj.nanjing.gov.cn/njsmzj/njsmzj/202510/P020251014625305200009.pdf) identifies the unit and shows `公开06表` on page 18. The same table gives:

| Item | Value |
|---|---:|
| 基本工资 | 2,031.97 万元 |
| 津贴补贴 | 2,687.93 万元 |
| 绩效工资 | 3,322.75 万元 |
| 奖金 | blank |
| 住房公积金 | 1,120.39 万元 |
| 职业年金缴费 | 485.42 万元 |

## What the Skill Does

```text
已披露的可变项目下限 = 2,687.93 + 3,322.75 = 6,010.68 万元
已披露部分 / 基本工资 = 6,010.68 / 2,031.97 = 2.9581
```

This is a lower bound, not the article's final structure multiple: `奖金` is blank and the table does not establish that blank means zero. The skill therefore reports the missing item and keeps the conclusion at `STRUCTURE_ONLY`; it does not label the hospital "待遇较差" and it does not divide by an unsupported headcount.

## Why This Case Matters

Hospitals may have multiple compensation funding streams. The cited table is a fiscal basic-expenditure table, not proof of the hospital's complete payroll. The case shows why transparent withholding is a successful outcome rather than a failure of the tool.
