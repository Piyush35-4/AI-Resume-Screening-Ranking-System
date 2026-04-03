from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_resumes(job_description: str, resume_texts: list[dict]) -> list[dict]:
    documents = [job_description] + [resume["text"] for resume in resume_texts]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    job_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]
    similarity_scores = cosine_similarity(job_vector, resume_vectors).flatten()

    ranked_results = []
    for resume, score in zip(resume_texts, similarity_scores):
        ranked_results.append(
            {
                "filename": resume["filename"],
                "score": round(float(score) * 100, 2),
                "extracted_text_preview": resume["text"][:220].replace("\n", " "),
            }
        )

    ranked_results.sort(key=lambda item: item["score"], reverse=True)
    return ranked_results

