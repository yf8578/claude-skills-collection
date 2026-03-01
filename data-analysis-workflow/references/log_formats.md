# Log Format Specifications

Complete format specifications for all log files in the data-analysis-workflow system.

## MASTER_LOG.md Format

The master log records all operations chronologically with detailed metadata.

### Header Section

```markdown
# Project: [Project Name]
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD HH:MM:SS

## Operation Log
```

**Fields:**
- `Project`: Name of the project (automatically set from directory name)
- `Created`: Date when project was initialized
- `Last Updated`: Automatically updated with each new log entry

### Operation Entry Format

```markdown
### [YYYY-MM-DD HH:MM:SS] Operation Name
**Type:** [Operation Type]
**Location:** `path/to/file`
**Parameters:**
- parameter1: value1
- parameter2: value2

**Result:** Brief description of outcome (one sentence)
**Key Findings:**
- Finding 1 with supporting evidence
- Finding 2 with supporting evidence

**Figures/Tables Generated:**
- `path/to/figure1.png` - Description
- `path/to/table1.csv` - Description

**Notes:** Additional context, caveats, or observations

---
```

### Field Descriptions

#### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `Timestamp` | ISO format timestamp | `2026-02-28 14:30:45` |
| `Operation Name` | Brief descriptive name | `Data cleaning` |
| `Type` | Category of operation | `Data Processing` |
| `Location` | Primary file path | `02_processed_data/cleaned.csv` |

#### Optional Fields

| Field | When to Use | Example |
|-------|-------------|---------|
| `Parameters` | When operation has configurable options | `threshold: 3`, `method: IQR` |
| `Result` | When operation produces measurable outcome | `Removed 47 outliers (2.3%)` |
| `Key Findings` | When operation reveals insights | `Most outliers in age column` |
| `Figures/Tables` | When operation generates visualizations | `figures/distribution.png` |
| `Notes` | For additional context or caveats | `Used conservative threshold due to small sample` |

### Operation Types

Standard operation types for consistency:

- **Data Processing**: Loading, cleaning, transforming, merging data
- **Analysis**: Statistical tests, modeling, exploratory analysis
- **Modeling**: Model training, hyperparameter tuning, evaluation
- **Visualization**: Figure generation, plotting, visual exploration
- **Reporting**: Document generation, summary creation
- **Project Setup**: Initialization, directory creation, configuration

### Examples

#### Example 1: Data Processing

```markdown
### [2026-02-28 09:15:23] Remove outliers from patient data
**Type:** Data Processing
**Location:** `02_processed_data/20260228_patients_cleaned.csv`
**Parameters:**
- method: IQR
- threshold: 3
- columns: ['age', 'weight', 'blood_pressure']

**Result:** Removed 47 outliers from 2,034 total records (2.3%)
**Key Findings:**
- Most outliers found in age column (n=32)
- Blood pressure outliers potentially measurement errors
- Weight outliers appear to be data entry errors (e.g., 600 kg)

**Notes:** Used IQR method instead of z-score due to non-normal distributions. Saved outlier records to `02_processed_data/outliers_20260228.csv` for manual review.

---
```

#### Example 2: Statistical Analysis

```markdown
### [2026-02-28 10:45:12] Compare treatment groups
**Type:** Analysis
**Location:** `03_results/statistics/treatment_comparison.txt`
**Parameters:**
- test: Welch's t-test
- alpha: 0.05
- alternative: two-sided

**Result:** Significant difference detected (t=3.45, p=0.0008, df=198)
**Key Findings:**
- Treatment group mean: 42.3 ± 8.1 (n=102)
- Control group mean: 38.7 ± 9.4 (n=98)
- Effect size (Cohen's d): 0.41 (small to medium)

**Figures/Tables Generated:**
- `03_results/figures/treatment_boxplot.png` - Side-by-side boxplots
- `03_results/tables/descriptive_stats.csv` - Summary statistics by group

**Notes:** Used Welch's t-test instead of standard t-test due to unequal variances (Levene's p=0.003). Assumption checks passed except for slight deviation from normality in treatment group (Shapiro-Wilk p=0.042), but t-test is robust to minor violations with n>30.

---
```

#### Example 3: Model Training

