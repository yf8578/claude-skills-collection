#!/usr/bin/env python3
"""
AnalysisLogger - Automatic logging for data analysis workflows

This module provides the AnalysisLogger class for systematically recording
all operations, decisions, and results in a data analysis project.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any


class AnalysisLogger:
    """
    Automatic logging system for data analysis projects.

    Records all operations, decisions, and results to standardized log files
    with timestamps and detailed metadata.

    Example:
        >>> logger = AnalysisLogger(project_root=".")
        >>> logger.log_operation(
        ...     operation="Data cleaning",
        ...     location="02_processed_data/cleaned.csv",
        ...     params={"method": "remove_outliers"},
        ...     result="Removed 47 outliers",
        ...     key_findings=["Most outliers in age column"]
        ... )
    """

    def __init__(self, project_root: str = "."):
        """
        Initialize the logger.

        Args:
            project_root: Root directory of the analysis project
        """
        self.project_root = Path(project_root)
        self.logs_dir = self.project_root / "logs"
        self.master_log = self.logs_dir / "MASTER_LOG.md"
        self.decisions_log = self.logs_dir / "decisions.md"
        self.errors_log = self.logs_dir / "errors.md"

        # Ensure logs directory exists
        self.logs_dir.mkdir(exist_ok=True)

        # Initialize master log if it doesn't exist
        if not self.master_log.exists():
            self._initialize_master_log()

    def _initialize_master_log(self):
        """Create initial master log file."""
        project_name = self.project_root.resolve().name
        content = f"""# Project: {project_name}
**Created:** {datetime.now().strftime('%Y-%m-%d')}
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Operation Log

"""
        self.master_log.write_text(content)

    def _update_timestamp(self):
        """Update the 'Last Updated' timestamp in master log."""
        content = self.master_log.read_text()
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('**Last Updated:**'):
                lines[i] = f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                break
        self.master_log.write_text('\n'.join(lines))

    def log_operation(
        self,
        operation: str,
        location: str,
        operation_type: str = "Analysis",
        params: Optional[Dict[str, Any]] = None,
        result: Optional[str] = None,
        key_findings: Optional[List[str]] = None,
        figures: Optional[List[str]] = None,
        notes: Optional[str] = None
    ):
        """
        Log an analysis operation to the master log.

        Args:
            operation: Name/description of the operation
            location: File path where operation was performed or output saved
            operation_type: Type of operation (Analysis, Data Processing, Modeling, Visualization)
            params: Dictionary of parameters used
            result: Brief description of the outcome
            key_findings: List of important findings from this operation
            figures: List of figure/table paths generated
            notes: Additional context or observations
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Build the log entry
        entry = f"\n### [{timestamp}] {operation}\n"
        entry += f"**Type:** {operation_type}\n"
        entry += f"**Location:** `{location}`\n"

        if params:
            entry += "**Parameters:**\n"
            for key, value in params.items():
                entry += f"- {key}: {value}\n"
            entry += "\n"

        if result:
            entry += f"**Result:** {result}\n"

        if key_findings:
            entry += "**Key Findings:**\n"
            for finding in key_findings:
                entry += f"- {finding}\n"
            entry += "\n"

        if figures:
            entry += "**Figures/Tables Generated:**\n"
            for fig in figures:
                entry += f"- `{fig}`\n"
            entry += "\n"

        if notes:
            entry += f"**Notes:** {notes}\n"

        entry += "\n---\n"

        # Append to master log
        with open(self.master_log, 'a') as f:
            f.write(entry)

        # Update timestamp
        self._update_timestamp()

        print(f"✓ Logged: {operation}")

    def log_decision(
        self,
        question: str,
        decision: str,
        reasoning: str,
        alternatives: Optional[List[str]] = None,
        references: Optional[List[str]] = None,
        impact: Optional[str] = None
    ):
        """
        Log an analytical decision.

        Args:
            question: The question or decision point
            decision: What was decided
            reasoning: Why this decision was made
            alternatives: Other options considered (and why rejected)
            references: Citations or sources supporting the decision
            impact: Expected impact on the analysis
        """
        timestamp = datetime.now().strftime('%Y-%m-%d')

        # Initialize decisions log if needed
        if not self.decisions_log.exists():
            self.decisions_log.write_text("# Analytical Decisions Log\n\n")

        # Build the entry
        entry = f"\n## [{timestamp}] {question}\n\n"
        entry += f"**Decision:** {decision}\n\n"
        entry += f"**Reasoning:**\n{reasoning}\n\n"

        if alternatives:
            entry += "**Alternatives Considered:**\n"
            for alt in alternatives:
                entry += f"- {alt}\n"
            entry += "\n"

        if references:
            entry += "**References:**\n"
            for ref in references:
                entry += f"- {ref}\n"
            entry += "\n"

        if impact:
            entry += f"**Impact:** {impact}\n\n"

        entry += "---\n"

        # Append to decisions log
        with open(self.decisions_log, 'a') as f:
            f.write(entry)

        print(f"✓ Decision logged: {question}")

    def log_error(
        self,
        error_type: str,
        description: str,
        resolution: Optional[str] = None,
        code_snippet: Optional[str] = None
    ):
        """
        Log an error and its resolution.

        Args:
            error_type: Type/category of error
            description: Description of what went wrong
            resolution: How the error was fixed
            code_snippet: Code that caused the error (if relevant)
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Initialize errors log if needed
        if not self.errors_log.exists():
            self.errors_log.write_text("# Error Log\n\n")

        # Build the entry
        entry = f"\n## [{timestamp}] {error_type}\n\n"
        entry += f"**Description:** {description}\n\n"

        if code_snippet:
            entry += f"**Code:**\n```python\n{code_snippet}\n```\n\n"

        if resolution:
            entry += f"**Resolution:** {resolution}\n\n"
        else:
            entry += "**Resolution:** UNRESOLVED\n\n"

        entry += "---\n"

        # Append to errors log
        with open(self.errors_log, 'a') as f:
            f.write(entry)

        status = "resolved" if resolution else "UNRESOLVED"
        print(f"✓ Error logged ({status}): {error_type}")

    def create_analysis_log(
        self,
        analysis_name: str,
        input_data: List[str],
        methods: List[str],
        results: Optional[Dict[str, Any]] = None,
        next_steps: Optional[List[str]] = None,
        notes: Optional[str] = None,
        analyst: str = "Unknown"
    ) -> Path:
        """
        Create a new timestamped analysis directory with analysis_log.md.

        Args:
            analysis_name: Descriptive name for this analysis
            input_data: List of input file paths
            methods: List of methods/techniques used
            results: Dictionary of results and statistics
            next_steps: List of next actions to take
            notes: Additional notes or observations
            analyst: Name of person conducting analysis

        Returns:
            Path to the created analysis directory
        """
        # Create timestamped directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        analysis_dir = self.project_root / "01_analysis" / f"{timestamp}_{analysis_name}"
        analysis_dir.mkdir(parents=True, exist_ok=True)

        # Create outputs subdirectory
        (analysis_dir / "outputs").mkdir(exist_ok=True)

        # Create analysis log
        log_path = analysis_dir / "analysis_log.md"

        content = f"""# Analysis: {analysis_name}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Analyst:** {analyst}
