import json
import sys

from rwp_module3.card_model import Quiz


# Function to load flashcards from a JSON file
def load_flashcards(filename: str) -> Quiz:
    with open(filename, "r") as file:
        data = json.load(file)
    return Quiz.model_validate(data)


# Function to display flashcards
def display_flashcards(quiz: Quiz):
    for item in quiz.items:
        print("Question:", item.question)
        input("Press any key to see the answer...")
        print("Answer:", item.answer)
        print("\n")
        input("Press any key to continue to the next question...")
        print("\n")


# Main function
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <flashcards_file>")
        sys.exit(1)

    flashcards_file = sys.argv[1]
    try:
        quiz = load_flashcards(flashcards_file)
        display_flashcards(quiz)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
