from pydantic import BaseModel
from typing import Optional

class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

class AnalysisResult(BaseModel):
    summary: str
    sentiment: str
    sentiment_score: float
    entities: list[str]
    topics: list[str]
    language: str