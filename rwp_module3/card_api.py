import os
from urllib.parse import quote

from fastapi import FastAPI, HTTPException, Request

from rwp_module3.cli_cards import load_flashcards

app = FastAPI()

my_path = os.path.abspath(__file__)
SRC_DIR = os.path.dirname(my_path)
APP_DIR = os.path.dirname(SRC_DIR)


# TODO: move to a utility class and add tests.
def app_data_path(rel_path):
    return os.path.join(APP_DIR, rel_path)


def encode_for_url_path(string: str) -> str:
    return quote(string, safe="")


# TODO: add id field
quizzes = {
    "Electricity 1": load_flashcards(app_data_path("data/electricity1.json")),
    "Electricity 2": load_flashcards(app_data_path("data/electricity2.json")),
}


@app.get("/quiz")
async def get_quizzes(request: Request):
    base_url = str(request.base_url)
    if not base_url.endswith("/"):
        base_url = base_url + "/"
    info_list = [
        {"name": str(k), "link": base_url + "quiz/" + encode_for_url_path(str(k))}
        for k in quizzes.keys()
    ]
    return info_list


# TODO: let them select the quiz


@app.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: str):
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    quiz = quizzes[quiz_id]
    return quiz


@app.get("/flashcards/")
async def get_flashcards():
    quiz = quizzes["Electricity 1"]
    return quiz
