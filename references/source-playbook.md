# Source and Search Playbook

Use this checklist for every unit. Prefer the newest completed fiscal year, then inspect the prior two years for continuity.

## Source Order

1. Target unit's official website and government-information-disclosure pages.
2. Supervising department's budget/final-account and subordinate-unit disclosure pages.
3. Central Ministry of Finance department budget/final-account portal or the relevant provincial/municipal finance disclosure portal.
4. Public-institution registration and annual-report disclosure systems.
5. Official establishment, institutional-functions, and staffing disclosures.
6. Official audit reports, inspection整改 reports, performance evaluations, government annual reports, and recruitment announcements.
7. Official statistical yearbooks or government open-data portals.
8. News, job sites, forums, social platforms, and employee disclosures for additional leads and consistency checks.

Use multiple discovery routes when ordinary web search misses an attachment: general search engines, official-site internal search, government disclosure indexes, direct filename search, browser-rendered pages, attachment-link inspection, and available platform-specific search tools. Search WeChat public articles, Xiaohongshu, Zhihu, Weibo, job forums, and employee discussions for report titles, former names, staffing clues, and corroboration, then trace important figures back to the strongest available document.

Useful official entry points include:

- Central department budget/final accounts: `https://www.mof.gov.cn/zyyjsgkpt/zybmyjs/`
- Beijing municipal final accounts: `https://www.beijing.gov.cn/gongkai/zdlyxxgk/czsj/sjbmjs/index.html`
- Central institution registration platform: `https://gjsy.scopsr.gov.cn/`
- Legacy `事业单位在线` entry used by registration notices: `http://gjsy.gov.cn/`

Do not assume these two portals cover every target. Find the equivalent finance and disclosure portals for the unit's jurisdiction.

For city-specific portal layouts and verified examples from different city sizes, read [city-coverage-patterns.md](city-coverage-patterns.md).

## Three Parallel Tracks

Start all tracks immediately:

### Identity Track

1. Find the current official institutional-functions page, `三定` provisions, establishment approval, legal-person registration, or classification decision.
2. Record the official wording and source without inferring `公益一类/二类`, `参公`, or enterprise-style status from the name.
3. Check for mergers, renaming, supervision transfers, and reforms between the identity source year and the compensation report year.
4. Keep `官方机构身份` separate from the expert analysis route under [institution-classification.md](institution-classification.md).

### Amount Track

1. Find the exact unit's newest final account.
2. Open `一般公共预算财政拨款基本支出决算明细表`, commonly `公开06表`.
3. Extract `30101 基本工资`, `30102 津贴补贴`, `30103 奖金`, `30107 绩效工资`, `30109 职业年金缴费`, `30113 住房公积金`, `30199 其他工资福利支出`, and total `301 工资福利支出`.
4. Preserve each row's name. Do not convert a blank or unreadable cell to zero unless the table legend expressly says blanks mean zero.
5. Reconcile the available `301xx` detail to the `301` total when the complete table is present; explain any difference beyond rounding.
6. Record whether the table covers `一般公共预算财政拨款基本支出`, another fiscal funding scope, or the institution's full payroll. For universities, hospitals, and operating institutions, a fiscal-appropriation table may omit compensation funded by service or operating income.
7. If only a budget is available, use the equivalent basic-expenditure budget table and mark every result as budget-based.

### Headcount Track

Search in this order:

1. the same-year unit final-account narrative for `人员编制及实有情况`;
2. the same-year unit budget narrative for `机构编制及交通工具情况`, `编制数`, or `实有人数`;
3. same-year department or unit overall-performance/self-evaluation reports for `人员管理情况` and `财政供养人员控制率`;
4. national or local institution-registration annual reports for `人员总数`;
5. same-year official annual reports, audit reports, institutional profiles, and recruitment materials;
6. adjacent-year official staff figures only as a continuity check, never as a same-year denominator unless an official source establishes comparability.

If a matching headcount is still unavailable, keep the case in evidence state `STRUCTURE_ONLY` and deliver the author's structure analysis.

Rank denominator quality in the final report:

1. annual-average actual staff for the same payroll scope;
2. year-end actual staff;
3. actual staff at an unspecified date or registered annual-report total;
4. sanctioned establishment count.

Lower-ranked denominators are still usable under the author's method when the scope is supported, but must carry a caveat. If two credible denominators exist, show the sensitivity range rather than silently choosing the more favorable result.

## Query Families

Run queries with the full name, current alias, former name, and supervising department where applicable:

- `"单位全称" 年度 决算`
- `"单位全称" 年度 单位决算`
- `"单位全称" 年度 部门决算`
- `"单位全称" 年度 预算`
- `"单位全称" 工资福利支出`
- `"单位全称" 基本工资 绩效工资 津贴补贴`
- `"单位全称" 住房公积金 职业年金`
- `"单位全称" 编制 人数`
- `"单位全称" 在职人数 实有人数 年末人数`
- `"单位全称" 事业单位法人 年度报告`
- `"单位全称" 审计 报告`
- `"单位全称" 招聘 待遇`
- `"单位全称" 年报 人员总数`
- `"单位全称" "人员编制及实有情况"`
- `"单位全称" "机构编制及交通工具情况"`
- `"单位全称" "人员管理情况" "财政供养人员控制率"`
- `"单位全称" 公开招聘 工资 薪酬 公积金`
- `"单位全称" 小红书 OR 知乎 OR 微博 待遇`
- `"主管部门全称" 年度 所属单位决算`
- `"城市名" 年度 市级部门决算公开`
- `"开发区/示范区全称" 年度 部门决算`
- `"单位全称" "单位决算信息公开目录"`
- `"单位全称" "事业单位法人年度报告"`
- `"单位全称" "公开06表"`
- `site:official-domain "单位全称" filetype:pdf`
- `site:official-domain "单位全称" filetype:xls OR filetype:xlsx`

Repeat for the newest final-account year and at least two preceding years when available. Search by report title and attachment filename if a page exists but its file is not indexed.

## Attachment Handling

- Open HTML attachments rather than relying on page summaries.
- Extract the attachment URL from the official landing page. A failed preview is not evidence that the attachment is absent.
- Download official PDFs, spreadsheets, or archives when inspection tools require a local file.
- For XLSX, inspect sheet names and locate `GK06`, `公开06表`, or the basic-expenditure sheet with a spreadsheet parser.
- For ZIP, list entries first, then inspect only relevant PDF, DOCX, XLSX, or image files. Preserve the archive and landing-page URL in the evidence ledger.
- For government object-storage or CDN links, retain the official landing page that links to the object. A bare object URL alone may not prove publisher identity.
- Use OCR for image-only reports and verify extracted digits against the page image.
- Inspect table headers for `金额单位` and footnotes for scope.
- Record the direct report URL and the landing-page URL when both exist.
- If a portal requires a CAPTCHA or login, record the access barrier and continue through the unit, supervisor, finance, audit, and archived official channels.
- If a linked provincial or zone finance portal is JavaScript-only, record the landing page and use a browser-capable tool or recover the underlying API/attachment URLs. A JavaScript rendering failure is an access barrier, not `搜不到`.
- Reject search-result clones and scraped copies when the same document exists on an official government or unit domain. Domain appearance and page title are not enough; verify the publisher, site identity, and attachment origin.

## Scope Checklist

Before accepting a number, answer all of these:

- Is this the exact unit or a department-wide consolidation?
- Is it the same legal entity as the requested unit?
- Is the figure a budget, adjusted budget, or final account?
- What fiscal year does it cover?
- Does the report explicitly include subordinate or secondary budget units?
- Is the amount in yuan, ten-thousand yuan, or hundred-million yuan?
- Does the amount cover only fiscal appropriations or all payroll funding sources?
- Does the numerator cover establishment staff, all employees, dispatched labor, retirees, or subordinate units?
- Is the headcount sanctioned establishment, actual year-end staff, average staff, or total employees?
- Are one-off rewards or arrears included?
- Are employer social insurance, provident fund, and occupational annuity included?
- Is an alleged special award explicitly identified by a source, rather than inferred from its size?
- Do blank cells mean zero under the table legend, or are they missing/unreadable?

Do not infer scope from the filename alone. Some cities call an individual institution's disclosure `部门决算`; inspect the internal `单位名称`, organization description, and table headers.

## Stopping Rule

The search is complete when:

1. all eight source classes above have been checked where applicable;
2. all relevant query families have been tried for the current name and known aliases;
3. the newest usable final account and available adjacent years have been inspected;
4. report attachments and footnotes have been opened;
5. remaining missing fields and blocked channels are recorded.

If the matched wage amount or the required staff count remains unavailable, state `搜不到` for that field and use the expert fallback route when possible. Attach one or more cause codes: `NOT_DISCLOSED`, `NOT_FOUND_AFTER_CHECKLIST`, `ACCESS_BLOCKED`, `SCOPE_MISMATCH`, or `YEAR_MISMATCH`.
