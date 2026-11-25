# ResearchPilot AI - UI components
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Generator, Union
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.research_service import conduct_research


def load_css() -> None:
    """Read styles.css and inject it into the page."""
    css_path = Path(__file__).parent / "styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def get_logo_base64() -> str:
    """Read logo.svg and return base64 encoded data URI."""
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.svg")
    with open(logo_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


def render_sidebar_brand() -> None:
    """
    Renders branding in the sidebar:
    44px x 44px vibrant flat green logo badge next to 'ResearchPilot AI' (18px, bold, white).
    """
    data_uri = get_logo_base64()
    st.sidebar.markdown(
        f"""
        <div class="rp-sidebar-header">
            <div class="rp-sidebar-logo">
                <img src="{data_uri}" width="44" height="44" alt="Logo" style="width:44px;height:44px;display:block;" />
            </div>
            <div class="rp-sidebar-title">ResearchPilot AI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def report_to_markdown(report: Union[dict, Any]) -> str:
    """
    Converts structured report fields into clean Markdown.
    Only includes fields that actually exist and skips empty ones.
    """
    def get_val(key, default=None):
        if isinstance(report, dict):
            return report.get(key, default)
        return getattr(report, key, default)

    topic = get_val("topic", "Research Topic")
    lines = [f"# 📄 Research Report: {topic}\n"]

    exec_summary = get_val("executive_summary")
    if exec_summary:
        lines.append("### 📝 Executive Summary\n")
        lines.append(f"{exec_summary}\n")

    key_findings = get_val("key_findings")
    if key_findings:
        lines.append("### 🔑 Key Findings\n")
        for i, finding in enumerate(key_findings, start=1):
            lines.append(f"{i}. {finding}")
        lines.append("")

    insights = get_val("important_insights")
    if insights:
        lines.append("### 💡 Important Insights\n")
        for insight in insights:
            lines.append(f"- {insight}")
        lines.append("")

    methodology = get_val("research_methodology")
    if methodology:
        lines.append("### 🔬 Research Methodology\n")
        lines.append(f"{methodology}\n")

    limitations = get_val("limitations")
    if limitations:
        lines.append("### ⚠️ Limitations\n")
        for lim in limitations:
            lines.append(f"- {lim}")
        lines.append("")

    conclusion = get_val("conclusion")
    if conclusion:
        lines.append("### ✅ Conclusion\n")
        lines.append(f"{conclusion}\n")

    sources = get_val("sources")
    if sources:
        lines.append("### 🔗 Sources\n")
        for i, src in enumerate(sources, start=1):
            title = src.get("title") if isinstance(src, dict) else getattr(src, "title", "Source")
            url = src.get("url") if isinstance(src, dict) else getattr(src, "url", "#")
            lines.append(f"{i}. [{title}]({url})")
        lines.append("")

    return "\n".join(lines)


def stream_text(text: str) -> Generator[str, None, None]:
    """Yields text in small chunks (a few words) with time.sleep(0.02) to simulate streaming."""
    words = text.split(" ")
    chunk_size = 3
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i : i + chunk_size])
        if i + chunk_size < len(words):
            chunk += " "
        yield chunk
        time.sleep(0.02)


def render_download_buttons(report: Union[dict, Any], saved_path: str = None, msg_index: int = 0) -> None:
    """Renders small secondary style download buttons under a report."""
    def get_val(key, default=None):
        if isinstance(report, dict):
            return report.get(key, default)
        return getattr(report, key, default)

    topic = get_val("topic", "Research Topic")
    if hasattr(report, "model_dump"):
        report_dict = report.model_dump()
    elif hasattr(report, "dict"):
        report_dict = report.dict()
    elif isinstance(report, dict):
        report_dict = report
    else:
        report_dict = {"topic": topic}

    json_str = json.dumps(report_dict, indent=2, ensure_ascii=False)
    file_base = topic.lower().strip().replace(" ", "_")

    md_content = None
    if saved_path and os.path.isfile(saved_path):
        try:
            with open(saved_path, "r", encoding="utf-8") as f:
                md_content = f.read()
        except Exception:
            md_content = None

    if not md_content:
        # Fallback to generated markdown content
        md_content = report_to_markdown(report_dict)

    col1, col2, _ = st.columns([1, 1, 2])
    with col1:
        st.download_button(
            label="⬇️ Markdown",
            data=md_content,
            file_name=f"{file_base}_report.md",
            mime="text/markdown",
            key=f"dl_md_{msg_index}",
            use_container_width=True,
        )
    with col2:
        st.download_button(
            label="⬇️ JSON",
            data=json_str,
            file_name=f"{file_base}_report.json",
            mime="application/json",
            key=f"dl_json_{msg_index}",
            use_container_width=True,
        )


def run_research(topic: str) -> dict:
    """
    Calls the existing research function and catches exceptions,
    returning a structured dictionary with success status and results/errors.
    """
    try:
        result = conduct_research(topic)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
