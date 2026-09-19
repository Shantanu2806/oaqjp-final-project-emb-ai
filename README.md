# Emotion Detector

Coursera / IBM final project: a Flask web application using the IBM Watson NLP EmotionPredict service to detect anger, disgust, fear, joy, and sadness.

## Files

- `EmotionDetection/emotion_detection.py`
- `EmotionDetection/__init__.py`
- `test_emotion_detection.py`
- `server.py`
- `templates/index.html`
- `static/mywebscript.js`

## Run locally

```bash
pip install flask requests pylint
python -m unittest -v
python server.py
```

Open `http://127.0.0.1:5000/` in a browser.
