import os
from pathlib import Path

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")
LOGO_PATH = str(Path(__file__).parent / "assets" / "esilv_logo.png")

APP_NAME = "ESILV Tutor"
STUDENT_NAME = "Zeineb"
ALL_COURSES = "All courses"
# Label shown in the sidebar -> mode sent to the API
RETRIEVAL_MODES = {"Dense": "dense", "BM25": "bm25", "Hybrid": "hybrid"}

st.set_page_config(page_title=APP_NAME, page_icon=LOGO_PATH, layout="centered")

st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 6rem;
    }

    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E1E1C;
        margin: 0;
    }

    .app-subtitle {
        color: #6B6B6B;
        margin: 0;
    }

    .header-line {
        border: none;
        border-top: 2px solid #D0105A;
        margin: 0.5rem 0 1.5rem 0;
    }

    .empty-state {
        text-align: center;
        color: #6B6B6B;
        margin-top: 4rem;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []


def ask_api(question, course, history, mode):
    response = requests.post(
        f"{API_URL}/ask",
        json={"question": question, "course": course, "history": history, "mode": mode},
        timeout=300
    )
    response.raise_for_status()
    return response.json()


def fetch_courses():
    try:
        response = requests.get(f"{API_URL}/courses", timeout=10)
        response.raise_for_status()
        return response.json()["courses"]
    except requests.RequestException:
        return []


def build_history(messages):
    """Previous messages sent to the API (error messages are left out)."""
    return [
        {"role": m["role"], "content": m["content"]}
        for m in messages
        if not m["content"].startswith("⚠️")
    ]


def show_rewritten(message):
    rewritten = message.get("standalone_question")
    if rewritten:
        st.caption(f"🔎 Understood as: {rewritten}")


def show_sources(sources, mode=None):
    if sources:
        pages = " · ".join(f"{s['file']} (p. {s['page']})" for s in sources)
        # Mode label as in the sidebar (Dense, BM25, Hybrid)
        label = next((name for name, value in RETRIEVAL_MODES.items() if value == mode), None)
        prefix = f"🔍 Mode: {label} · " if label else ""
        st.caption(f"{prefix}📄 Sources: {pages}")


# -------------------------
# Sidebar: courses
# -------------------------

with st.sidebar:
    st.image(LOGO_PATH, width=110)
    st.subheader("My courses")

    uploaded_file = st.file_uploader("Add a course (PDF)", type=["pdf"])

    if st.button("Upload", type="primary", use_container_width=True, disabled=uploaded_file is None):
        try:
            with st.spinner("Indexing course..."):
                response = requests.post(
                    f"{API_URL}/upload",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                    timeout=180
                )
            response.raise_for_status()
            result = response.json()
            st.success(f"{result['message']} ({result['chunks_indexed']} chunks)")
        except requests.RequestException as e:
            st.error(f"Upload failed: {e}")

    st.divider()

    # Fetched after the upload, so a new course appears right away
    selected = st.selectbox("Course", [ALL_COURSES] + fetch_courses())
    selected_course = None if selected == ALL_COURSES else selected

    # Dense = embeddings, BM25 = keywords, Hybrid = both merged with RRF
    selected_mode = RETRIEVAL_MODES[st.radio("Retrieval mode", list(RETRIEVAL_MODES), horizontal=True)]

    st.divider()

    if st.button("New conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# -------------------------
# Header
# -------------------------

logo_col, title_col = st.columns([1, 5], vertical_alignment="center")
with logo_col:
    st.image(LOGO_PATH, width=80)
with title_col:
    st.markdown(
        f'<p class="app-title">{APP_NAME}</p>'
        '<p class="app-subtitle">Ask questions about your courses</p>',
        unsafe_allow_html=True
    )
st.markdown('<hr class="header-line">', unsafe_allow_html=True)


# -------------------------
# Conversation
# -------------------------

if not st.session_state.messages:
    st.markdown(
        f'<p class="empty-state">Hi {STUDENT_NAME} 👋<br>'
        "Upload a course in the sidebar, then ask your question below.</p>",
        unsafe_allow_html=True
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        show_rewritten(message)
        st.markdown(message["content"])
        show_sources(message.get("sources"), message.get("mode"))

question = st.chat_input("Ask a question about your courses...")

if question:
    # History = the messages before this question
    history = build_history(st.session_state.messages)

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    rewritten = None
    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching your courses..."):
                result = ask_api(question, selected_course, history, selected_mode)
            answer, sources = result["answer"], result.get("sources", [])
            mode = result.get("mode", selected_mode)
            if result.get("standalone_question", question) != question:
                rewritten = result["standalone_question"]
        except requests.RequestException as e:
            answer, sources, mode = f"⚠️ Request failed: {e}", [], None
        st.markdown(answer)
        show_sources(sources, mode)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "mode": mode,
        "standalone_question": rewritten,
    })
    st.rerun()
