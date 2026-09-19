"""Emotion detection using the IBM Watson NLP EmotionPredict service."""

import requests

WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result():
    """Return a safe result for invalid input or service errors."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def emotion_detector(text_to_analyze):
    """Detect five emotions and the dominant emotion in a text."""
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            WATSON_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )
        if response.status_code == 400:
            return _empty_result()

        response.raise_for_status()
        data = response.json()
        scores = data["emotionPredictions"][0]["emotion"]

        result = {emotion: scores.get(emotion) for emotion in EMOTIONS}
        valid_scores = {
            key: value
            for key, value in result.items()
            if isinstance(value, (int, float))
        }
        result["dominant_emotion"] = (
            max(valid_scores, key=valid_scores.get)
            if valid_scores
            else None
        )
        return result
    except (
        requests.RequestException,
        ValueError,
        KeyError,
        TypeError,
        IndexError,
    ):
        return _empty_result()
