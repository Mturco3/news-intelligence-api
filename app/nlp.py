import spacy
from transformers import pipeline
from newspaper import Article
import langdetect

nlp = spacy.load("en_core_web_sm")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

TOPICS = ["politics", "economics", "technology", "sports", "health", "environment", "entertainment"]

def extract_text_from_url(url: str) -> str:
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def get_entities(text: str) -> list[str]:
    doc = nlp(text)
    entities = list(set([ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "GPE"]]))
    return entities

def get_summary(text: str) -> str:
    max_input = 1024
    truncated = text[:max_input]
    result = summarizer(truncated, max_length=130, min_length=30, do_sample=False)
    return result[0]["summary_text"]

def get_sentiment(text: str) -> tuple[str, float]:
    truncated = text[:512]
    result = sentiment_analyzer(truncated)[0]
    label = result["label"].lower()
    score = round(result["score"], 3)
    return label, score

def get_topics(text: str) -> list[str]:
    truncated = text[:512]
    result = classifier(truncated, TOPICS, multi_label=True)
    topics = [label for label, score in zip(result["labels"], result["scores"]) if score > 0.5]
    return topics

def get_language(text: str) -> str:
    try:
        return langdetect.detect(text)
    except:
        return "unknown"

def analyze_text(text: str) -> dict:
    return {
        "summary": get_summary(text),
        "sentiment": get_sentiment(text)[0],
        "sentiment_score": get_sentiment(text)[1],
        "entities": get_entities(text),
        "topics": get_topics(text),
        "language": get_language(text)
    }