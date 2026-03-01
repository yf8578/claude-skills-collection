#!/usr/bin/env python3
"""
Initialize a new data analysis project with standard directory structure.

Usage:
    python init_project.py project_name [--path /path/to/parent/dir]
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


STANDARD_DIRECTORIES = [
    "00_raw_data",
    "01_analysis",
    "01_analysis/archive",
    "02_processed_data",
    "03_results",
    "03_results/figures",
    "03_results/tables",
    "03_results/statistics",
    "04_reports",
    "04_reports/final_manuscript",
    "05_models",
    "logs"
]

README_TEMPLATES = {
    "00_raw_data/README.md": """# Raw Data

This directory contains original, unmodified data files.

## Data Provenance

### Dataset 1
- **Source:** [Data source]
- **Date obtained:** YYYY-MM-DD
- **Description:** [Brief description]
- **Files:**
  - `file1.csv` - Description
  - `file2.csv` - Description

### Dataset 2
- **Source:** [Data source]
- **Date obtained:** YYYY-MM-DD
- **Description:** [Brief description]
- **Files:**
  - `file3.csv` - Description

## Important Notes

- **DO NOT MODIFY FILES IN THIS DIRECTORY**
- All data processing should work on copies in 02_processed_data/
- Document any data cleaning or transformations in processing logs
""",

    "02_processed_data/processing_notes.md": """# Data Processing Notes

## Processing Log

### YYYY-MM-DD - Initial Cleaning
- **Input:** 00_raw_data/dataset.csv
- **Output:** YYYYMMDD_cleaned_data.csv
- **Operations:**
  - Removed missing values
  - Standardized column names
  - Converted date formats
- **Notes:** [Any important observations]

---
""",

    "05_models/model_registry.md": """# Model Registry

## Model Versions

### v1 - YYYY-MM-DD
- **Type:** [Model type, e.g., Random Forest]
- **Training data:** [Path to training data]
- **Parameters:**
  - param1: value1
  - param2: value2
- **Performance:**
  - Metric1: value
  - Metric2: value
- **Location:** `model_v1/`
- **Status:** Development / Testing / Production
- **Notes:** [Any important notes]

---
"""
}

GITIGNORE_CONTENT = """# Data files
00_raw_data/**/*.csv
00_raw_data/**/*.tsv
00_raw_data/**/*.xlsx
00_raw_data/**/*.txt
00_raw_data/**/*.h5
00_raw_data/**/*.hdf5
00_raw_data/**/*.parquet

# Large processed files
02_processed_data/**/*.csv
02_processed_data/**/*.tsv
02_processed_data/**/*.h5
02_processed_data/**/*.hdf5
02_processed_data/**/*.parquet

# Models
05_models/**/*.pkl
05_models/**/*.h5
05_models/**/*.pt
05_models/**/*.pth
05_models/**/*.onnx

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.bak
*.log
"""


def create_master_log(project_path: Path, project_name: str):
    """Create initial MASTER_LOG.md"""
    log_content = f"""# Project: {project_name}
**Created:** {datetime.now().strftime('%Y-%m-%d')}
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Operation Log

### [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Project Initialized
**Type:** Project Setup
**Location:** {project_path}

**Notes:** Standard project structure created with all directories and README files.

---

"""
    log_path = project_path / "logs" / "MASTER_LOG.md"
    log_path.write_text(log_content)
    return log_path


def create_project_readme(project_path: Path, project_name: str):
    """Create main project README.md"""
    readme_content = f"""# {project_name}

**Created:** {datetime.now().strftime('%Y-%m-%d')}
**Status:** Active

## Project Description

[Brief description of the analysis project]

## Objectives

1. Objective 1
2. Objective 2
3. Objective 3

## Directory Structure

```
{project_name}/
├── 00_raw_data/           # Original, unmodified data
├── 01_analysis/           # Analysis scripts and notebooks
│   ├── YYYYMMDD_HHMM_*/  # Timestamped analysis directories
│   └── archive/           # Completed analyses
├── 02_processed_data/     # Cleaned, transformed data
├── 03_results/            # Final outputs (figures, tables, stats)
├── 04_reports/            # Written reports and manuscripts
├── 05_models/             # Trained models
└── logs/                  # Master log and decision logs
```

## Quick Start

### Initialize Analysis Logger

