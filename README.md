# 🐞🤖 DebuggerAI: LLM-Powered Code Debugger & Tutor

Welcome to **DebuggerAI** — your next-level, teaching-focused AI that not only *fixes* code, but *explains* bugs in plain English! Perfect for learning, pair programming, and codebase health.

---

## 🚀 What is DebuggerAI?

DebuggerAI is an AI-powered tool that:
- Scans your code for bugs, anti-patterns, and suspicious logic
- Explains each issue in human language (not just "replace X with Y")
- Suggests fixes with code
- Optionally explains the *underlying concept* (e.g., "This is a classic off-by-one error")
- Supports multiple languages (Python, C++, JS, Java, ...)
- Outputs beautiful markdown and interactive HTML reports
- Designed to *learn your codebase style* over time
- Lets you rate explanations and fixes for continuous improvement
- Remembers your project/session history and user account
- Handles large codebases with async processing and robust error handling
- Summarizes bug patterns and project health in a dashboard

---

## 🧩 Features

- ✅ Paste/upload code, or analyze entire folders (multi-file, multi-language)
- ✅ User authentication (email/username sign up, login, session management)
- ✅ Project/session history (persistent, per-user)
- ✅ Async static analysis and LLM explanations (fast, scalable)
- ✅ AI scans, finds bugs, anti-patterns, style issues
- ✅ Shows file + line number for each issue
- ✅ Explains why it’s wrong *in plain English* (customizable depth: Beginner, Expert, "Explain like I’m 12")
- ✅ Suggests possible fixes (with code and diffs)
- ✅ Markdown and interactive HTML reports (with collapsible diffs)
- ✅ Feedback loop: rate explanations/fixes, leave comments
- ✅ Codebase style learning and suggestions
- ✅ Bug pattern dashboard (summarizes recurring issues)
- ✅ Robust error handling, logging, and async processing

---

## ⚙️ How to Run

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```sh
   streamlit run DebuggerAI/app.py
   ```

3. **Sign up or log in:**
   - Enter a username, email, and password to create an account, or log in if you already have one.

4. **Analyze code:**
   - Paste code, upload files, or enter a folder path (server-side) to analyze multiple files at once.
   - Select language, explanation depth, and provide your OpenAI API key.
   - Click "Analyze Codebase" to start async analysis.

5. **Review results:**
   - See explanations, fixes, and diffs for each issue.
   - Rate explanations/fixes and leave feedback.
   - Export a beautiful HTML report with one click.
   - View codebase style analysis and bug pattern dashboard.
   - Your session/project history is saved and viewable in the UI.

---

## ✨ Example Prompt

```markdown
You are an AI code tutor.
For this Python function, explain in plain English why there might be a bug, suggest a fix, and explain the concept behind the bug:
```
```python
def divide(a, b):
    return a / b
```

---

## 📦 Requirements

- Python 3.8+
- See `requirements.txt`
- OpenAI API key (for LLM explanations)
- (Optional) clang-tidy, eslint, checkstyle for C++, JS, Java static analysis

---

## 🏁 Quickstart

1. `pip install -r requirements.txt`
2. `streamlit run DebuggerAI/app.py`
3. Sign up, log in, and start analyzing code!

---

## 🛠️ Roadmap

- [x] Multi-language support (C++, JS, Java)
- [x] Learns your codebase style
- [x] Summarizes recurring bug patterns
- [x] "Explain like I’m 12" mode
- [x] VSCode/GitHub integration (coming soon)
- [x] User feedback loop
- [x] Project/session history, user accounts
- [x] Async processing, error handling, logging

---

## 🤝 Contributing

PRs and ideas welcome! Let’s build the future of code learning and debugging together.

---

## © 2024 DebuggerAI 
