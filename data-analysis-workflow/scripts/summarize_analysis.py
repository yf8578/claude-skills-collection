#!/usr/bin/env python3
"""
Generate project summary from analysis logs.

Usage:
    python summarize_analysis.py [--project-root .] [--output summary.md]
"""

import argparse
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple


def parse_master_log(log_path: Path) -> List[Dict]:
    """
    Parse MASTER_LOG.md and extract all operations.

    Returns:
        List of operation dictionaries
    """
    if not log_path.exists():
        print(f"Error: {log_path} not found")
        return []

    content = log_path.read_text()
    operations = []

    # Split by operation headers
    operation_blocks = re.split(r'\n### \[(.*?)\] (.*?)\n', content)[1:]

    # Process blocks in groups of 3 (timestamp, operation, content)
    for i in range(0, len(operation_blocks), 3):
        if i + 2 >= len(operation_blocks):
            break

        timestamp = operation_blocks[i]
        operation_name = operation_blocks[i + 1]
        content_block = operation_blocks[i + 2]

        # Extract metadata
        op_dict = {
            'timestamp': timestamp,
            'operation': operation_name,
            'raw_content': content_block
        }

        # Extract type
        type_match = re.search(r'\*\*Type:\*\* (.*?)\n', content_block)
        if type_match:
            op_dict['type'] = type_match.group(1)

        # Extract location
        loc_match = re.search(r'\*\*Location:\*\* `(.*?)`', content_block)
        if loc_match:
            op_dict['location'] = loc_match.group(1)

        # Extract result
        result_match = re.search(r'\*\*Result:\*\* (.*?)\n', content_block)
        if result_match:
            op_dict['result'] = result_match.group(1)

        # Extract key findings
        findings_match = re.search(r'\*\*Key Findings:\*\*\n((?:- .*?\n)+)', content_block)
        if findings_match:
            findings = [f.strip('- ').strip() for f in findings_match.group(1).split('\n') if f.strip()]
            op_dict['findings'] = findings

        # Extract figures
        figs_match = re.search(r'\*\*Figures/Tables Generated:\*\*\n((?:- `.*?`\n)+)', content_block)
        if figs_match:
            figures = [f.strip('- `').strip('`').strip() for f in figs_match.group(1).split('\n') if f.strip()]
            op_dict['figures'] = figures

        operations.append(op_dict)

    return operations


def generate_timeline(operations: List[Dict]) -> str:
    """Generate timeline of operations."""
    timeline = "## Analysis Timeline\n\n"

    # Group by date
    by_date = defaultdict(list)
    for op in operations:
        date = op['timestamp'].split()[0]
        by_date[date].append(op)

    # Format timeline
    for date in sorted(by_date.keys()):
        timeline += f"### {date}\n\n"
        for op in by_date[date]:
            time = op['timestamp'].split()[1] if len(op['timestamp'].split()) > 1 else ""
            op_type = op.get('type', 'Unknown')
            timeline += f"- **{time}** [{op_type}] {op['operation']}\n"
        timeline += "\n"

    return timeline


def generate_operations_summary(operations: List[Dict]) -> str:
    """Generate summary of operations by type."""
    summary = "## Operations Summary\n\n"

    # Group by type
    by_type = defaultdict(list)
    for op in operations:
        op_type = op.get('type', 'Unknown')
        by_type[op_type].append(op)

    # Count by type
    summary += "### Operation Types\n\n"
    summary += "| Type | Count |\n"
    summary += "|------|-------|\n"
    for op_type in sorted(by_type.keys()):
        count = len(by_type[op_type])
        summary += f"| {op_type} | {count} |\n"

    summary += "\n### Recent Operations (Last 10)\n\n"
    for op in operations[-10:]:
        timestamp = op['timestamp']
        operation = op['operation']
        location = op.get('location', 'N/A')
        summary += f"- **[{timestamp}]** {operation}\n"
        summary += f"  - Location: `{location}`\n"
        if 'result' in op:
            summary += f"  - Result: {op['result']}\n"
        summary += "\n"

    return summary


def generate_findings_summary(operations: List[Dict]) -> str:
    """Generate summary of all key findings."""
    summary = "## Key Findings\n\n"

    all_findings = []
    for op in operations:
        if 'findings' in op:
            for finding in op['findings']:
                all_findings.append({
                    'timestamp': op['timestamp'],
                    'operation': op['operation'],
                    'finding': finding
                })

    if not all_findings:
        summary += "*No key findings recorded yet.*\n\n"
        return summary

    summary += f"**Total findings recorded:** {len(all_findings)}\n\n"

    # Group by operation
    summary += "### Findings by Operation\n\n"
    for item in all_findings:
        summary += f"#### {item['operation']} ({item['timestamp']})\n"
        summary += f"- {item['finding']}\n\n"

    return summary


