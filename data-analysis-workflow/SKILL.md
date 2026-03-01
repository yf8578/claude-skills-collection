---
name: data-analysis-workflow
description: Structured data analysis workflow with automatic logging and standardized project organization. Use when starting a new data analysis project or when you need to organize analysis operations, track decisions, and maintain analysis logs in specific directories for easy retrieval and reporting.
---

# Data Analysis Workflow

## Overview

This skill provides a standardized structure for organizing data analysis projects with automatic logging of all operations, decisions, and results. It ensures that key operations and analysis logs are systematically recorded in specific directories, making it easy to review, reproduce, and report on analysis work.

**Use this skill when:**
- Starting a new data analysis project
- Need to track analysis operations systematically
- Want to maintain organized logs of decisions and results
- Preparing analysis for publication or reporting
- Collaborating on data analysis projects
- Need to reproduce or review past analyses

## Core Principles

1. **Standardized Directory Structure**: All projects follow consistent organization
2. **Automatic Logging**: Every operation is logged with timestamp and details
3. **Decision Documentation**: Analytical decisions are recorded with reasoning
4. **Timestamped Analysis**: Each analysis run gets a unique timestamped directory
5. **Progressive Organization**: Data flows logically from raw → processed → results

## Standard Directory Structure

Every data analysis project follows this structure:

```
project_root/
├── 00_raw_data/           # Original, unmodified data
│   ├── experiment_1/
│   └── README.md          # Data provenance and descriptions
│
├── 01_analysis/           # Analysis scripts and notebooks
│   ├── YYYYMMDD_HHMM_descriptive_name/  # Timestamped analysis directories
│   │   ├── analysis_log.md              # Detailed analysis log
│   │   ├── script.py or notebook.ipynb
│   │   └── outputs/
│   └── archive/           # Completed analyses
│
├── 02_processed_data/     # Cleaned, transformed data
│   ├── YYYYMMDD_dataset_name.csv
│   └── processing_notes.md
│
├── 03_results/            # Final analysis outputs
│   ├── figures/
│   ├── tables/
│   └── statistics/
│
├── 04_reports/            # Written reports and summaries
│   ├── YYYYMMDD_report_name.md
│   └── final_manuscript/
│
├── 05_models/             # Trained models and parameters
│   ├── model_v1/
│   └── model_registry.md
│
└── logs/                  # Centralized logging
    ├── MASTER_LOG.md      # Complete project operation log
    ├── decisions.md       # Key analytical decisions
    └── errors.md          # Error tracking and resolutions
```

## Workflow

### 1. Initialize a New Project

Create the standard directory structure:

```bash
python ~/.claude/skills/data-analysis-workflow/scripts/init_project.py project_name
cd project_name
```

This creates:
- All standard directories
- Initial README files
- Empty MASTER_LOG.md with header
- .gitignore configured for data analysis

### 2. Log Every Operation

Use the AnalysisLogger class to record operations:

```python
from data_analysis_workflow.log_helper import AnalysisLogger

logger = AnalysisLogger(project_root=".")

# Log a data processing operation
logger.log_operation(
    operation="Data cleaning",
    location="02_processed_data/20260228_cleaned_data.csv",
    params={"method": "remove_outliers", "threshold": 3},
    result="Removed 47 outliers (2.3% of data)",
    key_findings=["Most outliers in column X", "Normal distribution after cleaning"],
    notes="Used IQR method"
)

# Log an analytical decision
logger.log_decision(
    question="Which statistical test to use for group comparison?",
    decision="Welch's t-test instead of standard t-test",
    reasoning="Unequal variances detected (Levene p=0.003)",
    references=["Statistics textbook, p.234"]
)
```

### 3. Create Analysis-Specific Logs

For each analysis session, create a timestamped directory with detailed log:

```python
logger.create_analysis_log(
    analysis_name="differential_expression",
    input_data=["00_raw_data/counts_matrix.csv", "00_raw_data/metadata.csv"],
    methods=[
        "DESeq2 normalization",
        "Negative binomial GLM",
        "Benjamini-Hochberg FDR correction"
    ],
    results={
        "significant_genes": 423,
        "upregulated": 256,
        "downregulated": 167
    },
    next_steps=[
        "Pathway enrichment analysis",
        "Validate top 20 genes with qPCR"
    ],
    notes="Used stricter FDR < 0.01 instead of 0.05 due to large sample size"
)
```

This creates:
- `01_analysis/20260228_1430_differential_expression/`
- `01_analysis/20260228_1430_differential_expression/analysis_log.md`

