from pydantic import BaseModel, Field


class ResumeScore(BaseModel):
    filename: str = Field(..., example="john_doe_resume.pdf")
    score: float = Field(..., example=87.52)
    extracted_text_preview: str = Field(
        ..., example="Experienced Python developer with strong NLP and FastAPI skills..."
    )


class RankingResponse(BaseModel):
    job_description: str
    total_resumes: int
    results: list[ResumeScore]

