from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from functools import lru_cache


print("🚀 AI Model is loading...", flush=True)

_sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
_categorization_model = SentenceTransformer("all-MiniLM-L6-v2")

print("✅ AI Model Loaded Successfully", flush=True)

# Predefined categories
CATEGORIES = ["usability", "design", "performance", "pricing", "support"]

@lru_cache(maxsize=1000)
def analyze_feedback(feedback_text: str):
    """Analyze user feedback: categorize and perform sentiment analysis"""

    # Step 1: Sentiment Analysis
    sentiment = analyze_sentiment(feedback_text)

    # Step 2: Categorization (Find Closest Category)
    category_scores = {category: util.pytorch_cos_sim(_categorization_model.encode(feedback_text), 
                                                      _categorization_model.encode(category)).item()
                       for category in CATEGORIES}
    category = max(category_scores, key=category_scores.get)

    return {
        "sentiment": sentiment,
        "category": category
    }


def analyze_sentiment(text: str):
    return _sentiment_analyzer(text)[0]["label"].lower()