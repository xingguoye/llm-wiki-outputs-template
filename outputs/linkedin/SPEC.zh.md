<!-- translation: zh · canonical: outputs/linkedin/SPEC.md · synced: 2026-11-14 -->

# SPEC：LinkedIn 档案

只针对 LinkedIn 这个去处的规则。此处不含事实——每个事实都经第 5 节的映射从 `wiki/` 来。

## 1. 受众与目标

- 读者：招聘者（常常非技术、在扫关键词）与用人经理（按经历顺序读）。
- 10 秒内的决定：进短名单还是跳过，依据是 Headline + About 的前两行 + 当前职位。
- 优化目标：关键词可读、时间线无歧义、不做会在面试中崩掉的夸大。

## 2. 结构

固定顺序。每个语言变体都用同一顺序。

| # | 字段 | 写什么 |
|---|---|---|
| 1 | Headline | 角色 + 技术栈 + 一个差异点。不要放你辩护不了的形容词。 |
| 2 | About | 3–4 段：定位 → 年限与技术栈 → 客户/项目 → 语言 |
| 3 | Experience | 每个职位页一条；organization 字段 = 法律雇主 |
| 4 | Projects | 个人或值得一说的项目，各一条 |
| 5 | Education | 学位与校区所在地 |
| 6 | Languages | 自评，按第 6 节映射到平台下拉档位 |
| 7 | Skills | wiki 里的完整技能列表，排序见第 3 节 |
| 8 | Certifications | 证书、颁发机构、日期 |

避免绝大多数混乱的规则：**Experience 的 "Organization" 是法律雇主，绝不是终端客户。** 客户与项目写进描述，或写成嵌套的项目条目。把客户填进 organization 字段等于伪造工作履历。

## 3. 硬上限

| 字段 | 平台上限 | 最近实测 |
|---|---|---|
| Headline | 220 字符 | <measure> |
| About | 2,600 字符 | <measure> |
| Experience 描述 | 2,000 字符 | <measure> |
| Projects 描述（每块） | 2,000 字符 | <measure> |
| Skills | 50 项 | <measure> |
| 自定义 URL | – | – |

实测值属于 `state.md`，不属于这里：上限是公开信息，你的文案不是。

**Skills 排序。** 前三个技能是展示最频繁的；按目标职位来定，不要按列表长度。其余保持 wiki 的规范顺序，这样重贴一次的结果是确定的。

描述超过 2,000 字符时的**裁剪优先级**：

1. 砍掉逐工具的配置细节（推理链、设置项、硬件清单）。
2. 把硬件/基础设施清单压缩成一个从句。
3. 缩短方法论叙述——最后手段，它的信息量最大。

## 4. 语言版本

- 一个主语言，与你找工作的地点匹配。
- 次要版本是**这份规格的变体**，不是独立的规格：同结构、同事实，只有措辞变。
- 跨语言规则：任何陈述资历、年限或范围的句子，在每个变体里必须读起来完全一致。在 `state.md` 里留一行"同步锚点"——那句必须一致的句子——因为译者最先在这里漂。

## 5. 事实映射

| 字段 | 取自 |
|---|---|
| Headline、About（年限、定位） | `wiki/entities/person-*` |
| Experience 的时间线与办公形式 | `wiki/entities/employer-*`（拥有时间段） + `wiki/entities/position-*` |
| 职责、客户归属 | `wiki/entities/position-*`、`wiki/entities/client-*` |
| 技能与排除项 | `wiki/concepts/skill-*` |
| Projects | `wiki/entities/project-*` |
| Education、校区 | `wiki/entities/education-*` |
| 语言、证书 | `wiki/entities/person-*` |
| 关于"不要声称什么"的裁定 | `wiki/synthesis/decisions-*` |

## 6. 命名

- 职位名：用雇主使用的原名，用档案所在语言呈现；雇主原名非该语言时附上该语言的写法。在职位页里为每个职位维护两列对照表，而不是每次临时翻译。
- 语言下拉映射：自评 → 平台档位。在这里一次性固定映射（例如工作语言用 "professional working proficiency"，只有母语才用 "native or bilingual"），这样每次发布都不必再争一遍。

## 7. 禁写项

| 永不写 | 因为 |
|---|---|
| 记录支撑不了的资历词（"senior"、"lead"、"expert"） | 面试官最先检验这些；不匹配比缺这个词更糟 |
| 把客户当作雇主 | 伪造时间线；一点就露 |
| 把课程级技术当作职业经验 | 无法核实，且很快被戳穿 |
| 暗示并行雇主的重叠日期 | "先后接续、并非同时"值得在描述里明说 |
| 你无法溯源的指标 | 档案里的任何数字，面试时都会被追问 |

## 8. 验收清单

- [ ] Headline ≤ 220、About ≤ 2,600、每段描述 ≤ 2,000——已实测
- [ ] 每条记录的 organization 字段 = 法律雇主
- [ ] 每条记录的日期与 `wiki/entities/employer-*` 完全一致
- [ ] About 里的总年限与人物页一致（单一事实出处）
- [ ] Skills ≤ 50 且与 wiki 列表完全一致
- [ ] 逐条走过禁写项
- [ ] 语言变体：资历/年限相关的句子完全一致

## 9. 发布流程

1. 草稿写进 `outputs/linkedin/drafts/<YYYY-MM>/`——每种语言一个文件，外加一个可直接粘贴的块文件。
2. 用脚本量长度；改草稿，永不改 wiki（若事实是错的，适用铁律 4）。
3. 粘贴后对着草稿重读线上页面（平台会重排）。
4. 更新 `state.md`（版本、日期、实测值、偏差）与 `wiki/log.md`。
