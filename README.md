# AI Resume Screening & Ranking System

An end-to-end AI/ML mini project that screens multiple PDF resumes against a job description and ranks candidates using NLP-based similarity scoring.

## Project Highlights

- FastAPI backend for file upload, text extraction, ranking, and API responses
- PDF resume parsing using `PyPDF2`
- NLP similarity scoring using `TF-IDF` + `cosine similarity`
- MongoDB integration for storing ranking history
- Clean frontend built with plain HTML, CSS, and JavaScript
- Beginner-friendly structure that runs locally

## Project Structure

```text
AI Resume Screening & Ranking System/
|-- backend/
|   |-- app/
|   |   |-- __init__.py
|   |   |-- database.py
|   |   |-- main.py
|   |   |-- models.py
|   |   |-- ranker.py
|   |   `-- resume_parser.py
|   `-- requirements.txt
|-- frontend/
|   |-- index.html
|   |-- script.js
|   `-- styles.css
`-- README.md
```

## How It Works

1. The user opens the frontend page in a browser.
2. The user uploads multiple PDF resumes and pastes a job description.
3. The frontend sends the data to the FastAPI backend using `fetch()` and `FormData`.
4. The backend extracts text from each PDF.
5. The backend converts the job description and resume texts into TF-IDF vectors.
6. Cosine similarity scores are calculated between the job description and each resume.
7. Resumes are sorted from highest score to lowest score.
8. The result is returned to the frontend and also stored in MongoDB.

## Backend Setup

### 1. Create and activate a virtual environment

```bash
cd backend
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start MongoDB

Make sure MongoDB is installed and running locally on:

```bash
mongodb://localhost:27017
```

You can also change the connection using environment variables:

```bash
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=resume_screening_db
```

### 4. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

1. Open the `frontend/` folder.
2. Open `index.html` directly in your browser.

For best results, you can also serve it with a simple static server:

```bash
cd frontend
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

## API Endpoint

### `POST /api/rank-resumes`

Form fields:

- `job_description`: Job description text
- `resumes`: One or more PDF files

Sample JSON response:

```json
{
  "job_description": "Looking for a Python developer with FastAPI, NLP, and MongoDB skills.",
  "total_resumes": 2,
  "results": [
    {
      "filename": "resume_1.pdf",
      "score": 91.45,
      "extracted_text_preview": "Experienced Python developer with FastAPI and machine learning..."
    },
    {
      "filename": "resume_2.pdf",
      "score": 63.78,
      "extracted_text_preview": "Frontend engineer with JavaScript and React experience..."
    }
  ]
}
```

## How Frontend Connects to Backend

The frontend uses JavaScript `fetch()` to send a `POST` request to:

```text
http://127.0.0.1:8000/api/rank-resumes
```

It packages:

- the job description
- all uploaded PDF files

inside a `FormData` object. The backend receives those values, processes the resumes, and returns ranked results in JSON format. The frontend then updates the HTML table dynamically without reloading the page.

## How the ML Ranking Works

This project uses a simple and beginner-friendly NLP pipeline:

1. Convert the job description and resumes into text
2. Use `TF-IDF Vectorizer` to turn text into numeric features
3. Use `cosine similarity` to measure how close each resume is to the job description
4. Multiply the similarity by 100 to show a percentage score
5. Sort the resumes by score

Why this works:

- TF-IDF gives more weight to important words
- Cosine similarity compares document meaning based on shared weighted terms
- It is lightweight, explainable, and easy to demo in interviews

## Sample Test Data

Use this sample job description:

```text
We are hiring a Python developer with experience in FastAPI, REST APIs, MongoDB, machine learning, NLP, resume screening, and backend development.
```

Create simple PDF resumes with content like:

### Resume 1

```text
John Doe
Python Developer
Skills: Python, FastAPI, MongoDB, NLP, Scikit-learn, REST API
Experience: Built machine learning applications for document analysis and candidate screening.
```

### Resume 2

```text
Jane Smith
Frontend Developer
Skills: HTML, CSS, JavaScript, UI design
Experience: Built responsive dashboards and web interfaces.
```

### Resume 3

```text
Rahul Kumar
Data Scientist
Skills: Python, Machine Learning, NLP, Pandas, Scikit-learn
Experience: Worked on text classification, semantic search, and ranking systems.
```

## Interview Explanation

You can explain the project like this:

> I built a full-stack AI resume screening system where recruiters can upload multiple resumes and compare them against a job description. On the backend, I used FastAPI for the API layer, PyPDF2 for resume text extraction, and TF-IDF with cosine similarity to rank resumes by relevance. I stored the results in MongoDB for persistence. On the frontend, I used plain HTML, CSS, and JavaScript to keep the UI simple and lightweight while still supporting multi-file upload and dynamic result rendering.

Key interview talking points:

- Demonstrates full-stack development
- Shows practical NLP knowledge
- Uses an explainable ML ranking approach
- Includes file handling, APIs, and database integration
- Can be extended later with embeddings, authentication, and recruiter dashboards

## Future Improvements

- Replace TF-IDF with sentence embeddings
- Add user authentication
- Save uploaded files in cloud storage
- Add resume history and analytics dashboard
- Export ranked results to CSV or PDF

## License

This project is free to use for learning and portfolio purposes.
