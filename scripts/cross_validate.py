#!/usr/bin/env python3
"""
Cross-validate numeric data and terminology across policy/planning documents.

Usage:
    python cross_validate.py <project_folder> [--term-check] [--num-check] [--budget-check]

Default: all checks enabled
"""

import sys
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set


class CrossValidator:
    """Validate consistency across policy documents."""

    UNITS = {
        '억원': 100000000,
        '만원': 10000,
        '%': 1,
        '명': 1,
        '개': 1,
    }

    METRIC_KEYWORDS = {
        '예산', '투자', '기금', '자금', '비용', '지출',
        '인원', '명수', '대상자', '수혜자', '참여자',
        '비율', '비중', '증가', '감소', '목표',
    }

    BUDGET_KEYWORDS = {'예산', '재원', '자금', '투자', '지출'}

    def __init__(self, project_folder: str):
        self.project_folder = Path(project_folder)
        if not self.project_folder.exists():
            raise ValueError(f"Project folder not found: {project_folder}")

        self.files = list(self.project_folder.glob('**/*.md'))
        if not self.files:
            raise ValueError(f"No .md files found in {project_folder}")

        self.file_contents = {}
        self._load_files()

    def _load_files(self):
        """Load all markdown files."""
        for fpath in self.files:
            try:
                self.file_contents[str(fpath)] = fpath.read_text(encoding='utf-8')
            except Exception as e:
                print(f"Warning: Could not read {fpath}: {e}", file=sys.stderr)

    def numeric_check(self) -> List[Dict]:
        """Extract numbers with units and find mismatches across files."""
        results = []
        metrics = defaultdict(dict)  # metric_key -> {file -> values}

        # Pattern: number + optional space + unit
        pattern = r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(' + '|'.join(re.escape(u) for u in self.UNITS.keys()) + r')'

        for fpath, content in self.file_contents.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                value_str, unit = match.groups()
                value = float(value_str.replace(',', ''))

                # Extract context (30 chars before and after)
                start = max(0, match.start() - 30)
                end = min(len(content), match.end() + 30)
                context = content[start:end].strip()

                # Try to identify metric from context
                metric_name = None
                for keyword in self.METRIC_KEYWORDS:
                    if keyword in context:
                        metric_name = keyword
                        break

                if not metric_name:
                    metric_name = "기타"

                metric_key = f"{metric_name}_{unit}"
                if metric_key not in metrics:
                    metrics[metric_key] = {}
                if fpath not in metrics[metric_key]:
                    metrics[metric_key][fpath] = []
                metrics[metric_key][fpath].append((value, context))

        # Find mismatches: same metric with different values
        for metric_key, file_values in metrics.items():
            if len(file_values) > 1:
                all_values = []
                for fpath, values in file_values.items():
                    for val, ctx in values:
                        all_values.append((fpath, val, ctx))

                # Check for value mismatches
                unique_values = set(v[1] for v in all_values)
                if len(unique_values) > 1:
                    for i, (f1, v1, c1) in enumerate(all_values):
                        for f2, v2, c2 in all_values[i+1:]:
                            if v1 != v2:
                                results.append({
                                    'File1': Path(f1).name,
                                    'File2': Path(f2).name,
                                    'Metric': metric_key,
                                    'Value1': str(v1),
                                    'Value2': str(v2),
                                    'Type': 'numeric_mismatch',
                                    'Context1': c1,
                                    'Context2': c2,
                                })

        return results

    def term_check(self) -> List[Dict]:
        """Find potential term inconsistencies."""
        results = []
        term_map = defaultdict(lambda: defaultdict(Counter))  # term -> {file -> Counter}

        # Extract Korean words and phrases
        korean_pattern = r'[가-힣]+(?:\s+[가-힣]+)*'
        english_pattern = r'[A-Za-z]+(?:\s+[A-Za-z]+)*'

        for fpath, content in self.file_contents.items():
            fname = Path(fpath).name

            # Extract Korean terms
            korean_matches = re.findall(korean_pattern, content)
            for term in korean_matches:
                if len(term) >= 2:  # Only meaningful terms
                    term_map['korean'][fname][term] += 1

            # Extract English terms
            english_matches = re.findall(english_pattern, content)
            for term in english_matches:
                if len(term) >= 3:  # Only meaningful terms
                    term_map['english'][fname][term] += 1

        # Find potential inconsistencies
        # 1. Similar Korean terms used in same context
        korean_terms = term_map.get('korean', {})
        if len(korean_terms) > 1:
            all_korean = set()
            for fname, counter in korean_terms.items():
                all_korean.update(counter.keys())

            # Find semantically similar terms (simple heuristic: shared characters)
            terms_list = sorted(all_korean)
            for i, term1 in enumerate(terms_list):
                for term2 in terms_list[i+1:]:
                    # Check if terms share significant overlap (e.g., 청년, 청년층)
                    overlap = len(set(term1) & set(term2))
                    if overlap >= len(min(term1, term2)) * 0.5:
                        in_files1 = [f for f, c in korean_terms.items() if term1 in c]
                        in_files2 = [f for f, c in korean_terms.items() if term2 in c]
                        common_files = set(in_files1) & set(in_files2)
                        if common_files:
                            results.append({
                                'File1': common_files.pop() if common_files else 'N/A',
                                'File2': list(common_files)[0] if common_files else 'N/A',
                                'Metric': f"{term1} vs {term2}",
                                'Value1': str(korean_terms[in_files1[0]][term1]) if in_files1 else '0',
                                'Value2': str(korean_terms[in_files2[0]][term2]) if in_files2 else '0',
                                'Type': 'term_variation',
                            })

        return results

    def budget_check(self) -> List[Dict]:
        """Validate budget consistency."""
        results = []
        budget_pattern = r'(?:' + '|'.join(re.escape(k) for k in self.BUDGET_KEYWORDS) + r')\s*:?\s*(\d+(?:,\d{3})*(?:\.\d+)?)\s*(' + '|'.join(re.escape(u) for u in self.UNITS.keys()) + r')?'

        file_budgets = {}

        for fpath, content in self.file_contents.items():
            fname = Path(fpath).name
            matches = re.finditer(budget_pattern, content)
            total = 0
            found_values = []

            for match in matches:
                value_str = match.group(1)
                unit = match.group(2) if match.group(2) else '원'

                value = float(value_str.replace(',', ''))

                # Normalize to base unit (원)
                if unit in self.UNITS:
                    normalized = value * self.UNITS[unit]
                else:
                    normalized = value

                total += normalized
                found_values.append((value, unit))

            if found_values:
                file_budgets[fname] = {
                    'total': total,
                    'values': found_values,
                    'file_path': fpath,
                }

        # Compare budgets across files
        fnames = sorted(file_budgets.keys())
        for i, fname1 in enumerate(fnames):
            for fname2 in fnames[i+1:]:
                b1 = file_budgets[fname1]['total']
                b2 = file_budgets[fname2]['total']

                # Allow 10% margin for rounding
                if abs(b1 - b2) > max(b1, b2) * 0.1:
                    results.append({
                        'File1': fname1,
                        'File2': fname2,
                        'Metric': 'total_budget',
                        'Value1': f"{b1:,.0f}",
                        'Value2': f"{b2:,.0f}",
                        'Type': 'budget_mismatch',
                    })

        return results

    def run(self, checks: Set[str]) -> int:
        """Run selected checks and output results."""
        all_results = []

        if 'num' in checks:
            print("Running numeric check...", file=sys.stderr)
            all_results.extend(self.numeric_check())

        if 'term' in checks:
            print("Running term check...", file=sys.stderr)
            all_results.extend(self.term_check())

        if 'budget' in checks:
            print("Running budget check...", file=sys.stderr)
            all_results.extend(self.budget_check())

        # Output results
        if not all_results:
            print("No mismatches found.", file=sys.stderr)
            return 0

        # Print header
        print(
            f"{'File1':<30} | {'File2':<30} | {'Metric':<25} | "
            f"{'Value1':<15} | {'Value2':<15} | {'Type':<20}"
        )
        print("-" * 150)

        # Print results
        for result in all_results:
            print(
                f"{result['File1']:<30} | {result['File2']:<30} | "
                f"{result['Metric']:<25} | {result['Value1']:<15} | "
                f"{result['Value2']:<15} | {result['Type']:<20}"
            )

        print(f"\nTotal mismatches found: {len(all_results)}", file=sys.stderr)
        return 1


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python cross_validate.py <project_folder> [--term-check] [--num-check] [--budget-check]")
        print("Default: all checks enabled")
        sys.exit(1)

    project_folder = sys.argv[1]
    flags = set(sys.argv[2:]) if len(sys.argv) > 2 else {'--term-check', '--num-check', '--budget-check'}

    # Normalize flag names
    checks = set()
    if '--num-check' in flags or not flags or flags == set():
        checks.add('num')
    if '--term-check' in flags or not flags or flags == set():
        checks.add('term')
    if '--budget-check' in flags or not flags or flags == set():
        checks.add('budget')

    # If specific flags provided, use only those
    if flags and flags != set():
        checks = set()
        if '--num-check' in flags:
            checks.add('num')
        if '--term-check' in flags:
            checks.add('term')
        if '--budget-check' in flags:
            checks.add('budget')

    try:
        validator = CrossValidator(project_folder)
        exit_code = validator.run(checks)
        sys.exit(exit_code)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
