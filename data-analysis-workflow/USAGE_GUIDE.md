# Data Analysis Workflow - Quick Start Guide

## 已创建的技能概述

这个技能已成功创建，用于规范化数据分析工作流程，自动记录所有操作、决策和结果。

## 技能结构

```
data-analysis-workflow/
├── SKILL.md                          # 完整的技能文档
├── scripts/
│   ├── log_helper.py                 # AnalysisLogger类（核心功能）
│   ├── init_project.py               # 项目初始化脚本
│   └── summarize_analysis.py         # 分析总结生成脚本
├── references/
│   └── log_formats.md                # 详细的日志格式规范
└── assets/                           # （保留为空，未来可扩展）
```

## 快速开始

### 1. 创建新项目

```bash
cd ~/work
python ~/.claude/skills/data-analysis-workflow/scripts/init_project.py my_analysis_project
cd my_analysis_project
```

这会创建标准目录结构：
- `00_raw_data/` - 原始数据（只读）
- `01_analysis/` - 分析脚本和日志
- `02_processed_data/` - 处理后的数据
- `03_results/` - 结果（图表、表格、统计）
- `04_reports/` - 报告和手稿
- `05_models/` - 训练的模型
- `logs/` - 集中化日志（MASTER_LOG.md）

### 2. 在分析中使用AnalysisLogger

```python
import sys
from pathlib import Path

# 导入AnalysisLogger
sys.path.insert(0, str(Path.home() / '.claude/skills/data-analysis-workflow/scripts'))
from log_helper import AnalysisLogger

# 初始化logger
logger = AnalysisLogger(project_root=".")

# 记录操作
logger.log_operation(
    operation="数据清洗",
    location="02_processed_data/20260228_cleaned_data.csv",
    operation_type="Data Processing",
    params={"method": "remove_outliers", "threshold": 3},
    result="删除了47个异常值（占总数的2.3%）",
    key_findings=["大多数异常值出现在年龄列", "清洗后数据呈正态分布"],
    notes="使用IQR方法进行清洗"
)

# 记录分析决策
logger.log_decision(
    question="应该使用哪种统计检验来比较组别？",
    decision="使用Welch's t检验而非标准t检验",
    reasoning="检测到方差不齐（Levene p=0.003）",
    references=["统计学教材第234页"]
)

# 创建分析会话
analysis_dir = logger.create_analysis_log(
    analysis_name="差异表达分析",
    input_data=["00_raw_data/counts_matrix.csv"],
    methods=["DESeq2归一化", "负二项GLM", "FDR校正"],
    results={"显著基因数": 423, "上调": 256, "下调": 167},
    next_steps=["通路富集分析", "验证前20个基因"],
    analyst="张三"
)
```

### 3. 生成项目总结

```bash
python ~/.claude/skills/data-analysis-workflow/scripts/summarize_analysis.py
```

这会生成 `ANALYSIS_SUMMARY.md`，包含：
- 操作时间线
- 操作类型统计
- 关键发现汇总
- 输出文件清单
- 待办事项列表

## 核心功能

### AnalysisLogger类方法

1. **log_operation()** - 记录数据处理、分析、建模等操作
2. **log_decision()** - 记录分析决策及其依据
3. **log_error()** - 记录错误及其解决方案
4. **create_analysis_log()** - 创建带时间戳的分析目录和日志

### 辅助脚本

1. **init_project.py** - 初始化项目目录结构
2. **summarize_analysis.py** - 生成项目总结报告
3. **log_helper.py** - 提供AnalysisLogger类（可导入使用）

## 日志格式

### MASTER_LOG.md格式
```markdown
### [2026-02-28 14:30:45] 操作名称
**Type:** Data Processing
**Location:** `path/to/file`
**Parameters:**
- param1: value1
**Result:** 简要结果描述
**Key Findings:**
- 发现1
**Notes:** 额外说明
---
```

### analysis_log.md格式
每个分析会话在 `01_analysis/YYYYMMDD_HHMM_名称/` 目录下都有详细的分析日志，包含：
- 目标、输入数据、方法
- 结果、关键发现
- 局限性、下一步计划

详细格式请参考 `references/log_formats.md`

## 与科学写作集成

可以从日志中自动提取方法部分内容用于论文撰写：

```python
from log_helper import extract_methods

methods_text = extract_methods(
    log_path="logs/MASTER_LOG.md",
    start_date="2026-02-01",
    end_date="2026-02-28",
    format="markdown"  # 或 "latex"
)

# 将提取的内容用于手稿的Methods部分
with open("04_reports/methods_draft.md", "w") as f:
    f.write(methods_text)
```

## 最佳实践

1. **立即记录** - 操作完成后立刻记录，不要事后回忆
2. **详细参数** - 记录所有关键参数和设置
3. **量化结果** - 包含具体数字、p值、效应量
4. **记录决策** - 说明为什么选择某种方法而非其他方法
5. **链接输出** - 始终记录生成的图表和表格路径

## 示例工作流

1. **初始化项目** → `init_project.py`
2. **添加原始数据** → `00_raw_data/`
3. **开始分析** → 使用AnalysisLogger记录
4. **保存处理后的数据** → `02_processed_data/YYYYMMDD_*.csv`
5. **生成结果** → `03_results/figures/`, `tables/`
6. **定期总结** → `summarize_analysis.py`
7. **撰写报告** → 提取日志内容到 `04_reports/`

## 技能安装状态

✓ 技能已创建在：`~/.claude/skills/data-analysis-workflow/`
✓ 所有脚本已设置为可执行权限
✓ SKILL.md已完成（14KB，完整文档）
✓ 核心功能脚本已创建（log_helper.py, init_project.py, summarize_analysis.py）
✓ 参考文档已创建（log_formats.md，详细格式规范）

## 下一步

### 立即使用

```bash
# 创建第一个项目
python ~/.claude/skills/data-analysis-workflow/scripts/init_project.py test_project
cd test_project

# 查看生成的结构
ls -la

# 运行示例脚本
python 01_analysis/example_analysis.py
```

### 与Claude交互时使用

在Claude对话中，这个技能会自动可用。当你进行数据分析时，Claude会建议使用这个workflow来组织和记录你的工作。

你可以说：
- "使用data-analysis-workflow创建一个新项目"
- "帮我记录这个数据清洗操作"
- "生成项目分析总结"

## 技术支持

- 完整文档：阅读 `SKILL.md`
- 日志格式：参考 `references/log_formats.md`
- 代码示例：查看 `scripts/init_project.py` 中的项目模板

---

创建时间：2026-02-28
状态：完成 ✓