```markdown
### [2026-02-28 14:22:35] Train Random Forest classifier
**Type:** Modeling
**Location:** `05_models/20260228_rf_v1.pkl`
**Parameters:**
- n_estimators: 100
- max_depth: 10
- min_samples_split: 5
- random_state: 42
- cv_folds: 5

**Result:** Cross-validation accuracy: 0.847 ± 0.023
**Key Findings:**
- Top 3 features: age (0.34), BMI (0.22), systolic_bp (0.18)
- Training converged after 87 trees
- No evidence of overfitting (train acc=0.891, test acc=0.852)

**Figures/Tables Generated:**
- `03_results/figures/feature_importance.png` - Bar plot of feature importances
- `03_results/figures/learning_curve.png` - CV learning curves
- `03_results/tables/model_performance.csv` - Detailed metrics by fold

**Notes:** Tested max_depth values [5, 10, 15, 20]. Chose 10 as best trade-off between performance and interpretability. Model saved with joblib for later deployment.

---
```

## analysis_log.md Format

Detailed log for individual analysis sessions, stored in timestamped directories.

### Complete Template

```markdown
# Analysis: [Descriptive Name]
**Date:** YYYY-MM-DD HH:MM
**Analyst:** [Name or Username]
**Status:** In Progress / Complete / Archived

## Objective
Brief description of what this analysis aims to accomplish. Include specific research questions or hypotheses.

## Input Data
List all input data files with descriptions:

- `path/to/input1.csv` - Description of dataset (n=XXX, variables=YY)
- `path/to/input2.csv` - Description of dataset
- `path/to/metadata.txt` - Codebook or metadata

## Methods
Detailed description of analytical approach:

1. **Data Preparation**
   - Specific preprocessing steps
   - Transformations applied
   - Quality control checks

2. **Statistical Analysis**
   - Tests or models used
   - Parameters and assumptions
   - Multiple testing corrections

3. **Visualization**
   - Types of plots created
   - Purpose of each visualization

## Results

### Summary Statistics
- Statistic 1: value (95% CI: [lower, upper])
- Statistic 2: value (interpretation)

### Statistical Tests
- Test 1: result (test statistic, p-value, effect size)
- Test 2: result (test statistic, p-value, effect size)

### Model Performance (if applicable)
- Accuracy: X.XXX
- Precision: X.XXX
- Recall: X.XXX
- F1-score: X.XXX

### Figures
- `outputs/figure1_distribution.png` - Description and interpretation
- `outputs/figure2_correlation.png` - Description and interpretation

### Tables
- `outputs/table1_summary_stats.csv` - Description
- `outputs/table2_test_results.csv` - Description

## Key Findings
Numbered list of important discoveries with evidence:

1. **Finding 1 headline**
   - Supporting evidence from results
   - Statistical significance and effect size
   - Interpretation in context

2. **Finding 2 headline**
   - Supporting evidence
   - Comparison to expectations or prior literature

3. **Finding 3 headline**
   - Evidence and interpretation

## Limitations
Honest assessment of analytical limitations:

- Limitation 1 (impact: high/medium/low)
- Limitation 2 (impact: high/medium/low)

## Next Steps
Actionable items with checkbox format:

- [ ] Validate findings with independent dataset
- [ ] Perform sensitivity analysis varying parameter X
- [ ] Write up results for manuscript Methods section
- [ ] Share preliminary findings with collaborators

## Notes
Additional observations, caveats, or future ideas:

- Unexpected pattern in subgroup X warrants follow-up
- Consider alternative model Y for comparison
- Raw data quality issues in columns A, B require investigation

## References
Citations for methods or context:

- Reference 1 (methodology)
- Reference 2 (comparison data)

---

**Analysis Metadata:**
- Start time: YYYY-MM-DD HH:MM
- End time: YYYY-MM-DD HH:MM
- Total duration: X hours Y minutes
- Software versions: Python 3.11, pandas 2.0, scikit-learn 1.3
```

### Status Values

| Status | Meaning | When to Use |
|--------|---------|-------------|
| `In Progress` | Active work | Analysis currently underway |
| `Complete` | Finished | Analysis concluded, results finalized |
| `Archived` | Historical | Moved to archive/, superseded by later analysis |
| `On Hold` | Paused | Temporarily suspended, will resume later |
| `Failed` | Unsuccessful | Analysis abandoned due to errors or infeasibility |

## decisions.md Format

Records all analytical decisions with justification.

### Entry Template

