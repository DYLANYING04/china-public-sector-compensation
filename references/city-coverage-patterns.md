# City Coverage Patterns

This reference records source-discovery patterns validated across representative cities as of 2026-09-16. Market labels such as first-, second-, and third-tier are not official classifications; use them only to diversify testing. The operational distinction is portal architecture, not city tier.

## Portal Archetypes

### 1. Centralized City Fiscal Index

The city portal lists departments and individual units by fiscal year. Start here because it can expose many units that search engines do not rank.

- Beijing municipal final accounts: `https://www.beijing.gov.cn/gongkai/zdlyxxgk/czsj/sjbmjs/index.html`
- Yantai 2024 final-account index: `https://www.yantai.gov.cn/col/col119690/index.html`

Search the page for the exact unit, then distinguish `部门决算`, `本级`, and subordinate-unit records.

### 2. Supervising Department Batch Page

The supervising department publishes one landing page containing attachments for all subordinate units. Search for the supervisor plus `所属单位决算` when the exact unit query fails.

- Nanjing Culture and Tourism Bureau subordinate-unit disclosures: `https://wlj.nanjing.gov.cn/njswhgdxwcbj/202511/t20251119_5693067.html`
- Shantou Culture, Radio, Television, Tourism and Sports Bureau batch page: `https://www.shantou.gov.cn/wgxj/zwgk/czyjs/content/post_2478885.html`
- Wuhan Education Bureau subordinate-unit page: `https://jyj.wuhan.gov.cn/zfxxgk/fdzdgknr/czzj/bmyjsjsgjf/202510/t20251010_2657362.shtml`

Batch pages are especially productive for museums, libraries, schools, research institutes, service centers, and cultural institutions.

### 3. Unit or Supervisor Disclosure Column

The unit or its supervisor maintains a `财政信息`, `预算/决算`, `预决算公开`, or `通知公告` column.

- Beijing Investment Promotion Service Center: `https://invest.beijing.gov.cn/zwgk/zfxxgk/zfxxgkpt/fdzdgknr/ysjs/`
- Wuhan Science and Technology Museum: `https://www.whstm.org.cn/shownews/list/24`
- Xi'an Science and Technology Bureau fiscal-information column: `https://xakj.xa.gov.cn/zwgk/czxx/3.html`
- Hefei Science and Technology Museum disclosure column: `https://www.hfstm.com/yjsgk/49594.jhtml`

The landing page may expose attachments that generic search cannot parse.

### 4. Direct PDF on the Government Portal

Shanghai and many other regions publish the complete disclosure as a directly indexed PDF. Search the exact unit and year, then jump to `公开06表`.

- Shanghai Science and Technology Museum 2024 final account: `https://www.shanghai.gov.cn/cmsres/ea/ea695b7c065440238fe25efd6b709788/fb0d22a1e0464b37235842dd734cfba9.pdf`
- Shenzhen Public Employment Service Center 2024 final account: `https://hrss.sz.gov.cn/attachment/1/1635/1635145/12439767.pdf`
- Guangzhou Museum 2024 final account: `https://wglj.gz.gov.cn/attachment/7/7906/7906693/10481198.pdf`

### 5. Government Disclosure System or Object Storage

The landing page and the attachment may live on different official infrastructure. Verify the link relationship before accepting a bare object URL.

- Zibo government-disclosure documents use department-specific `zibo.gov.cn` paths.
- Hangzhou/Zhejiang attachments may use the official `zjjcmspublic...zj.gov.cn` object host.
- Luoyang attachments may use `oss.ly.gov.cn`.

Preserve both the landing page and attachment URL in citations.

## High-Yield Query Escalation

Use this order for an exact unit:

1. `"单位全称" "2024年度单位决算"`
2. `"单位全称" "2024年度部门决算"`
3. `"单位全称" "公开06表"`
4. `"主管部门" "2024年度所属单位决算"`
5. `"城市" "2024年市级部门决算公开"`
6. repeat for the prior year and current official name aliases;
7. search the official site's internal disclosure column and inspect attachment links.

