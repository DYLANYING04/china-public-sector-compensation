# 中国企事业单位待遇研究

[![Tests](https://github.com/DYLANYING04/china-public-sector-compensation/actions/workflows/tests.yml/badge.svg)](https://github.com/DYLANYING04/china-public-sector-compensation/actions/workflows/tests.yml)
[![MIT License](https://img.shields.io/github/license/DYLANYING04/china-public-sector-compensation)](LICENSE)
[![skills.sh installs](https://skills.sh/b/DYLANYING04/china-public-sector-compensation)](https://skills.sh/DYLANYING04/china-public-sector-compensation)

[English README](README.en.md)

> 输入一个中国企事业单位名称，自动检索官方报告并按专业经验估算待遇；真实数据找不到，就明确说搜不到。

![真实案例预览：杨凌党校 2024 FULL 结果](assets/launch-preview.png)

## 一条命令安装

```bash
npx skills add DYLANYING04/china-public-sector-compensation -g
```

`-g` 会安装为全局 skill。安装器会自动发现仓库根目录的 `SKILL.md`；动态安装量见上方 skills.sh 徽章。手动克隆仅作为备用方式：

```powershell
git clone https://github.com/DYLANYING04/china-public-sector-compensation.git "$env:USERPROFILE\.codex\skills\china-public-sector-compensation"
```

如已安装，请在该目录执行 `git pull` 更新。ChatGPT 支持技能的账号可上传下载并审查后的技能文件夹；不同产品和工作区的可用性可能不同。

## 30 秒看到结果

不需要准备链接、表格、JSON，也不需要判断单位属于哪一类。只发送一句话：

```text
使用 $china-public-sector-compensation，研究“某市公共就业服务中心”的待遇。
```

它会自动完成单位识别、官方来源搜索、附件读取、口径核对和计算。没有年份时，默认查最新已完成且可核验的年度；同名单位确实无法区分时才提问。

结果开头直接给出单位/年度、证据状态和结论或缺失字段；后面提供来源和逐步计算，便于复核。

## 可复核的真实案例

- [杨凌示范区工委党校 2024](cases/yangling-party-school-2024.md)：`FULL`，同年实有人数与工资项目匹配，普通员工年度等效估算为 `11.5424 万元`。
- [北京市投资促进服务中心（本级）2022](cases/beijing-investment-center-2022.md)：`FULL`，复现文章中的 `503 + 1764`、88 人和 `196` 专项奖判断，普通员工年度等效估算为 `17.1823 万元`。
- [南京市佑安医院 2024](cases/nanjing-youan-hospital-2024.md)：`STRUCTURE_ONLY`，展示医院表格中奖金空白且人数不匹配时为何不能硬算。
- [漠河市融媒体中心 2024](cases/mohe-media-center-2024.md)：偏远县级门户，结构倍数 `1.1861`，并拒绝用旧口径人数相除。
- [北京市投资促进服务中心（本级）2024](cases/beijing-investment-center-2024.md)：展示北京单位决算本级与部门人数不匹配时的拒算边界。

首发 [30 家单位 Benchmark](benchmark/README.md) 找到 `28/30` 份可用工资拆分，但只有 `1/30` 达到严格的人均 `FULL` 标准。这是刻意保守的结果：宁可保留 `STRUCTURE_ONLY` 或 `搜不到`，也不做跨范围除法。

## 能做什么

- 解析市级财政索引、主管部门所属单位批量公开页、单位官网栏目和政府附件存储。
- 覆盖直辖市、省会、地级市、县级市、开发区、示范区和中央垂管单位等不同公开架构。
- 处理 PDF、XLSX、ZIP、扫描件，以及附件预览失败、JavaScript 财政平台或对象存储链接。
- 同时搜索工资金额和人数证据，核对单位、年度、预算/决算性质、人员范围和金额单位。
- 数据不足时明确写出 `搜不到`，不使用行业平均数补齐；但会按作者方法对真实报表中已披露的金额作出明确标注的专家判断。

## 作者的计算方法

这些规则是必选方法，不是可选参考。这里的路线是分析方法，不等于单位的官方机构分类：

1. **地方事业单位**：
   `单位可比工资合计 ÷ 匹配人数 = 单位人均`

   普通员工估算：`单位人均 × 2/3`。

2. **符合作者所说领导层拉高均值/企业化特征的单位**：
   `工资总额 ÷ 匹配员工数 = 单位人均`

   普通员工估算：`单位人均 × 1/2`。

3. **混合用工、经营收入较多或人数不可比的单位**：
   `（奖金 + 绩效工资 + 津贴补贴）÷ 基本工资`

   - 大于等于 4：待遇不错
   - 小于 3：待遇较差
   - 3 至小于 4：继续看住房公积金和职业年金比值

4. **有官方公益一类依据且人数可比的单位**：在工资总额和人员范围匹配时，直接计算人均待遇，并说明人数是年末人数、全年平均人数还是其他口径。

**专项奖的作者经验判断**：报表金额必须真实可追溯；但奖项用途不一定由报表直接命名。此时可以像作者判断“`196`估计为招商任务奖”一样，结合单位职责和报表项目结构作出专家判断。报告必须单列“专家判断”、其依据和置信度，不能伪称为报表原话。

金额字段在计算器中统一换算为万元；原始单位、换算过程和来源定位必须一并记录。

`官方机构身份`和`作者方法分析路线`必须分开写。找不到机构编制批复、登记年报、三定规定等官方依据时，写“未查明”，不能根据单位名称或工资结构猜它是公益一类、公益二类或参公单位。

## 证据状态

证据状态与上面的计算路线字母分开：

| 状态 | 含义 |
|---|---|
| `FULL` | 同年度、同范围的决算工资数据和人数均已找到，可计算人均及普通员工估算 |
| `STRUCTURE_ONLY` | 决算工资结构已找到，但没有匹配人数，输出工资结构判断并继续追查人数 |
| `BUDGET_ONLY` | 只有预算数据，结果必须标为预算估算 |
| `NO_USABLE_DATA` | 完成检索清单后仍没有可用工资分解，明确报告 `搜不到` |

## 数据口径底线

- 不把部门汇总金额除以单个下属单位人数。
- 不把旧年度本级人数除以新年度包含下属单位的汇总金额。
- 不把预算、调整预算和决算混在同一个计算式中。
- 不把编制数、实有人数、年末人数和全年平均人数当成同一种分母。
- 不把仅含一般公共预算财政拨款的表格说成单位全部薪酬；高校、医院等尤其要查事业收入或其他资金口径。
- 不把含单位社保、公积金、职业年金的工资福利支出说成个人税后或到手工资。
- 不把表格空白项自动当作零；专项奖可以按作者经验作出专家判断，但必须写清依据、置信度和“非报表明示”。
- 不因搜索结果标题、转载页面或附件预览失败就认定数据不存在。
- 页面能定位附件，但附件内容未核验时，不把数字当作最终证据。

你不需要自己判断“搜不到”还是“待遇较差”：前者表示关键真实数据没有找到，后者表示数据已找到且按作者阈值计算后落在较低区间。

## 研究流程

1. 解析单位全称、别名、地区、主管部门和官方机构身份；将身份与计算路线分开。
2. 按市级索引、主管部门批量页、单位栏目、财政公开平台和附件链接逐层检索。
3. 机构身份、金额和人数三条线并行搜索，优先打开同年度 `公开06表` 或等价工资明细表。
4. 建立证据台账，记录来源标题、直接链接、发布机关、年度、表格位置、原始标签、金额单位、资金范围和人员范围。
5. 按作者方法逐行计算，单列一次性奖励、专项资金及其他不可比项目。
6. 用相邻年度、绩效评价、编制说明和招聘公告交叉检查。
7. 按 [references/output-template.md](references/output-template.md) 输出结论、计算过程、来源口径、搜索记录和缺失字段。

详细规则见：

- [SKILL.md](SKILL.md)：调用入口和总流程
- [references/expert-method.md](references/expert-method.md)：四条计算路线和输入格式
- [references/institution-classification.md](references/institution-classification.md)：官方机构身份与分析路线的分离规则
- [references/source-playbook.md](references/source-playbook.md)：来源优先级、搜索词和附件处理
- [references/city-coverage-patterns.md](references/city-coverage-patterns.md)：不同城市及偏门门户的实测模式
- [references/output-template.md](references/output-template.md)：标准输出结构

## 计算器

对已核验的 JSON 输入运行：

```bash
python scripts/calculate_compensation.py path/to/input.json
```

计算器会强制检查：

- 报告年度和预算/决算性质；
- 原始金额单位、标准化单位和换算说明；
- 来源标题、发布机关、链接、定位和实体范围；
- 金额范围及人数范围是否已明确核对；
- 人数路线是否提供同年度、同范围的人数证据。
- 官方机构身份说明、资金范围、是否含单位缴费和人数分母类型；
- 来源日期格式以及 `301xx` 明细与 `301` 合计的勾稽说明。

缺少这些信息时，程序拒绝计算，而不是静默生成一个看似精确的金额。JSON 字段示例见 [references/expert-method.md](references/expert-method.md)。

## 测试

运行仓库自带测试：

```powershell
$env:PYTHONUTF8='1'
python -m unittest discover -s tests -v
```

GitHub Actions 会在每次推送和拉取请求时自动运行测试。测试包括作者截图中的 `2/3`、`1/2` 和结构倍数阈值，以及北京、上海、深圳、广州、武汉、杭州、西安、合肥、烟台、淄博、陕西、漠河等公开报告案例和来源口径拒算案例。

## 已验证的检索经验

- 市级财政索引适合批量发现单位；主管部门页面适合发现博物馆、图书馆、学校、服务中心等下属单位。
- 县级和偏远地区常把本级与转播台、二级预算单位合并，必须先读 `部门决算编制范围`。
- 开发区、示范区可能使用独立的政府信息公开目录和双附件页面。
- 省级财政平台可能只提供 JavaScript 页面；渲染失败属于访问障碍，不等于 `搜不到`。
- 中央垂管系统常由总局批量列出单位，子站 502 或超时后仍应继续查直链、归档页和相邻年度。
- 官方对象存储链接必须和官方落地页一起保存，不能只引用一个裸文件地址。

## 许可与贡献

本仓库采用 [MIT License](LICENSE)，允许复用、修改和分发。新增案例、规则或门户路径请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，并使用 [请求研究单位](https://github.com/DYLANYING04/china-public-sector-compensation/issues/new?template=request-institution.yml)、[报告数据错误](https://github.com/DYLANYING04/china-public-sector-compensation/issues/new?template=data-correction.yml) 或 [新增地区门户](https://github.com/DYLANYING04/china-public-sector-compensation/issues/new?template=portal-pattern.yml) 表单。
