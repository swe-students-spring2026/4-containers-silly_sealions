from db import speeches_collection


def test_db_connection():
    result = speeches_collection.insert_one({"title": "connection test"})
    assert result.inserted_id is not None
    speeches_collection.delete_one({"_id": result.inserted_id})


def test_insert_speech():
    speech = {
        "user_id": "test_user_1",
        "title": "test speech",
        "timestamp": "2026-04-14T22:00:00",
        "transcript": "this is a test",
        "wpm": 120,
        "filler_count": 3,
        "filler_words_found": ["um", "like", "uh"],
        "volume_score": 80,
        "pitch_variety_score": 75,
        "pace_score": 85,
        "overall_score": 80,
    }

    result = speeches_collection.insert_one(speech)
    assert result.inserted_id is not None

    saved_speech = speeches_collection.find_one({"_id": result.inserted_id})
    assert saved_speech is not None
    assert saved_speech["title"] == "test speech"
    assert saved_speech["wpm"] == 120
    assert saved_speech["filler_count"] == 3

    speeches_collection.delete_one({"_id": result.inserted_id})
