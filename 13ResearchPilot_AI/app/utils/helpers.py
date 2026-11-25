def format_research_report(report) -> str:
    """
    Format a structured research report into a professional
    terminal-friendly layout.
    """

    output = []

    width = 70

    def add_section(number, title):
        output.append("")
        output.append("-" * width)
        output.append(f"{number}. {title}")
        output.append("-" * width)

    def add_list(items):
        if not items:
            output.append("   No information provided.")
            return

        for index, item in enumerate(items, start=1):
            output.append(f"   {index}. {item}")

    # Header
    output.append("=" * width)
    output.append("                 RESEARCHPILOT AI")
    output.append("              AI RESEARCH ASSISTANT")
    output.append("=" * width)

    # Research topic
    output.append("")
    output.append(f"RESEARCH TOPIC: {report.topic}")
    output.append("=" * width)

    # Research methodology
    add_section(1, "RESEARCH METHODOLOGY")
    output.append(report.research_methodology)

    # Executive summary
    add_section(2, "EXECUTIVE SUMMARY")
    output.append(report.executive_summary)

    # Key findings
    add_section(3, "KEY FINDINGS")
    add_list(report.key_findings)

    # Important insights
    add_section(4, "IMPORTANT INSIGHTS")
    add_list(report.important_insights)

    # Limitations
    add_section(5, "RESEARCH LIMITATIONS")
    add_list(report.limitations)

    # Conclusion
    add_section(6, "CONCLUSION")
    output.append(report.conclusion)

    # Sources
    add_section(7, "REFERENCES")

    if report.sources:
        for index, source in enumerate(report.sources, start=1):
            output.append(f"   [{index}] {source.title}")
            output.append(f"       URL: {source.url}")
    else:
        output.append("   No sources available.")

    # Footer
    output.append("")
    output.append("=" * width)
    output.append("              END OF RESEARCH REPORT")
    output.append("=" * width)

    return "\n".join(output)
