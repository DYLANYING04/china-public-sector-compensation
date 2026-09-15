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
- `"单位全称" 公开招聘 工资 薪酬 公积金`
- `"单位全称" 小红书 OR 知乎 OR 微博 待遇`
- `site:official-domain "单位全称" filetype:pdf`
- `site:official-domain "单位全称" filetype:xls OR filetype:xlsx`

Repeat for the newest final-account year and at least two preceding years when available. Search by report title and attachment filename if a page exists but its file is not indexed.

## Attachment Handling

- Open HTML attachments rather than relying on page summaries.
- Download official PDFs or spreadsheets when inspection tools require a local file.
- Use OCR for image-only reports and verify extracted digits against the page image.
- Inspect table headers for `金额单位` and footnotes for scope.
- Record the direct report URL and the landing-page URL when both exist.
- If a portal requires a CAPTCHA or login, record the access barrier and continue through the unit, supervisor, finance, audit, and archived official channels.

## Scope Checklist

Before accepting a number, answer all of these:

- Is this the exact unit or a department-wide consolidation?
- Is it the same legal entity as the requested unit?
- Is the figure a budget, adjusted budget, or final account?
- What fiscal year does it cover?
- Is the amount in yuan, ten-thousand yuan, or hundred-million yuan?
- Does the numerator cover establishment staff, all employees, dispatched labor, retirees, or subordinate units?
- Is the headcount sanctioned establishment, actual year-end staff, average staff, or total employees?
- Are one-off rewards or arrears included?
- Are employer social insurance, provident fund, and occupational annuity included?

## Stopping Rule

The search is complete when:

1. all eight source classes above have been checked where applicable;
2. all relevant query families have been tried for the current name and known aliases;
3. the newest usable final account and available adjacent years have been inspected;
4. report attachments and footnotes have been opened;
5. remaining missing fields and blocked channels are recorded.

If the matched wage amount or the required staff count remains unavailable, state `搜不到` for that field and use the expert fallback route when possible.
