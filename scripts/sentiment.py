import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def run():
    tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

    text = "This is a great movie!"
    tokens = tokenizer.encode(text, return_tensors="pt")

    result = model(tokens) 

    print(result.logits)

    print(torch.argmax(result.logits))

    print(int(torch.argmax(result.logits)) + 1)