import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(text):
    """Returns sentiment score (1 to 5) for a single review."""
    tokens = tokenizer.encode(text, return_tensors="pt")
    result = model(tokens)
    sentiment_score = int(torch.argmax(result.logits)) + 1
    return sentiment_score

def get_sentiment_label(avg_score):

    if avg_score >= 4.5:
        return "Very Positive"
    elif avg_score >= 3.5:
        return "Positive"
    elif avg_score >= 2.5:
        return "Neutral"
    elif avg_score >= 1.5:
        return "Negative"
    else:
        return "Very Negative"