def generate_outputs_inventory(operations: List[Dict], project_root: Path) -> str:
    """Generate inventory of all outputs (figures, tables, models)."""
    inventory = "## Outputs Inventory\n\n"

    # Collect all figures
    all_figures = []
    for op in operations:
        if 'figures' in op:
            for fig in op['figures']:
                all_figures.append({
                    'path': fig,
                    'operation': op['operation'],
                    'timestamp': op['timestamp']
                })

    # Figures
    inventory += "### Figures and Tables\n\n"
    if all_figures:
        inventory += "| File | Created | Operation |\n"
        inventory += "|------|---------|----------|\n"
        for fig in all_figures:
            path = Path(fig).name
            timestamp = fig['timestamp'].split()[0]
            operation = fig['operation']
            inventory += f"| `{path}` | {timestamp} | {operation} |\n"
    else:
        inventory += "*No figures recorded yet.*\n"

    inventory += "\n"

    # Scan results directory
    results_dir = project_root / "03_results"
    if results_dir.exists():
        inventory += "### Files in 03_results/\n\n"

        # Count files by subdirectory
        for subdir in ['figures', 'tables', 'statistics']:
            subdir_path = results_dir / subdir
            if subdir_path.exists():
                files = list(subdir_path.glob('*'))
                files = [f for f in files if f.is_file()]
                inventory += f"- **{subdir}/**: {len(files)} files\n"

        inventory += "\n"

    # Scan models directory
    models_dir = project_root / "05_models"
    if models_dir.exists():
        model_dirs = [d for d in models_dir.iterdir() if d.is_dir()]
        inventory += f"### Models ({len(model_dirs)} versions)\n\n"
        for model_dir in sorted(model_dirs):
            inventory += f"- `{model_dir.name}/`\n"

    inventory += "\n"

    return inventory


def generate_next_steps(project_root: Path) -> str:
    """Extract next steps from analysis logs."""
    next_steps_section = "## Next Steps\n\n"

    analysis_dir = project_root / "01_analysis"
    if not analysis_dir.exists():
        return next_steps_section + "*No analysis logs found.*\n\n"

    all_next_steps = []

    # Find all analysis_log.md files
    for log_file in analysis_dir.glob("*/analysis_log.md"):
        content = log_file.read_text()

        # Extract next steps section
        match = re.search(r'## Next Steps\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if match:
            steps_text = match.group(1).strip()
            if steps_text and "TODO" not in steps_text:
                analysis_name = log_file.parent.name
                all_next_steps.append({
                    'analysis': analysis_name,
                    'steps': steps_text
                })

    if not all_next_steps:
        next_steps_section += "*No next steps recorded yet.*\n\n"
        return next_steps_section

    for item in all_next_steps:
        next_steps_section += f"### {item['analysis']}\n\n"
        next_steps_section += item['steps'] + "\n\n"

    return next_steps_section


def generate_summary(project_root: Path, output_path: Path):
    """Generate complete project summary."""
    project_root = Path(project_root)
    master_log = project_root / "logs" / "MASTER_LOG.md"

    print(f"Generating summary for: {project_root}")
    print(f"Reading: {master_log}")

    # Parse master log
    operations = parse_master_log(master_log)
    print(f"Found {len(operations)} operations")

    # Generate summary sections
    project_name = project_root.name
    summary = f"# Analysis Summary: {project_name}\n\n"
    summary += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    summary += f"**Total Operations:** {len(operations)}\n\n"

    summary += "---\n\n"
    summary += generate_timeline(operations)
    summary += "---\n\n"
    summary += generate_operations_summary(operations)
    summary += "---\n\n"
    summary += generate_findings_summary(operations)
    summary += "---\n\n"
    summary += generate_outputs_inventory(operations, project_root)
    summary += "---\n\n"
    summary += generate_next_steps(project_root)

    # Write summary
    output_path.write_text(summary)
    print(f"\n✓ Summary written to: {output_path}")

    # Print preview
    print("\n" + "="*60)
    print("SUMMARY PREVIEW")
    print("="*60)
    print(summary[:1000])
    if len(summary) > 1000:
        print(f"\n... ({len(summary) - 1000} more characters)")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description="Generate project summary from analysis logs"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Root directory of the project (default: current directory)"
    )
    parser.add_argument(
        "--output",
        default="ANALYSIS_SUMMARY.md",
        help="Output file path (default: ANALYSIS_SUMMARY.md)"
    )

    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    output_path = project_root / args.output

    try:
        generate_summary(project_root, output_path)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