```markdown
## [YYYY-MM-DD] Decision Title (Question Form)

**Question:** What specific question or decision point was encountered?

**Decision:** Clear statement of what was decided.

**Reasoning:**
Detailed explanation of why this decision was made:

1. Reason 1 with supporting evidence
2. Reason 2 with data or citations
3. Reason 3 with methodological justification

**Alternatives Considered:**
- **Alternative 1:** Description
  - Pros: Benefits of this approach
  - Cons: Drawbacks that led to rejection
- **Alternative 2:** Description
  - Pros: Benefits
  - Cons: Drawbacks

**References:**
- Citation 1 supporting the decision
- Citation 2 providing methodological guidance
- Documentation link or textbook reference

**Impact:** Expected impact on downstream analysis and results.

**Confidence:** High / Medium / Low

**Reversible:** Yes / No (can this decision be changed later without major rework?)

---
```

### Example Decision Entries

#### Example 1: Statistical Test Selection

```markdown
## [2026-02-28] Which statistical test for group comparison?

**Question:** Should we use standard t-test, Welch's t-test, or Mann-Whitney U test to compare treatment and control groups?

**Decision:** Use Welch's t-test for the primary analysis.

**Reasoning:**
1. **Unequal variances detected:** Levene's test showed significant difference (F=8.92, p=0.003)
2. **Near-normal distributions:** Both groups approximately normal (Shapiro-Wilk p>0.05)
3. **Sufficient sample size:** n=102 and n=98 make t-test robust to minor assumption violations
4. **Standard in field:** Previous studies in this area use Welch's t-test
5. **More powerful than non-parametric:** Given approximate normality, t-test has better power than Mann-Whitney

**Alternatives Considered:**
- **Standard Student's t-test:**
  - Pros: Simpler, more widely known
  - Cons: Assumes equal variances, violated in our data
- **Mann-Whitney U test (non-parametric):**
  - Pros: No distribution assumptions
  - Cons: Less powerful when distributions are normal, tests medians not means

**References:**
- Ruxton, G. D. (2006). The unequal variance t-test is an underused alternative to Student's t-test and the Mann–Whitney U test. Behavioral Ecology, 17(4), 688-690.
- Field, A. (2013). Discovering Statistics Using IBM SPSS Statistics (4th ed.), Chapter 9.

**Impact:** This choice affects how we report results and interpret p-values. Welch's test produces slightly larger confidence intervals than standard t-test, leading to more conservative inference.

**Confidence:** High

**Reversible:** Yes (can rerun with different test if reviewers request)

---
```

#### Example 2: Data Transformation

```markdown
## [2026-02-28] Should we log-transform the income variable?

**Question:** Should we apply log transformation to the highly right-skewed income variable before analysis?

**Decision:** Apply log10 transformation to income for all analyses.

**Reasoning:**
1. **Extreme right skew:** Original skewness = 3.2, kurtosis = 15.4
2. **Range spans orders of magnitude:** Min=$12k, Max=$4.2M
3. **Interpretability:** Log transformation allows interpretation as multiplicative effects
4. **Improved model fit:** Log-transformed income improves R² from 0.23 to 0.41
5. **Standard practice:** Income typically log-transformed in economics literature

**Alternatives Considered:**
- **No transformation:**
  - Pros: Easier interpretation, preserves absolute scale
  - Cons: Violates normality/linearity assumptions, poor model fit
- **Square root transformation:**
  - Pros: Less extreme than log
  - Cons: Still shows skewness=1.8, doesn't match field conventions
- **Winsorization (cap extreme values):**
  - Pros: Preserves most data on original scale
  - Cons: Arbitrary cutoff, loses information about high earners

**References:**
- Wooldridge, J. M. (2015). Introductory Econometrics (6th ed.), Chapter 6.2
- Benoit, K. (2011). Linear Regression Models with Logarithmic Transformations. London School of Economics.

**Impact:** Results will be reported as percentage changes rather than absolute dollar amounts. This affects interpretation but is standard in the field.

**Confidence:** High

**Reversible:** Yes (but would require re-running all analyses)

---
```

## errors.md Format

Tracks errors encountered and their resolutions.

### Entry Template

```markdown
## [YYYY-MM-DD HH:MM:SS] Error Type/Category

**Description:** Clear description of what went wrong and when.

**Error Message:**
```
Full error traceback or message
```

**Context:**
- What were you trying to do?
- Which script/notebook?
- Input data characteristics
- Software versions

**Root Cause:** Analysis of why the error occurred.

**Resolution:** Step-by-step description of how the error was fixed.

**Prevention:** How to avoid this error in the future.

**Status:** Resolved / Unresolved

**Time to Resolve:** X minutes/hours

---
```

