import collections
import logging
import os
from pprint import pprint

from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

from rwp_module3.card_model import Quiz, QuizItem

load_dotenv()

# MongoDB connection information with default values
mongo_host = os.environ.get("MONGO_HOST", "localhost")
mongo_port = int(os.environ.get("MONGO_PORT", 27017))  # Convert port to integer
mongo_username = os.environ.get("MONGO_USERNAME", "")
mongo_password = os.environ.get("MONGO_PASSWORD", "")

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"MongoDB Host: {mongo_host}")
logger.info(f"MongoDB Port: {mongo_port}")
logger.info(f"MongoDB Username: {mongo_username}")

database_name = "quizdb"  # Replace with your database name

DBConnection = collections.namedtuple("DBConnection", "client db")


def connect_db():
    # Connect to MongoDB
    client = MongoClient(host=mongo_host, port=mongo_port)
    db = client[database_name]
    return DBConnection(client, db)


def close_db(conn):
    # Close the MongoDB connection
    conn.client.close()


def insert_quiz(conn, new_quiz):
    # Insert the new quiz into MongoDB
    quiz_collection = conn.db["quizzes"]
    inserted_quiz_id = quiz_collection.insert_one(new_quiz.dict()).inserted_id
    return inserted_quiz_id


def all_quizzes(conn):
    quiz_collection = conn.db["quizzes"]
    return quiz_collection.find()


def lookup_quiz(conn, quiz_id):
    quiz_collection = conn.db["quizzes"]
    quiz = quiz_collection.find_one({"_id": ObjectId(quiz_id)})
    return quiz  # or None


def delete_quiz(conn, quiz_id):
    quiz_collection = conn.db["quizzes"]
    deleted_quiz = quiz_collection.find_one_and_delete({"_id": ObjectId(quiz_id)})
    return deleted_quiz


def add_item_to_quiz(conn, quiz_id, new_item_data):
    existing_quiz = lookup_quiz(conn, quiz_id)

    if existing_quiz:
        new_item = QuizItem(**new_item_data)

        existing_quiz["items"].append(new_item.model_dump())

        quiz_collection = conn.db["quizzes"]
        quiz_collection.update_one({"_id": ObjectId(quiz_id)}, {"$set": existing_quiz})

    return existing_quiz


def main():
    conn = connect_db()

    insert = False
    find = True
    delquiz = False
    update = False

    if insert:
        new_quiz_data = {
            # "title": "My New Quiz",
            "items": [
                {"question": "What is 2 + 2?", "answer": "4"},
                {"question": "What is the capital of France?", "answer": "Paris"},
                {
                    "question": "Who wrote 'Romeo and Juliet'?",
                    "answer": "William Shakespeare",
                },
            ]
        }
        new_quiz = Quiz(**new_quiz_data)

        new_quiz_id = insert_quiz(conn, new_quiz)
        print(f"New quiz inserted with ID: {new_quiz_id}")

    if find:
        # my_id = "65ad7cf48947faf0cc64c245"
        my_id = "65ad7edeb31f7754ac8cc21b"
        my_quiz = lookup_quiz(conn, my_id)
        print("found:", end="")
        pprint(my_quiz)

    if delquiz:
        my_id = "65ad7cf48947faf0cc64c245"
        my_quiz = delete_quiz(conn, my_id)
        print("deleted:", end="")
        pprint(my_quiz)

    if update:
        my_id = "65ad7edeb31f7754ac8cc21b"
        my_item = {"question": "What is 3 * 2?", "answer": "6"}
        my_quiz = add_item_to_quiz(conn, my_id, my_item)
        print("updated:", end="")
        pprint(my_quiz)

    quizzes = all_quizzes(conn)
    for q in quizzes:
        pprint(q)

    close_db(conn)


if __name__ == "__main__":
    main()
