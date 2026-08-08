from fastapi import FastAPI

from services.word_service import import_words


app = FastAPI(
    title="GermanTrainer API"
)


@app.get("/")
def home():

    return {
        "status": "GermanTrainer API running"
    }


@app.post("/import")
def import_words_api(data: dict):

    added = import_words(
        telegram_id=data["telegram_id"],
        category=data["category"],
        lesson=data["lesson"],
        words=data["words"]
    )

    return {
        "status": "success",
        "added": added
    }