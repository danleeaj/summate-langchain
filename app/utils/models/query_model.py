from pydantic import BaseModel

class Query(BaseModel):
    rubricComponent: str
    studentResponse: str