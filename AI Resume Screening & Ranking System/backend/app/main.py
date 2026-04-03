from datetime import datetime, timezone

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .database import get_rankings_collection
from .models import RankingResponse
from .ranker import rank_resumes
from .resume_parser import extract_text_from_pdf


app = FastAPI(
    title="AI Resume Screening & Ranking System",
    description="Upload PDF resumes, compare them to a job description, and rank candidates.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {"message": "AI Resume Screening & Ranking System API is running."}


@app.post("/api/rank-resumes", response_model=RankingResponse)
async def rank_uploaded_resumes(
    job_description: str = Form(...),
    resumes: list[UploadFile] = File(...),
):
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")

    if not resumes:
        raise HTTPException(status_code=400, detail="Please upload at least one resume.")

    parsed_resumes: list[dict] = []

    for resume in resumes:
        if not resume.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type for {resume.filename}. Only PDF files are allowed.",
            )

        file_bytes = await resume.read()
        extracted_text = extract_text_from_pdf(file_bytes)

        if not extracted_text:
            extracted_text = "No readable text found in this PDF."

        parsed_resumes.append(
            {
                "filename": resume.filename,
                "text": extracted_text,
            }
        )

    ranked_results = rank_resumes(job_description=job_description, resume_texts=parsed_resumes)

    response_payload = {
        "job_description": job_description,
        "total_resumes": len(ranked_results),
        "results": ranked_results,
    }

    get_rankings_collection().insert_one(
        {
            **response_payload,
            "created_at": datetime.now(timezone.utc),
        }
    )

    return response_payload