### Example Error Entry

```markdown
## [2026-02-28 11:23:15] Memory Error Loading Large Dataset

**Description:** Python crashed with MemoryError when attempting to load full dataset into pandas DataFrame.

**Error Message:**
```
MemoryError: Unable to allocate 8.34 GiB for an array with shape (1000000000, 12) and data type float64
```

**Context:**
- Script: `01_analysis/20260228_1100_initial_exploration/load_data.py`
- Input: `00_raw_data/sensor_data_2023.csv` (15 GB, 1B rows)
- System: MacBook Pro M1, 16 GB RAM
- Python 3.11, pandas 2.0.0

**Root Cause:** Dataset too large to fit in available RAM. Standard `pd.read_csv()` loads entire file into memory before processing.

**Resolution:**
1. **Switched to chunked reading:**
   ```python
   chunks = pd.read_csv('data.csv', chunksize=100000)
   processed = pd.concat([process_chunk(chunk) for chunk in chunks])
   ```

2. **Alternative solution considered:** Use Dask for out-of-core processing, but chunking was sufficient for this task.

3. **Optimized data types:** Reduced memory by downcasting numeric columns:
   ```python
   df['sensor_id'] = df['sensor_id'].astype('int32')  # was int64
   df['timestamp'] = pd.to_datetime(df['timestamp'])  # was string
   ```

4. **Final memory usage:** Reduced from 15 GB to 4.2 GB after optimization.

**Prevention:**
- Always check file size before loading: `os.path.getsize('file.csv') / (1024**3)` GB
- Use `chunksize` parameter for files > 1 GB
- Profile memory usage: `df.memory_usage(deep=True).sum() / (1024**3)` GB
- Consider Dask or Polars for datasets > 10 GB

**Status:** Resolved

**Time to Resolve:** 45 minutes

---
```

## File Naming Conventions

### Timestamped Files

Format: `YYYYMMDD_descriptive_name.ext`

Examples:
- `20260228_cleaned_patient_data.csv`
- `20260228_exploratory_analysis.ipynb`
- `20260228_regression_results.txt`

### Timestamped Directories

Format: `YYYYMMDD_HHMM_descriptive_name/`

Examples:
- `01_analysis/20260228_1430_differential_expression/`
- `01_analysis/20260301_0915_survival_analysis/`

### Benefits

1. **Chronological sorting:** Files sort naturally by date
2. **No conflicts:** Timestamp ensures unique names
3. **Tracking:** Easy to see when work was done
4. **Reproducibility:** Links to log entries by timestamp

## Best Practices

### Writing Effective Log Entries

1. **Be specific:** "Removed 47 outliers" not "Cleaned data"
2. **Include context:** Why, not just what
3. **Quantify results:** Include numbers, p-values, effect sizes
4. **Link outputs:** Always list generated figures/tables
5. **Document decisions:** Record why you chose method X over Y

### Maintaining Consistency

1. **Use templates:** Start from standard formats
2. **Standardize operation types:** Stick to predefined categories
3. **Update immediately:** Log right after operations complete
4. **Review regularly:** Check MASTER_LOG weekly
5. **Archive completed work:** Move finished analyses to archive/

### Integration with Code

```python
from data_analysis_workflow.log_helper import AnalysisLogger

logger = AnalysisLogger()

# Log at key checkpoints
data = load_data()
logger.log_operation("Load data", "00_raw_data/dataset.csv",
                     result=f"{len(data)} rows loaded")

# Log decisions immediately
logger.log_decision(
    question="Which test to use?",
    decision="Welch's t-test",
    reasoning="Unequal variances detected"
)

# Create analysis sessions
logger.create_analysis_log(
    analysis_name="exploratory_eda",
    input_data=["00_raw_data/dataset.csv"],
    methods=["Summary stats", "Distributions"]
)
```

## Summary

Well-formatted logs provide:

✓ **Reproducibility:** Others can recreate your work
✓ **Transparency:** Clear record of all decisions
✓ **Efficiency:** Easy to review and extract for reports
✓ **Learning:** Track what worked and what didn't
✓ **Collaboration:** Keep team members informed

Use these formats consistently to build a comprehensive analysis archive.
