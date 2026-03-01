---
name: bgi-software-writing
description: 按中国软著“软件设计说明书”规范生成长篇、图文并茂、格式完整的技术文档。先判型（平台型/分析型/工具型）再选文档主干；平台型采用“架构+模块+流程+权限+运维”主线；“输入/输出/执行步骤”仅在适合模块中选择性使用。支持 Markdown 与 DOCX 双输出。
allowed-tools: Read Write Edit Bash
license: Proprietary
---

# BGI Software Writing

## Overview

该技能用于撰写中文软著《软件设计说明书》，目标是输出可直接用于登记材料整理的长篇技术文档。

核心原则：
- 主干必须由软件实际功能决定，不允许套用单一固定模板。
- 先判型再写作：平台型、分析型、工具型分别使用不同章节框架。
- 图文并茂：流程图、文本图、图表编号、图注规则必须完整。
- 保证格式：标题层级、目录、图表编号、附录结构一致。

## When to Use

在以下场景触发本技能：
- 用户要求撰写软著《软件设计说明书》。
- 用户要求“按软著风格”“篇幅长”“图文并茂”“格式规范”。
- 用户给出软件功能，希望自动组织章节主干并生成完整技术文档。

不适用场景：
- 营销文案、产品宣传页。
- 学术论文投稿（可转用 scientific-writing 等技能）。

## Required Workflow (Mandatory)

### Step 1: 类型确认（先问一句）

当用户没有明确说明软件类型时，必须先问：

`本次软著是平台型、分析型还是工具型？`

只有在用户回答后，或信息足够明确时，才进入下一步。

### Step 2: 主干预览（先给结构，不直接长文）

在正式撰写前，先输出“拟采用文档主干预览”，包括：
- 选定的软件类型
- 一级章节列表
- 每章拟覆盖的关键内容

### Step 3: 全文生成

按已确认主干生成长篇正文，满足：
- 章节完整
- 图文并茂
- 编号与格式一致
- 语体正式、术语稳定

## Type Decision and Fallback Rules

若用户未回复类型，允许按关键词回退判型：

- 平台型关键词：`用户管理` `权限` `工作流` `看板` `配置中心` `审计` `部署` `多角色` `运维`
- 分析型关键词：`差异分析` `建模` `归一化` `聚类` `统计检验` `可视化结果` `特征筛选`
- 工具型关键词：`导入导出` `批处理` `转换` `清洗` `脚本执行` `命令行`

冲突处理：
- 若多个类型高强度同时命中，优先再次询问用户；
- 在未确认前，不进入正文生成。

详细决策树见：`references/skeleton-decision-tree.md`

## Document Skeleton Selection

根据类型加载对应模板：
- 平台型：`references/template-platform.md`
- 分析型：`references/template-analysis.md`
- 工具型：`references/template-tool.md`

### 关键约束：输入/输出/执行步骤的使用

- 分析链路、算法链路、数据处理链路：使用 `输入/输出/执行步骤`。
- 平台管理模块（用户、权限、配置、审计等）：使用
  `角色` + `触发条件` + `业务流程` + `状态变更` + `结果产物`。
- 不允许全篇机械套用“输入/输出/执行步骤”。

## Length and Detail Requirements

默认篇幅目标：
- 中文字符：20,000–35,000（可按用户要求上调）。

最小内容密度：
- 每个一级章节至少 3 段有效技术叙述。
- 每个核心子模块至少包含：
  - 设计目标
  - 业务或技术逻辑
  - 边界条件/异常处理

扩写策略见：`references/length-control-and-expansion.md`

## Figure and Table Requirements

最低图文要求：
- 平台型：每个一级功能域至少 1 幅流程图/文本图。
- 分析型：每个核心分析模块至少 1 幅图。
- 全文图表编号连续：`图1...图N`、`表1...表M`。

图表与图注规则见：`references/figure-table-playbook.md`

可复用图块见：`assets/diagram-snippets.md`

## Formatting Requirements

必须遵循：
- 标题层级：Heading 1 / Heading 2 / Heading 3
- 正文：Normal
- 图注：Caption（图/表编号+标题）
- 目录与正文层级一致
- 术语命名前后一致

风格规则见：`references/style-guide-zh-softcopyright.md`

## Output Contract

默认双输出：
1. Markdown 主稿（结构化、可审阅）
2. DOCX 交付稿（格式化最终稿）

推荐流程：
- 先生成 Markdown：使用 `assets/software-design-spec-template.md` 为骨架。
- 再转写 DOCX：保持标题层级、图注、目录、编号一致。

若用户明确只要一种格式，可按要求输出单格式。

## Quality Gate (Before Final Delivery)

交付前必须做自检：
- 类型与主干是否匹配
- 章节是否完整、无空章
- 图表编号是否连续
- 输入输出步骤是否只在适合模块出现
- 术语、缩略语、命名是否一致
- Markdown 与 DOCX 版本结构是否一致

详细检查清单见：`references/quality-checklist.md`