```python
from data_analysis_workflow.log_helper import AnalysisLogger

logger = AnalysisLogger(project_root=".")
```

### Log Operations

```python
logger.log_operation(
    operation="Data cleaning",
    location="02_processed_data/cleaned.csv",
    params={{"method": "remove_outliers"}},
    result="Removed 47 outliers"
)
```

### Create Analysis Session

```python
logger.create_analysis_log(
    analysis_name="exploratory_analysis",
    input_data=["00_raw_data/dataset.csv"],
    methods=["Summary statistics", "Correlation analysis"]
)
```

## Team Members

- [Name] - [Role]

## References

- Reference 1
- Reference 2

## Notes

[Any important project-wide notes]
"""
    readme_path = project_path / "README.md"
    readme_path.write_text(readme_content)
    return readme_path


def init_project(project_name: str, parent_path: str = ".") -> Path:
    """
    Initialize a new data analysis project.

    Args:
        project_name: Name of the project
        parent_path: Parent directory where project will be created

    Returns:
        Path to created project directory
    """
    # Create project root
    project_path = Path(parent_path) / project_name

    if project_path.exists():
        print(f"Error: Directory '{project_path}' already exists")
        sys.exit(1)

    project_path.mkdir(parents=True)
    print(f"✓ Created project directory: {project_path}")

    # Create all standard directories
    for dir_name in STANDARD_DIRECTORIES:
        dir_path = project_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {dir_name}/")

    # Create README files
    for readme_path, content in README_TEMPLATES.items():
        full_path = project_path / readme_path
        full_path.write_text(content)
        print(f"  ✓ {readme_path}")

    # Create master README
    create_project_readme(project_path, project_name)
    print(f"  ✓ README.md")

    # Create MASTER_LOG
    create_master_log(project_path, project_name)
    print(f"  ✓ logs/MASTER_LOG.md")

    # Create .gitignore
    gitignore_path = project_path / ".gitignore"
    gitignore_path.write_text(GITIGNORE_CONTENT)
    print(f"  ✓ .gitignore")

    # Create example analysis script
    example_script = project_path / "01_analysis" / "example_analysis.py"
    example_script.write_text("""#!/usr/bin/env python3
\"\"\"
Example analysis script demonstrating AnalysisLogger usage.
\"\"\"

import sys
from pathlib import Path

# Add data-analysis-workflow to path
# If installed as skill: use absolute import
# If using locally: adjust path as needed
try:
    from data_analysis_workflow.log_helper import AnalysisLogger
except ImportError:
    print("Note: Install data-analysis-workflow skill or adjust import path")
    sys.exit(1)

# Initialize logger
logger = AnalysisLogger(project_root="..")

# Create analysis session
analysis_dir = logger.create_analysis_log(
    analysis_name="example_analysis",
    input_data=["../00_raw_data/dataset.csv"],
    methods=["Data loading", "Summary statistics", "Visualization"],
    analyst="Your Name"
)

print(f"Analysis directory created: {analysis_dir}")

# Example: Log an operation
logger.log_operation(
    operation="Load example data",
    location="00_raw_data/dataset.csv",
    operation_type="Data Processing",
    result="Loaded successfully",
    notes="This is an example operation"
)

print("✓ Example analysis setup complete!")
print(f"\\nNext steps:")
print(f"1. Add your data files to 00_raw_data/")
print(f"2. Edit {analysis_dir}/analysis_log.md with your analysis details")
print(f"3. Run your analysis and log operations")
print(f"4. Review logs/MASTER_LOG.md to see all operations")
""")
    print(f"  ✓ 01_analysis/example_analysis.py")

    print(f"\n{'='*60}")
    print(f"✓ Project '{project_name}' initialized successfully!")
    print(f"{'='*60}")
    print(f"\nNext steps:")
    print(f"1. cd {project_name}")
    print(f"2. Add your data files to 00_raw_data/")
    print(f"3. Start analysis and use AnalysisLogger to track operations")
    print(f"4. Review logs/MASTER_LOG.md to monitor progress")
    print(f"\nExample usage:")
    print(f"  python 01_analysis/example_analysis.py")

    return project_path


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new data analysis project with standard structure"
    )
    parser.add_argument(
        "project_name",
        help="Name of the project to create"
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Parent directory where project will be created (default: current directory)"
    )

    args = parser.parse_args()

    try:
        init_project(args.project_name, args.path)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
