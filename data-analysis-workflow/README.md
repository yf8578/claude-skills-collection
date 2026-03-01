# Data Analysis Workflow

A structured data analysis workflow skill for Claude that provides automatic logging, standardized project organization, and systematic tracking of operations, decisions, and results.

## Overview

This skill helps organize data analysis projects with:

- **Standardized directory structure** for consistent project organization
- **Automatic operation logging** with timestamps and detailed metadata
- **Decision tracking** to document analytical choices and reasoning
- **Analysis session management** with timestamped directories
- **Integration with scientific writing** to extract methods from logs

## Features

### 🗂️ Standard Directory Structure

Every project follows a consistent organization:

```
project_root/
├── 00_raw_data/           # Original, unmodified data
├── 01_analysis/           # Analysis scripts and notebooks
│   └── YYYYMMDD_HHMM_*/  # Timestamped analysis sessions
├── 02_processed_data/     # Cleaned, transformed data
├── 03_results/            # Final outputs (figures, tables, stats)
├── 04_reports/            # Written reports and manuscripts
├── 05_models/             # Trained models
└── logs/                  # Centralized logging
    ├── MASTER_LOG.md      # Complete operation history
    ├── decisions.md       # Analytical decisions
    └── errors.md          # Error tracking
```

### 📝 Automatic Logging

The `AnalysisLogger` class automatically records:

- **Operations**: Data processing, analysis, modeling, visualization
- **Decisions**: Statistical test choices, parameter selections, method justifications
- **Results**: Key findings, statistics, effect sizes
- **Outputs**: Figures, tables, models with file paths
- **Errors**: Issues encountered and their resolutions

### 🔬 Scientific Workflow Integration

Designed to work seamlessly with scientific research:

- Extract methods text from logs for manuscripts
- Generate analysis summaries and timelines
- Track reproducibility with complete parameter logs
- Document all analytical decisions with reasoning
- Link outputs to the operations that created them

## Installation

### As a Claude Skill

1. Copy this directory to `~/.claude/skills/data-analysis-workflow/`
2. The skill will be automatically available in Claude Code

### Standalone Use

Clone the repository and use the scripts directly:

```bash
git clone https://github.com/yf8578/data-analysis-workflow.git
cd data-analysis-workflow
```

## Quick Start

### 1. Initialize a New Project

```bash
python scripts/init_project.py my_project
cd my_project
```

This creates the standard directory structure with README files and initial logs.

### 2. Use AnalysisLogger in Your Code

```python
import sys
from pathlib import Path

# Add to path (adjust based on your installation)
sys.path.insert(0, '/path/to/data-analysis-workflow/scripts')
from log_helper import AnalysisLogger

# Initialize logger
logger = AnalysisLogger(project_root=".")

# Log an operation
logger.log_operation(
    operation="Data cleaning",
    location="02_processed_data/cleaned_data.csv",
    operation_type="Data Processing",
    params={"method": "remove_outliers", "threshold": 3},
    result="Removed 47 outliers (2.3% of data)",
    key_findings=["Most outliers in age column"],
    notes="Used IQR method"
)

# Log an analytical decision
logger.log_decision(
    question="Which statistical test for group comparison?",
    decision="Welch's t-test instead of standard t-test",
    reasoning="Unequal variances detected (Levene p=0.003)",
    references=["Statistics textbook, Chapter 9"]
)

# Create an analysis session
analysis_dir = logger.create_analysis_log(
    analysis_name="exploratory_analysis",
    input_data=["00_raw_data/dataset.csv"],
    methods=["Summary statistics", "Distribution plots", "Correlation analysis"],
    analyst="Your Name"
)
```

### 3. Generate Project Summary

```bash
python scripts/summarize_analysis.py
```

This generates `ANALYSIS_SUMMARY.md` with:

- Timeline of all operations
- Summary by operation type
- Key findings compilation
- Inventory of outputs (figures, tables, models)
- Next steps from analysis logs

## Components

### Scripts

- **`log_helper.py`**: Core `AnalysisLogger` class with logging methods
- **`init_project.py`**: Initialize new projects with standard structure
- **`summarize_analysis.py`**: Generate project summaries from logs

### Documentation

- **`SKILL.md`**: Complete skill documentation for Claude integration
- **`USAGE_GUIDE.md`**: Quick start guide (Chinese)
- **`references/log_formats.md`**: Detailed log format specifications

## AnalysisLogger API

### Core Methods

#### `log_operation()`

Record data processing, analysis, or visualization operations.

```python
logger.log_operation(
    operation: str,              # Operation name
    location: str,               # File path (input or output)
    operation_type: str = "Analysis",
    params: Optional[Dict] = None,
    result: Optional[str] = None,
    key_findings: Optional[List[str]] = None,
    figures: Optional[List[str]] = None,
    notes: Optional[str] = None
)
```