### 4. Organize Data Progressively

Follow the data flow through directories:

```python
# Step 1: Load raw data
raw_data = pd.read_csv("00_raw_data/experiment_1/data.csv")
logger.log_operation("Load raw data", "00_raw_data/experiment_1/data.csv",
                     result=f"{len(raw_data)} rows loaded")

# Step 2: Clean and save to processed
cleaned_data = clean_data(raw_data)
output_path = "02_processed_data/20260228_cleaned_data.csv"
cleaned_data.to_csv(output_path, index=False)
logger.log_operation("Clean data", output_path,
                     params={"method": "remove_na", "impute": False},
                     result=f"{len(cleaned_data)} rows after cleaning")

# Step 3: Analyze and save results
results = analyze_data(cleaned_data)
fig_path = "03_results/figures/distribution_plot.png"
save_figure(fig_path)
logger.log_operation("Generate distribution plot", fig_path,
                     key_findings=["Bimodal distribution detected"])
```

### 5. Review and Summarize

Generate project summary from logs:

```bash
python ~/.claude/skills/data-analysis-workflow/scripts/summarize_analysis.py
```

This produces:
- Summary of all operations from MASTER_LOG.md
- Timeline of analysis progression
- Key decisions and their rationales
- Figures and results inventory
- Outstanding next steps

## Log Format Specifications

### MASTER_LOG.md Format

```markdown
# Project: [Project Name]
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD HH:MM:SS

## Operation Log

### [YYYY-MM-DD HH:MM:SS] Operation Name
**Type:** Data Processing / Analysis / Modeling / Visualization
**Location:** path/to/file
**Parameters:**
- param1: value1
- param2: value2

**Result:** Brief description of outcome
**Key Findings:**
- Finding 1
- Finding 2

**Figures/Tables Generated:**
- path/to/figure1.png
- path/to/table1.csv

**Notes:** Additional context or observations

---
```

### analysis_log.md Format (in timestamped directories)

```markdown
# Analysis: [Descriptive Name]
**Date:** YYYY-MM-DD HH:MM
**Analyst:** [Name]
**Status:** In Progress / Complete / Archived

## Objective
Brief description of analysis goals

## Input Data
- `path/to/input1.csv` - Description
- `path/to/input2.csv` - Description

## Methods
1. Method 1 with parameters
2. Method 2 with parameters

## Results
### Key Statistics
- Statistic 1: value (interpretation)
- Statistic 2: value (interpretation)

### Figures
- `outputs/figure1.png` - Description
- `outputs/figure2.png` - Description

## Key Findings
1. Finding 1 with evidence
2. Finding 2 with evidence

## Next Steps
- [ ] Action item 1
- [ ] Action item 2

## Notes
Additional observations, caveats, or context
```

### decisions.md Format

```markdown
# Analytical Decisions Log

## [YYYY-MM-DD] Decision Title

**Question:** What decision needed to be made?

**Decision:** What was decided?

**Reasoning:**
- Reason 1
- Reason 2
- Supporting evidence

**Alternatives Considered:**
- Alternative 1 (why rejected)
- Alternative 2 (why rejected)

**References:**
- Citation 1
- Citation 2

**Impact:** Expected impact on analysis

---
```

## Best Practices

### Directory Organization

