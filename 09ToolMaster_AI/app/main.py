from app.services.assistant import get_assistant_response


def main():

    print("\n-------------------------------")
    print("|       ToolMaster AI          |")
    print("-------------------------------\n")

    print("ToolMaster AI : Ask me anything or type 'exit' to quit.\n")

    while True:
        try:
            # Get user input
            user_message = input("You : ").strip()

            # Check exit command
            if user_message.lower() == "exit":
                print("\n----- Chat Ended -----\n")
                break

            # Handle empty input
            if not user_message:
                continue

            # Get AI response
            response = get_assistant_response(user_message)

            # Display AI response
            print("ToolMaster AI : ", response)
            print()

        except KeyboardInterrupt:
            print("\n----- Chat Ended -----\n")
            break

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()
