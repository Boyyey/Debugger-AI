from typing import List, Dict
import difflib

def generate_markdown_report(filename: str, explanations: List[Dict]) -> str:
    report = [f"# 🐞 DebuggerAI Report for `{filename}`\n"]
    for ex in explanations:
        report.append(f"## Issue at line {ex['line']} ({ex['type']})\n")
        report.append(f"**Error message:** {ex['message']}\n")
        report.append(f"**Explanation:**\n\n{ex['explanation']}\n")
        if ex.get('fix'):
            report.append(f"**Suggested fix:**\n\n```python\n{ex['fix']}\n```\n")
            # Show diff if fix is present
            orig_lines = ex['explanation'].splitlines()
            fix_lines = ex['fix'].splitlines()
            diff = difflib.unified_diff(orig_lines, fix_lines, fromfile='original', tofile='fix', lineterm='')
            diff_text = '\n'.join(diff)
            if diff_text:
                report.append(f"**Diff:**\n\n```diff\n{diff_text}\n```\n")
        report.append('---')
    return '\n'.join(report) 