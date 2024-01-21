from unittest.mock import MagicMock, patch

import pytest
from bson.objectid import ObjectId

# Import the methods to be tested
from rwp_module3.card_db import (
    DBConnection,
    add_item_to_quiz,
    all_quizzes,
    close_db,
    connect_db,
    delete_quiz,
    insert_quiz,
    lookup_quiz,
)

# Define test data
new_quiz_data = {
    "title": "Test Quiz",
    "items": [
        {"question": "What is 2 + 2?", "answer": "4"},
        {"question": "What is the capital of France?", "answer": "Paris"},
    ],
}


TEST_QUIZ_ID = "65ad7edeb31f7754ac8cc21b"


# Mocking the MongoClient and related methods
@pytest.fixture
def mock_mongo_client():
    with patch("rwp_module3.card_db.MongoClient") as mock_client:
        mock_db = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        yield DBConnection(mock_client, mock_db)


# Tests for the methods
def test_connect_db(mock_mongo_client):
    mock_client, _ = mock_mongo_client
    conn = connect_db()
    assert conn.client == mock_client.return_value
    assert conn.db == mock_client.return_value.__getitem__.return_value


def test_close_db(mock_mongo_client):
    mock_client, _ = mock_mongo_client
    conn = connect_db()
    close_db(conn)
    conn.client.close.assert_called_once()


def test_insert_quiz(mock_mongo_client):
    mock_client, mock_db = mock_mongo_client
    new_quiz = MagicMock()
    mock_db.__getitem__.return_value.insert_one.return_value.inserted_id = ObjectId(
        TEST_QUIZ_ID
    )
    inserted_quiz_id = insert_quiz(mock_mongo_client, new_quiz)
    print(f"returned id is {inserted_quiz_id}")
    assert inserted_quiz_id == ObjectId(TEST_QUIZ_ID)


def test_all_quizzes(mock_mongo_client):
    _, mock_db = mock_mongo_client
    mock_db.__getitem__.return_value.find.return_value = [{"quiz": "data"}]
    quizzes = all_quizzes(mock_mongo_client)
    assert isinstance(quizzes, list)
    assert len(quizzes) == 1


def test_lookup_quiz(mock_mongo_client):
    _, mock_db = mock_mongo_client
    mock_db.__getitem__.return_value.find_one.return_value = {"quiz": "data"}

    quiz = lookup_quiz(mock_mongo_client, TEST_QUIZ_ID)
    assert quiz == {"quiz": "data"}


def test_delete_quiz(mock_mongo_client):
    _, mock_db = mock_mongo_client
    mock_db.__getitem__.return_value.find_one_and_delete.return_value = {
        "deleted": "quiz"
    }
    deleted_quiz = delete_quiz(mock_mongo_client, TEST_QUIZ_ID)
    assert deleted_quiz == {"deleted": "quiz"}


def test_add_item_to_quiz(mock_mongo_client):
    _, mock_db = mock_mongo_client
    existing_quiz = {"items": []}
    mock_db.__getitem__.return_value.find_one.return_value = existing_quiz
    new_item_data = {"question": "New Question", "answer": "New Answer"}
    updated_quiz = add_item_to_quiz(mock_mongo_client, TEST_QUIZ_ID, new_item_data)
    assert updated_quiz["items"] == [new_item_data]  # Check if the item was added


# Run tests with pytest
if __name__ == "__main__":
    pytest.main()
