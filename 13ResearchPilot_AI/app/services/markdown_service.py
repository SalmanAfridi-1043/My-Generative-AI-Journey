from pathlib import Path
from datetime import datetime
import re
from app.utils.helpers import format_research_report


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]


# Reports output directory
REPORTS_DIR = BASE_DIR / "output" / "reports"


def create_filename(topic: str) -> str:
    """
    Create a clean and unique Markdown filename.
    """

    # Convert topic into lowercase
    filename = topic.lower().strip()

    # Replace spaces and special characters
    filename = re.sub(r"[^a-z0-9]+", "_", filename)

    # Remove underscores from beginning and end
    filename = filename.strip("_")

    # Use default name if topic is empty
    if not filename:
        filename = "research_report"

    # Add timestamp to make filename unique
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"{filename}_{timestamp}.md"


def save_report_as_markdown(report) -> str:
    """
    Save a structured research report as a Markdown file.
    """

    try:
        # Create output directory if it does not exist
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        # Generate filename
        filename = create_filename(report.topic)

        # Complete file path
        file_path = REPORTS_DIR / filename

        # Format report
        report_content = format_research_report(report)

        # Save report
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"# ResearchPilot AI Research Report\n\n")
            file.write(f"**Research Topic:** {report.topic}\n\n")
            file.write(
                f"**Generated On:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            file.write("---\n\n")
            file.write(report_content)

        return str(file_path)

    except Exception as e:
        raise RuntimeError(f"Failed to save Markdown report: {e}") from e
