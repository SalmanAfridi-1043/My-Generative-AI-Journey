from app.services.research_service import conduct_research
from app.services.markdown_service import save_report_as_markdown
from app.utils.helpers import format_research_report


def display_welcome():
    print("\n" + "=" * 65)
    print("                  RESEARCHPILOT AI")
    print("                 AI RESEARCH ASSISTANT")
    print("=" * 65)
    print("\nHello! What would you like to research today?")
    print("Enter a topic to begin or type 'exit' to quit.")


def display_user_message(topic):
    print(f"\nYou: {topic}")


def display_assistant_message(message):
    print(f"\nResearchPilot AI: {message}")


def process_research(topic):
    try:
        display_assistant_message("Starting your research...")

        # Step 1: Conduct research
        display_assistant_message("Searching the web and analyzing information...")

        research_result = conduct_research(topic)
        report = research_result["report"]

        # Step 2: Display report
        display_assistant_message("Your research report is ready.")

        print("\n" + format_research_report(report))

        # Step 3: Save report
        saved_path = save_report_as_markdown(report)

        display_assistant_message(
            f"Your report has been saved successfully.\nFile location: {saved_path}"
        )

    except Exception as e:
        display_assistant_message(
            f"Sorry, I couldn't complete your research.\nError: {e}"
        )


def main():
    display_welcome()

    while True:
        try:
            topic = input("\nYou: ").strip()

            if topic.lower() in ["exit", "quit", "bye"]:
                display_assistant_message(
                    "Thank you for using ResearchPilot AI. Goodbye!"
                )
                break

            if not topic:
                display_assistant_message("Please enter a research topic.")
                continue

            process_research(topic)

        except KeyboardInterrupt:
            display_assistant_message("Session interrupted. Goodbye!")
            break


if __name__ == "__main__":
    main()