**Status:** In Progress

## Objective
{notes if notes else 'TODO: Add analysis objective'}

## Input Data
"""
        for data in input_data:
            content += f"- `{data}`\n"

        content += "\n## Methods\n"
        for i, method in enumerate(methods, 1):
            content += f"{i}. {method}\n"

        content += "\n## Results\n"
        if results:
            content += "### Key Statistics\n"
            for key, value in results.items():
                content += f"- {key}: {value}\n"
        else:
            content += "TODO: Add results\n"

        content += "\n### Figures\nTODO: Add figure paths and descriptions\n"

        content += "\n## Key Findings\nTODO: Add key findings\n"

        content += "\n## Next Steps\n"
        if next_steps:
            for step in next_steps:
                content += f"- [ ] {step}\n"
        else:
            content += "TODO: Add next steps\n"

        content += "\n## Notes\nTODO: Add additional notes\n"

        log_path.write_text(content)

        # Log to master log
        self.log_operation(
            operation=f"Created analysis: {analysis_name}",
            location=str(analysis_dir),
            operation_type="Analysis Setup",
            notes=f"Analysis directory created with log file"
        )

        print(f"✓ Analysis created: {analysis_dir}")
        return analysis_dir


def extract_methods(
    log_path: str = "logs/MASTER_LOG.md",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    format: str = "markdown"
) -> str:
    """
    Extract methods text from operation logs for manuscript writing.

    Args:
        log_path: Path to MASTER_LOG.md
        start_date: Start date filter (YYYY-MM-DD)
        end_date: End date filter (YYYY-MM-DD)
        format: Output format ('markdown' or 'latex')

    Returns:
        Formatted methods text
    """
    with open(log_path, 'r') as f:
        content = f.read()

    # Extract operations (simple implementation)
    operations = []
    for line in content.split('\n'):
        if line.startswith('### ['):
            # Extract timestamp and operation name
            timestamp = line.split(']')[0].replace('### [', '')
            operation = line.split(']')[1].strip()

            # Filter by date if specified
            if start_date and timestamp.split()[0] < start_date:
                continue
            if end_date and timestamp.split()[0] > end_date:
                continue

            operations.append(operation)

    # Format output
    if format == "markdown":
        methods_text = "## Methods\n\n"
        methods_text += "The following operations were performed:\n\n"
        for op in operations:
            methods_text += f"- {op}\n"
    elif format == "latex":
        methods_text = "\\section{Methods}\n\n"
        methods_text += "The following operations were performed:\n\n"
        methods_text += "\\begin{itemize}\n"
        for op in operations:
            methods_text += f"  \\item {op}\n"
        methods_text += "\\end{itemize}\n"
    else:
        methods_text = "\n".join(operations)

    return methods_text


if __name__ == "__main__":
    # Example usage
    print("AnalysisLogger - Data Analysis Workflow Helper")
    print("\nExample usage:")
    print("""
from data_analysis_workflow.log_helper import AnalysisLogger

logger = AnalysisLogger(project_root=".")

# Log an operation
logger.log_operation(
    operation="Data cleaning",
    location="02_processed_data/cleaned_data.csv",
    params={"method": "remove_outliers", "threshold": 3},
    result="Removed 47 outliers (2.3%)",
    key_findings=["Most outliers in age column"]
)

# Log a decision
logger.log_decision(
    question="Which test to use?",
    decision="Welch's t-test",
    reasoning="Unequal variances detected"
)

# Create analysis session
logger.create_analysis_log(
    analysis_name="exploratory_analysis",
    input_data=["00_raw_data/dataset.csv"],
    methods=["Summary statistics", "Correlation analysis"]
)
    """)