#### `log_decision()`

Document analytical decisions with justification.

```python
logger.log_decision(
    question: str,                    # Decision point
    decision: str,                    # What was decided
    reasoning: str,                   # Why
    alternatives: Optional[List] = None,
    references: Optional[List] = None,
    impact: Optional[str] = None
)
```

#### `log_error()`

Track errors and their resolutions.

```python
logger.log_error(
    error_type: str,
    description: str,
    resolution: Optional[str] = None,
    code_snippet: Optional[str] = None
)
```

#### `create_analysis_log()`

Create timestamped analysis directory with detailed log.

```python
analysis_dir = logger.create_analysis_log(
    analysis_name: str,
    input_data: List[str],
    methods: List[str],
    results: Optional[Dict] = None,
    next_steps: Optional[List[str]] = None,
    notes: Optional[str] = None,
    analyst: str = "Unknown"
)
```

## Log Formats

### MASTER_LOG.md

Chronological record of all operations:

```markdown
### [2026-02-28 14:30:45] Data Cleaning
**Type:** Data Processing
**Location:** `02_processed_data/cleaned.csv`
**Parameters:**
- method: remove_outliers
- threshold: 3

**Result:** Removed 47 outliers (2.3%)
**Key Findings:**
- Most outliers in age column
- Normal distribution after cleaning

**Notes:** Used IQR method

---
```

### analysis_log.md

Detailed logs for each analysis session stored in `01_analysis/YYYYMMDD_HHMM_name/`:

- Objective and research questions
- Input data sources
- Methods and parameters
- Results and statistics
- Key findings
- Limitations
- Next steps

See [`references/log_formats.md`](references/log_formats.md) for complete format specifications.

## Example Workflows

### Exploratory Data Analysis

```python
logger = AnalysisLogger()

# Create analysis session
logger.create_analysis_log(
    analysis_name="initial_exploration",
    input_data=["00_raw_data/dataset.csv"],
    methods=["Summary statistics", "Distribution plots"]
)

# Log data loading
data = pd.read_csv("00_raw_data/dataset.csv")
logger.log_operation("Load data", "00_raw_data/dataset.csv",
                     result=f"{len(data)} rows, {data.shape[1]} columns")

# Log visualization
fig_path = "03_results/figures/distributions.png"
plot_distributions(data, save_path=fig_path)
logger.log_operation("Generate distributions", fig_path,
                     key_findings=["Age: right-skewed", "Income: bimodal"])
```

### Model Training

```python
# Train model
model = RandomForestClassifier(**params)
model.fit(X_train, y_train)

# Save and log
model_path = "05_models/rf_v1.pkl"
joblib.dump(model, model_path)

logger.log_operation(
    operation="Train Random Forest",
    location=model_path,
    operation_type="Modeling",
    params={"n_estimators": 100, "max_depth": 10},
    result=f"CV accuracy: {cv_score:.3f}",
    key_findings=["Top feature: age (importance=0.34)"]
)
```

## Integration with Scientific Writing

Extract methods text from logs for manuscripts:

```python
from log_helper import extract_methods

methods_text = extract_methods(
    log_path="logs/MASTER_LOG.md",
    start_date="2026-02-01",
    end_date="2026-02-28",
    format="markdown"  # or "latex"
)

# Use in manuscript Methods section
with open("04_reports/methods_draft.md", "w") as f:
    f.write(methods_text)
```

## Best Practices

1. **Log immediately** after operations complete
2. **Be specific** with parameters and file paths
3. **Quantify results** with numbers, p-values, effect sizes
4. **Document decisions** explaining why, not just what
5. **Link outputs** to the operations that created them
6. **Never modify** files in `00_raw_data/`
7. **Use timestamps** for all generated files (`YYYYMMDD_name.ext`)
8. **Review logs regularly** to track progress

## Benefits

- ✅ **Reproducibility**: Complete record of all operations
- ✅ **Transparency**: Clear documentation of decisions
- ✅ **Efficiency**: Easy to review and extract for reports
- ✅ **Collaboration**: Keep team members informed
- ✅ **Learning**: Track what worked and what didn't
- ✅ **Publication ready**: Extract methods for manuscripts

## Requirements

- Python 3.7+
- Standard library only (no external dependencies for core functionality)
- Works with pandas, scikit-learn, and other analysis libraries

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Author

Created as a Claude Code skill for systematic data analysis workflows.

## Links

- [Detailed Format Specifications](references/log_formats.md)
- [Complete Skill Documentation](SKILL.md)
- [Quick Start Guide (中文)](USAGE_GUIDE.md)

---

**Status**: Production ready ✓
**Version**: 1.0.0
**Created**: 2026-02-28
