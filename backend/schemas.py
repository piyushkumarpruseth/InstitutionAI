from pydantic import BaseModel, ConfigDict, Field

class InstitutionCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    institution_type: str = Field(min_length=2, max_length=50)
    email: str | None = Field(default=None, max_length=150)

class InstitutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    institution_type: str
    email: str | None = None

class ChatRequest(BaseModel):
    institution_id: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=1, max_length=2000)

class ChatResponse(BaseModel):
    institution_id: str
    question: str
    answer: str
