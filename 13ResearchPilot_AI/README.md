# 🧭 ResearchPilot AI

ResearchPilot AI is an intelligent research assistant built with **LangChain**, **OpenAI**, and **Tavily Search**. It conducts deep web research on any given topic, analyzes source data, and produces clean, structured markdown research reports.

---

## 🖥️ Web UI (Streamlit)

A modern, chat-style interface for ResearchPilot AI designed for conversational research workflows.

![ResearchPilot AI UI](ui/assets/screenshot.png)

### Features
- **💬 Chat Layout**: Intuitive user and assistant chat bubbles with status indicators.
- **⚡ Example Topics**: Quick one-click starter topic suggestions right under the welcome greeting.
- **📄 Formatted Report**: Structured formal report layout highlighting Executive Summary, Key Findings, Insights, Methodology, Limitations, Conclusion, and Reference links.
- **⬇️ Report Downloads**: One-click **Markdown (.md)** and **JSON (.json)** file downloads.
- **📚 Past Reports**: Sidebar navigation displaying the 5 most recent reports saved in `output/reports/` for quick review without re-running queries.

### How to Run the Web UI
```bash
pip install -r requirements.txt
streamlit run ui/streamlit_app.py
```

---

## 💻 Terminal Application

The original command-line interface remains fully functional:

```bash
python -m app.main
```

---

## 📁 Project Structure

```text
13ResearchPilot_AI/
├── .env
├── .streamlit/
│   └── config.toml
├── app/
│   ├── config/
│   │   └── settings.py
│   ├── core/
│   │   └── llm.py
│   ├── prompts/
│   │   └── report_prompt.py
│   ├── schemas/
│   │   └── report_schema.py
│   ├── services/
│   │   ├── markdown_service.py
│   │   ├── report_service.py
│   │   └── research_service.py
│   ├── tools/
│   │   └── search_tool.py
│   ├── utils/
│   │   └── helpers.py
│   └── main.py
├── output/
│   └── reports/
├── ui/
│   ├── __init__.py
│   ├── streamlit_app.py
│   ├── components.py
│   ├── styles.css
│   └── assets/
│       ├── logo.svg
│       └── screenshot.png
├── requirements.txt
└── README.md
```
