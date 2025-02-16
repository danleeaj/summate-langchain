from pydantic import BaseModel

class Response(BaseModel):
    explanation: str
    rubricComponentSatisfied: bool