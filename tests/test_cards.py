import os

from rwp_module3.card_model import QuizItem
from rwp_module3.cli_cards import load_flashcards

my_path = __file__
TEST_DIR = os.path.dirname(my_path)


# Test for load_flashcards function
def test_load_flashcards():
    print(f"my_dir is {TEST_DIR}")
    quiz = load_flashcards(os.path.join(TEST_DIR, "test_data/test_flashcards.json"))
    assert quiz.title == "Test Quiz"
    assert len(quiz.items) > 0
    assert isinstance(quiz.items[0], QuizItem)
