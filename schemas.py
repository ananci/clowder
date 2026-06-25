from pydantic import BaseModel

class EmailSummary(BaseModel):
    reasoning: str
    is_spam: bool
    sentiment: str