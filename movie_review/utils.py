import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(text):
    tokens = tokenizer.encode(text, return_tensors="pt")
    result = model(tokens)
    sentiment_score = int(torch.argmax(result.logits)) + 1
    return sentiment_score


