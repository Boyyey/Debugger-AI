from typing import List, Dict
import difflib

def generate_html_report(filename: str, explanations: List[Dict]) -> str:
    html = [f'<h1>🐞 DebuggerAI Report for <code>{filename}</code></h1>']
    for ex in explanations:
        html.append(f'<h2>Issue at line {ex["line"]} ({ex["type"]})</h2>')
        html.append(f'<b>Error message:</b> {ex["message"]}<br>')
        html.append(f'<b>Explanation:</b><pre>{ex["explanation"]}</pre>')
        if ex.get('fix'):
            html.append(f'<b>Suggested fix:</b><pre>{ex["fix"]}</pre>')
            orig_lines = ex['explanation'].splitlines()
            fix_lines = ex['fix'].splitlines()
            diff = difflib.unified_diff(orig_lines, fix_lines, fromfile='original', tofile='fix', lineterm='')
            diff_text = '\n'.join(diff)
            if diff_text:
                html.append(f'<details><summary>Show Diff</summary><pre style="background:#f8f8f8">{diff_text}</pre></details>')
        html.append('<hr>')
    return '\n'.join(html) 