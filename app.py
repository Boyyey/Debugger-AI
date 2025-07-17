import streamlit as st
import os
import asyncio
import logging
from input_pipeline import scan_files, SUPPORTED_EXTENSIONS
from static_analysis import StaticAnalyzer
from llm_explainer import LLMExplainer, EXPLANATION_DEPTHS
from report import generate_markdown_report
from style_learning import StyleLearner
from bug_pattern_dashboard import BugPatternSummarizer
from feedback import FeedbackDB
from html_report import generate_html_report
from auth import AuthDB
from session_history import SessionHistoryDB
from async_utils import run_in_executor

logging.basicConfig(filename='debuggerai.log', level=logging.INFO)

def main():
    st.set_page_config(page_title="DebuggerAI: LLM-Powered Debugger", page_icon="🐞🤖")
    st.title("🐞🤖 DebuggerAI: LLM-Powered Code Debugger & Tutor")
    st.markdown("""
    Welcome! Paste code, upload files, or analyze an entire folder. DebuggerAI will find bugs, explain them, and suggest fixes — in plain English!
    """)

    # --- User Authentication ---
    auth_db = AuthDB()
    session_token = st.session_state.get('session_token')
    user = None
    if not session_token:
        auth_mode = st.radio("Auth", ["Sign Up", "Login"])
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if auth_mode == "Sign Up":
            if st.button("Sign Up"):
                if auth_db.signup(username, email, password):
                    st.success("Sign up successful! Please log in.")
                else:
                    st.error("Username or email already exists.")
        else:
            if st.button("Login"):
                token = auth_db.login(username or email, password)
                if token:
                    st.session_state['session_token'] = token
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        st.stop()
    else:
        user = auth_db.get_user_by_token(session_token)
        if not user:
            st.session_state.pop('session_token', None)
            st.rerun()
        st.success(f"Logged in as {user['username']} ({user['email']})")
        if st.button("Logout"):
            st.session_state.pop('session_token', None)
            st.rerun()

    # --- Main App ---
    lang = st.selectbox("Select language", list(SUPPORTED_EXTENSIONS.keys()))
    api_key = st.text_input("Enter your OpenAI API key", type="password")
    depth = st.selectbox("Explanation depth", EXPLANATION_DEPTHS, index=1)
    input_mode = st.radio("Input mode", ["Paste code", "Upload file(s)", "Select folder"])

    code_files = []
    if input_mode == "Paste code":
        code_input = st.text_area("Paste your code here", height=200)
        if code_input.strip():
            code_files.append({'filename': '<input>', 'relpath': '<input>', 'code': code_input})
    elif input_mode == "Upload file(s)":
        uploads = st.file_uploader("Upload code file(s)", type=[ext[1:] for ext in sum(SUPPORTED_EXTENSIONS.values(), [])], accept_multiple_files=True)
        if uploads:
            for file in uploads:
                code = file.read().decode("utf-8")
                code_files.append({'filename': file.name, 'relpath': file.name, 'code': code})
    elif input_mode == "Select folder":
        folder_path = st.text_input("Enter absolute path to folder (server-side)")
        if folder_path and os.path.isdir(folder_path):
            code_files = scan_files(folder_path, lang)
            st.success(f"Found {len(code_files)} {lang} files in {folder_path}")

    # --- Async Analysis ---
    if st.button("Analyze Codebase"):
        if not code_files:
            st.warning("Please provide code input.")
        elif not api_key:
            st.warning("Please enter your OpenAI API key.")
        else:
            all_reports = []
            all_explanations = []
            feedback_db = FeedbackDB()
            session_db = SessionHistoryDB()
            try:
                async def analyze_file(file):
                    findings = await run_in_executor(StaticAnalyzer.analyze_code, file['code'], lang, file['filename'])
                    if not findings:
                        return None, None, None
                    explainer = LLMExplainer(api_key, depth=depth)
                    explanations = await run_in_executor(explainer.explain_findings, file['code'], findings)
                    report_md = generate_markdown_report(file['filename'], explanations)
                    return explanations, report_md, file['filename']
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(asyncio.gather(*[analyze_file(file) for file in code_files]))
                for explanations, report_md, fname in results:
                    if explanations is not None and report_md is not None and fname is not None:
                        all_explanations.append(explanations)
                        all_reports.append(report_md)
                        # Feedback UI for each explanation
                        for ex in explanations:
                            st.markdown(f"#### Feedback for {fname} line {ex['line']}")
                            rating = st.slider(f"Rate the explanation/fix (line {ex['line']})", 1, 5, 3, key=f"rate_{fname}_{ex['line']}")
                            comment = st.text_input(f"Comment (optional) for line {ex['line']}", key=f"comment_{fname}_{ex['line']}")
                            if st.button(f"Submit Feedback for {fname} line {ex['line']}", key=f"submit_{fname}_{ex['line']}"):
                                feedback_db.add_feedback(str(fname), ex['line'], ex['explanation'], ex['fix'], rating, comment)
                                st.success("Feedback submitted!")
                if all_reports:
                    st.markdown("\n---\n".join(all_reports))
                    # HTML report export
                    if st.button("Export HTML Report"):
                        html_report = ''
                        for i, file in enumerate(code_files):
                            html_report += generate_html_report(file['filename'], all_explanations[i])
                        st.download_button("Download HTML Report", html_report, file_name="debuggerai_report.html", mime="text/html")
                else:
                    st.success("No issues found in the provided codebase!")
                # Style learning and suggestions
                style_learner = StyleLearner()
                style_info = style_learner.analyze_codebase(code_files)
                st.markdown("## 🧑‍🎨 Codebase Style Analysis")
                st.json(style_info['metrics'])
                if style_info['suggestions']:
                    st.markdown("### Style Suggestions:")
                    for s in style_info['suggestions']:
                        st.markdown(f"- {s}")
                # Bug pattern dashboard
                bug_summarizer = BugPatternSummarizer()
                bug_summary = bug_summarizer.summarize(all_explanations)
                st.markdown("## 🐛 Bug Pattern Dashboard")
                st.json(bug_summary)
                # Save session history
                if user and 'username' in user:
                    session_db.add_session(user['username'], [f['filename'] for f in code_files], bug_summary['top_patterns'].__str__())
            except Exception as e:
                logging.exception("Error during analysis")
                st.error(f"An error occurred: {e}")

    # --- Project/Session History ---
    st.markdown("## 📜 Project/Session History")
    session_db = SessionHistoryDB()
    if user and 'username' in user:
        sessions = session_db.get_sessions(user['username'])
        for s in sessions:
            st.markdown(f"- **{s[3]}** (Files: {s[2]}) at {s[1]}")

if __name__ == "__main__":
    main() 