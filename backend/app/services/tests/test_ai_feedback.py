import pytest
from unittest.mock import patch, MagicMock

# Suppose your code is in ai_feedback.py
# from ai_feedback import analyze_sentiment, analyze_feedback, CATEGORIES

# Example structure: adapt imports/paths to your actual project
# from path.to.your.module import analyze_sentiment, analyze_feedback, CATEGORIES

@patch("path.to.your.module._sentiment_analyzer")
def test_analyze_sentiment(mock_sentiment_analyzer):
    # Mock the pipeline output
    mock_sentiment_analyzer.return_value = [{"label": "POSITIVE"}]

    result = analyze_sentiment("I love this product!")
    # Ensure the pipeline was called once
    mock_sentiment_analyzer.assert_called_once_with("I love this product!")
    assert result == "positive", "Expected a lowercase positive sentiment"

@patch("path.to.your.module._categorization_model")
@patch("path.to.your.module._sentiment_analyzer")
def test_analyze_feedback(mock_sentiment_analyzer, mock_categorization_model):
    # Mock sentiment output
    mock_sentiment_analyzer.return_value = [{"label": "NEGATIVE"}]

    # Mock the sentence-transformers model
    # We'll configure the .encode() calls and the similarity scores
    mock_encode = MagicMock(side_effect=lambda text: f"encoded({text})")
    mock_categorization_model.encode = mock_encode

    # Pretend each category returns these “similarity” values
    # so we can force a particular category to be chosen.
    # For example, let's say "design" yields the highest similarity.
    # We patch util.pytorch_cos_sim to return a MagicMock whose .item() is the value we want.
    with patch("path.to.your.module.util.pytorch_cos_sim") as mock_pytorch_cos_sim:
        mock_pytorch_cos_sim.side_effect = [
            0.1,  # "usability"
            0.2,  # "design"  <-- highest
            0.0,  # "performance"
            0.05, # "pricing"
            0.05  # "support"
        ]

        feedback_text = "The layout looks really outdated."
        result = analyze_feedback(feedback_text)

        # Check that _sentiment_analyzer was called
        mock_sentiment_analyzer.assert_called_once_with(feedback_text)
        # Check that we encoded the feedback text + each category exactly
        assert mock_encode.call_count == 6, "Should encode text once plus each of 5 categories"

        # Validate the results
        assert result["sentiment"] == "negative"
        assert result["category"] == "design"  # Because 0.2 was the highest similarity

@pytest.mark.parametrize(
    "feedback_text, expected_sentiment_mock, expected_category_scores, expected_category",
    [
        (
            "I absolutely love this app!",
            [{"label": "POSITIVE"}],
            [0.2, 0.1, 0.0, 0.0, 0.0],  # Highest on index 0: "usability"
            "usability",
        ),
        (
            "It's too expensive for what it offers.",
            [{"label": "NEGATIVE"}],
            [0.0, 0.0, 0.0, 0.8, 0.0],  # Highest on index 3: "pricing"
            "pricing",
        ),
    ],
)
@patch("path.to.your.module._categorization_model")
@patch("path.to.your.module._sentiment_analyzer")
def test_analyze_feedback_multiple_cases(
    mock_sentiment_analyzer,
    mock_categorization_model,
    feedback_text,
    expected_sentiment_mock,
    expected_category_scores,
    expected_category
):
    """
    Tests multiple scenarios with parametrize to ensure we handle different
    texts, sentiments, and category-scoring patterns.
    """
    mock_sentiment_analyzer.return_value = expected_sentiment_mock

    mock_encode = MagicMock(side_effect=lambda text: f"encoded({text})")
    mock_categorization_model.encode = mock_encode

    with patch("path.to.your.module.util.pytorch_cos_sim") as mock_pytorch_cos_sim:
        # Each time we call similarity, we pop from expected_category_scores
        mock_pytorch_cos_sim.side_effect = [
            score for score in expected_category_scores
        ]

        result = analyze_feedback(feedback_text)
        assert result["sentiment"] == expected_sentiment_mock[0]["label"].lower()
        assert result["category"] == expected_category


