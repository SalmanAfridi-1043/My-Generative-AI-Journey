import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Add project root and ui folder to sys.path so imports work in all execution contexts
UI_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = UI_DIR.parent
for p in [str(PROJECT_ROOT), str(UI_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import streamlit as st
from app.services.markdown_service import save_report_as_markdown

# Support both `from components import ...` and `from ui.components import ...`
try:
    from ui.components import (
        load_css,
        render_sidebar_brand,
        render_download_buttons,
        report_to_markdown,
        stream_text,
        run_research,
    )
except ImportError:
    from components import (
        load_css,
        render_sidebar_brand,
        render_download_buttons,
        report_to_markdown,
        stream_text,
        run_research,
    )

st.set_page_config(
    page_title="ResearchPilot AI",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="expanded",
)

load_css()

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "pending_topic" not in st.session_state:
    st.session_state["pending_topic"] = None

if "is_researching" not in st.session_state:
    st.session_state["is_researching"] = False


def process_topic(raw_topic: str) -> None:
    """Core topic handler for user input and suggestion clicks."""
    topic = raw_topic.strip()

    # Append & display user message FIRST before any long-running task
    st.session_state["messages"].append(
        {"role": "user", "type": "text", "content": raw_topic}
    )
    with st.chat_message("user", avatar="🧑"):
        st.markdown(raw_topic)

    # Validate input
    if not topic:
        error_msg = "⚠️ Please enter a valid research topic."
        st.session_state["messages"].append(
            {"role": "assistant", "type": "text", "content": error_msg}
        )
        with st.chat_message("assistant", avatar="🧭"):
            st.markdown(error_msg)
        return

    # Run research with status
    msg_index = len(st.session_state["messages"])
    with st.chat_message("assistant", avatar="🧭"):
        with st.status("Researching...", expanded=True) as status:
            result = run_research(topic)
            if result["success"]:
                status.update(label="Research complete", state="complete")
            else:
                status.update(label="Research failed", state="error")

        if not result["success"]:
            err_msg = (
                f"❌ Something went wrong while researching. Please try again.\n\n"
                f"<small style='color: #9B9B9B;'>Error: {result['error']}</small>"
            )
            st.markdown(err_msg, unsafe_allow_html=True)
            st.session_state["messages"].append(
                {"role": "assistant", "type": "text", "content": err_msg}
            )
        else:
            report = result["data"]["report"]
            report_md = report_to_markdown(report)

            # Stream response word-by-word
            st.write_stream(stream_text(report_md))

            # Save report file
            try:
                saved_path = save_report_as_markdown(report)
            except Exception:
                saved_path = None

            # Render download buttons directly below stream
            report_data = (
                report.model_dump()
                if hasattr(report, "model_dump")
                else (report.dict() if hasattr(report, "dict") else report)
            )
            render_download_buttons(
                report_data, saved_path=saved_path, msg_index=msg_index
            )

            # Store in session state for instant retrieval on rerun
            st.session_state["messages"].append(
                {
                    "role": "assistant",
                    "type": "report",
                    "content": report_md,
                    "report_data": report_data,
                    "saved_path": saved_path,
                }
            )


# Sidebar content
reports_dir = PROJECT_ROOT / "output" / "reports"

with st.sidebar:
    render_sidebar_brand()

    if st.button(
        "+ New Research",
        key="btn_new_research",
        disabled=st.session_state["is_researching"],
        use_container_width=True,
    ):
        st.session_state["messages"] = []
        st.session_state["pending_topic"] = None
        st.session_state["is_researching"] = False
        st.rerun()

    st.markdown(
        "<div class='rp-sidebar-section-title'>PAST REPORTS</div>",
        unsafe_allow_html=True,
    )

    past_files = []
    if reports_dir.exists() and reports_dir.is_dir():
        past_files = sorted(
            [f for f in reports_dir.glob("*.md") if f.is_file()],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )[:10]

    if not past_files:
        st.caption("No saved reports yet.")
    else:
        st.markdown("<div class='rp-past-reports-scroll'>", unsafe_allow_html=True)
        for idx, report_file in enumerate(past_files):
            stem = report_file.stem
            cleaned_stem = re.sub(r"_\d{8}_\d{6}$", "", stem)
            clean_name = cleaned_stem.replace("_", " ").title()

            mtime = datetime.fromtimestamp(report_file.stat().st_mtime)
            formatted_date = mtime.strftime("%d %b %Y, %I:%M %p")

            # Clean name without emoji, date provided in help tooltip
            if st.button(
                clean_name,
                key=f"past_rep_{idx}",
                help=formatted_date,
                disabled=st.session_state["is_researching"],
                use_container_width=True,
            ):
                try:
                    with open(report_file, "r", encoding="utf-8") as rf:
                        content = rf.read()
                    st.session_state["messages"].append(
                        {
                            "role": "assistant",
                            "type": "text",
                            "content": f"### 📚 Past Report: {clean_name}\n\n{content}",
                        }
                    )
                    st.session_state["pending_topic"] = None
                    st.rerun()
                except Exception as read_err:
                    st.error(f"Failed to read report: {read_err}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<p class='rp-sidebar-footer'>Built with LangChain, Tavily and Streamlit.</p>",
        unsafe_allow_html=True,
    )


# 1. Render all existing messages first
for idx, msg in enumerate(st.session_state["messages"]):
    role = msg["role"]
    avatar = "🧑" if role == "user" else "🧭"
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["content"], unsafe_allow_html=True)
        if msg.get("type") == "report":
            render_download_buttons(
                report=msg.get("report_data", {}),
                saved_path=msg.get("saved_path"),
                msg_index=idx,
            )

# 2. Check and handle pending topic (BEFORE rendering suggestions/inputs)
if st.session_state.get("pending_topic") is not None:
    topic_to_run = st.session_state.pop("pending_topic")
    try:
        process_topic(topic_to_run)
    finally:
        st.session_state["is_researching"] = False
        st.rerun()

# 3. Determine if chat is truly in empty state (messages empty AND no pending topic)
chat_is_empty = (
    len(st.session_state["messages"]) == 0
    and st.session_state.get("pending_topic") is None
)

# Placeholder slot for suggestions
suggestions_slot = st.empty()

if chat_is_empty:
    with suggestions_slot.container():
        st.markdown(
            "<div class='rp-empty-hero'>"
            "<h2>What would you like to research?</h2>"
            "</div>",
            unsafe_allow_html=True,
        )

        empty_input = st.chat_input(
            "Ask anything... e.g. Future of Robotics",
            key="empty_chat_input",
            disabled=st.session_state["is_researching"],
        )
        if empty_input is not None:
            st.session_state["pending_topic"] = empty_input
            st.session_state["is_researching"] = True
            suggestions_slot.empty()
            st.rerun()

        st.markdown("<div class='rp-suggestions-container'>", unsafe_allow_html=True)
        suggestions = [
            ("", "AI in Healthcare"),
            ("", "Future of Robotics"),
            ("", "Trends in Hardware Evolution"),
            ("", "Renewable Energy Trends"),
        ]

        for s_idx, (icon, topic_name) in enumerate(suggestions):
            btn_label = f"{icon}  {topic_name}"
            if st.button(
                btn_label,
                key=f"sugg_{s_idx}",
                disabled=st.session_state["is_researching"],
                use_container_width=True,
            ):
                st.session_state["pending_topic"] = topic_name
                st.session_state["is_researching"] = True
                suggestions_slot.empty()
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Chat active: Input pinned at bottom normally
    active_input = st.chat_input(
        "Ask something",
        key="active_chat_input",
        disabled=st.session_state["is_researching"],
    )
    if active_input is not None:
        st.session_state["pending_topic"] = active_input
        st.session_state["is_researching"] = True
        st.rerun()