1. **Never modify files in 00_raw_data/**: Always work on copies
2. **Use timestamps for files**: Format `YYYYMMDD_descriptive_name`
3. **Include README files**: Document data sources and processing
4. **Archive completed analyses**: Move to `01_analysis/archive/`
5. **Organize by data stage**: Follow the numbered directory progression

### Logging Practices

1. **Log immediately**: Record operations as they complete
2. **Be specific**: Include parameters, file paths, sample sizes
3. **Document decisions**: Record why, not just what
4. **Track errors**: Log failures and how they were resolved
5. **Link outputs**: Connect figures/tables to the operations that created them

### Analysis Organization

1. **One directory per analysis run**: Use timestamped directories
2. **Self-contained analyses**: Each directory should be reproducible independently
3. **Clear naming**: Use descriptive names, not just dates
4. **Document dependencies**: List all input files explicitly
5. **Track next steps**: Note what should happen next

### Collaboration

1. **Commit logs frequently**: Logs are as important as code
2. **Review MASTER_LOG**: Check before starting new work
3. **Update decisions.md**: Keep team aligned on analytical choices
4. **Standardize formats**: Follow the templates consistently
5. **Document everything**: Assume you'll forget details

## Integration with Scientific Writing

When preparing manuscripts or reports:

1. **Extract from MASTER_LOG**: Use logged operations for Methods section
2. **Reference decisions.md**: Justify analytical choices in manuscript
3. **Link figures automatically**: Logs contain all figure paths
4. **Generate methods text**: Summarize logged operations
5. **Track reproducibility**: Logs provide complete workflow documentation

Example extraction:

```python
from data_analysis_workflow.log_helper import extract_methods

methods_text = extract_methods(
    log_path="logs/MASTER_LOG.md",
    start_date="2026-02-01",
    end_date="2026-02-28",
    format="markdown"  # or "latex"
)
```

This generates Methods section text directly from logged operations.

## Example Workflows

### Workflow 1: Exploratory Data Analysis

```python
from data_analysis_workflow.log_helper import AnalysisLogger

logger = AnalysisLogger()

# Create analysis session
logger.create_analysis_log(
    analysis_name="initial_exploration",
    input_data=["00_raw_data/dataset.csv"],
    methods=["Summary statistics", "Distribution plots", "Correlation analysis"]
)

# Perform analysis and log each step
data = pd.read_csv("00_raw_data/dataset.csv")
logger.log_operation("Load data", "00_raw_data/dataset.csv",
                     result=f"{data.shape[0]} rows, {data.shape[1]} columns")

# Generate and log figures
fig_path = "03_results/figures/20260228_distributions.png"
plot_distributions(data, save_path=fig_path)
logger.log_operation("Generate distribution plots", fig_path,
                     key_findings=["Age: right-skewed", "Income: bimodal"])

# Log decision
logger.log_decision(
    question="Should we transform skewed variables?",
    decision="Apply log transformation to age and income",
    reasoning="Both show right skew >2.0, transformation may improve model fit"
)
```

### Workflow 2: Model Training

```python
logger = AnalysisLogger()

# Create model training session
logger.create_analysis_log(
    analysis_name="random_forest_v1",
    input_data=["02_processed_data/20260228_training_data.csv"],
    methods=["Random Forest", "5-fold CV", "Hyperparameter tuning"]
)

# Train and log
model = RandomForestClassifier(**params)
model.fit(X_train, y_train)

# Save model
model_path = "05_models/20260228_rf_v1.pkl"
joblib.dump(model, model_path)

logger.log_operation(
    operation="Train Random Forest",
    location=model_path,
    params={"n_estimators": 100, "max_depth": 10},
    result=f"CV accuracy: {cv_score:.3f}",
    key_findings=[
        "Top feature: age (importance=0.34)",
        "Converged after 87 trees"
    ]
)
```

### Workflow 3: Report Generation

```python
# Summarize project for manuscript
from data_analysis_workflow.log_helper import generate_report

report = generate_report(
    log_path="logs/MASTER_LOG.md",
    sections=["methods", "results", "figures"],
    output_format="markdown"
)

# Save to reports directory
report_path = "04_reports/20260228_analysis_summary.md"
with open(report_path, 'w') as f:
    f.write(report)

logger.log_operation("Generate analysis report", report_path,
                     notes="Ready for manuscript Methods section")
```

## Helper Scripts

### scripts/init_project.py
Initialize new project with standard directory structure

```bash
python ~/.claude/skills/data-analysis-workflow/scripts/init_project.py my_project
```

### scripts/log_helper.py
Python module with AnalysisLogger class for automatic logging

```python
from data_analysis_workflow.log_helper import AnalysisLogger
logger = AnalysisLogger()
```

### scripts/summarize_analysis.py
Generate project summary from logs

```bash
python ~/.claude/skills/data-analysis-workflow/scripts/summarize_analysis.py
```

### scripts/extract_methods.py
Extract Methods section text from operation logs

```bash
python ~/.claude/skills/data-analysis-workflow/scripts/extract_methods.py --format markdown
```

## References

For detailed documentation:
- `references/log_formats.md`: Complete log format specifications with examples
- `references/examples.md`: Example projects with complete logs
- `references/best_practices.md`: Extended best practices guide

## Integration with Other Skills

This skill works well with:
- **scientific-writing**: Extract logged operations for Methods sections
- **statistical-analysis**: Log all statistical tests and decisions
- **exploratory-data-analysis**: Document EDA findings systematically
- **peer-review**: Provide complete analysis documentation for reviewers
- **research-grants**: Demonstrate systematic approach and reproducibility
