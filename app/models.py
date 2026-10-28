from pydantic import BaseModel, Field

class RunRequest(BaseModel):
    problem_id: str = Field(min_length=1,max_length=80)
    candidate_id: str = Field(min_length=1,max_length=80)

class CodeReview(BaseModel):
    correctness: int = Field(ge=1,le=5)
    edge_cases: int = Field(ge=1,le=5)
    complexity: int = Field(ge=1,le=5)
    readability: int = Field(ge=1,le=5)
    specification_adherence: int = Field(ge=1,le=5)
    rationale: str = Field(min_length=10,max_length=3000)

class TestCase(BaseModel):
    case_id: str
    description: str
    input: list
    expected: list | None = None
    expected_error: str | None = None

class Candidate(BaseModel):
    candidate_id: str
    label: str
    trust_level: str
    notes: str