Do not require the title to say `单位决算`. Guangdong examples may label an individual unit document `部门决算`, while its internal tables identify one exact unit.

## Personnel Search Lessons

- Beijing unit narratives sometimes state `事业编制17人，实际16人` directly under `人员编制及实有情况`.
- Shenzhen performance self-evaluations can disclose `核定事业编制数`, `年末实有人数`, and `财政供养人员控制率` even when the final account omits headcount.
- Older or district budget narratives often contain `机构编制及交通工具情况` with staff types separated.
- Standard final-account tables in Shanghai, Shenzhen, Guangzhou, Wuhan, Yantai, and Zibo commonly omit headcount even though they disclose the full wage structure.

Therefore search for headcount independently, but calculate the structure multiple from `公开06表` as soon as it is available.

## Attachment Lessons

- Beijing may publish the final-account tables as XLSX and performance files as ZIP. Preview failure is not absence; download and parse by file type.
- Some PDF hosts time out in browser extraction but work by direct download from the official landing page.
- Search engines may surface scraped or deceptive copies of an official page. Prefer the government landing page and its own attachment.
- PDF metadata or extracted titles can be generic or misleading. Verify the internal unit name, fiscal year, table name, and amount unit.

## Edge-Case Patterns

### County and Remote-Area Media Units

Small counties may publish a long department index with hundreds of image-like attachment links. An exact unit can still have a usable `公开06表`, but the department report may consolidate the center and subordinate transmitters. For example, the 2024 Mohe Media Center decision includes the center plus two secondary budget units, while an older center-only budget states a different scope and headcount. Never divide the consolidated 2024 amount by the older center-only headcount.

### Special Administrative Zones

Development zones and special agricultural or high-tech zones often publish through a zone-wide legal-disclosure index rather than a normal city or county finance portal. Yangling's 2024 index leads to a unit landing page with both a PDF narrative and an XLSX table. Browser preview can fail on both formats even though direct downloads are valid; retain the landing page and parse the files locally.

### Central Vertical Systems

Central subordinate institutions may be enumerated on a ministry or bureau batch page while each unit's own subdomain hosts the report. The China Geological Survey batch page lists dozens of exact units, including Xi'an, Shenyang, Mudanjiang, and Urumqi centers. A 502, timeout, or inaccessible subdomain is an access barrier to record, not proof that the unit has no report. Continue through the batch page, direct attachment URL, archived search result, and adjacent-year official pages before reporting `搜不到`.

### Province-Specific JavaScript Disclosure Portals

Some provincial finance platforms expose a normal HTML announcement but send the actual unit report to a JavaScript-only budget application. Hubei's culture-and-tourism page links the Hubei Finance platform for exact unit decision directories, including the Hubei Academy of Fine Arts. Treat the JavaScript portal as a distinct transport route: inspect the linked page in a browser-capable tool or recover its API/attachment links; do not replace the unit with the supervising department's consolidated report.

## Coverage Outcome

Forward testing across Beijing, Shanghai, Shenzhen, Guangzhou, Nanjing, Wuhan, Hangzhou, Xi'an, Hefei, Yantai, Zibo, Shantou, and Luoyang found a usable exact-unit wage breakdown in most tested cases. Matched current-year headcount was much less consistently public. The robust default is therefore:

1. deliver a final-account structure judgment when `公开06表` is found;
2. continue the personnel cascade for a full per-person calculation;
3. use a budget estimate only when no final account is available;
4. state `搜不到` only after portal, supervisor, unit, attachment, registration, performance, and adjacent-year checks are logged.

5. For a department that lists subordinate units, read the report's `部门决算编制范围` and `部门人员情况` before choosing a denominator. A prior-year or center-only personnel figure is not a matched denominator.
