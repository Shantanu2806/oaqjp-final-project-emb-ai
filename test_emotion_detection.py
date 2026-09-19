"""Unit tests for the EmotionDetection package."""

import unittest
from unittest.mock import patch

from EmotionDetection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Test dominant-emotion formatting and error handling."""

    @staticmethod
    def _mock_response(scores):
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                return None

            def json(self):
                return {"emotionPredictions": [{"emotion": scores}]}

        return MockResponse()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_joy(self, mock_post):
        mock_post.return_value = self._mock_response({
            "anger": 0.01, "disgust": 0.02, "fear": 0.03,
            "joy": 0.90, "sadness": 0.04
        })
        self.assertEqual(
            emotion_detector("I am very happy today")["dominant_emotion"],
            "joy",
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_anger(self, mock_post):
        mock_post.return_value = self._mock_response({
            "anger": 0.90, "disgust": 0.02, "fear": 0.03,
            "joy": 0.01, "sadness": 0.04
        })
        self.assertEqual(
            emotion_detector("I am furious")["dominant_emotion"],
            "anger",
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_disgust(self, mock_post):
        mock_post.return_value = self._mock_response({
            "anger": 0.02, "disgust": 0.90, "fear": 0.03,
            "joy": 0.01, "sadness": 0.04
        })
        self.assertEqual(
            emotion_detector("That is disgusting")["dominant_emotion"],
            "disgust",
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_sadness(self, mock_post):
        mock_post.return_value = self._mock_response({
            "anger": 0.02, "disgust": 0.03, "fear": 0.04,
            "joy": 0.01, "sadness": 0.90
        })
        self.assertEqual(
            emotion_detector("I feel sad")["dominant_emotion"],
            "sadness",
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_fear(self, mock_post):
        mock_post.return_value = self._mock_response({
            "anger": 0.02, "disgust": 0.03, "fear": 0.90,
            "joy": 0.01, "sadness": 0.04
        })
        self.assertEqual(
            emotion_detector("I am afraid")["dominant_emotion"],
            "fear",
        )

    def test_blank_input(self):
        self.assertEqual(
            emotion_detector("   "),
            {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            },
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400(self, mock_post):
        class BadResponse:
            status_code = 400

            def raise_for_status(self):
                return None

        mock_post.return_value = BadResponse()
        self.assertIsNone(
            emotion_detector("invalid service request")["dominant_emotion"]
        )


if __name__ == "__main__":
    unittest.main()
