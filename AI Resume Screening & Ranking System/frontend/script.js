const API_BASE_URL = "http://127.0.0.1:8000";

const resumeForm = document.getElementById("resumeForm");
const jobDescriptionInput = document.getElementById("jobDescription");
const resumeFilesInput = document.getElementById("resumeFiles");
const submitButton = document.getElementById("submitButton");
const statusMessage = document.getElementById("statusMessage");
const resultsBody = document.getElementById("resultsBody");
const resultCount = document.getElementById("resultCount");

resumeForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const jobDescription = jobDescriptionInput.value.trim();
    const resumeFiles = resumeFilesInput.files;

    if (!jobDescription || resumeFiles.length === 0) {
        statusMessage.textContent = "Please enter a job description and upload at least one PDF resume.";
        return;
    }

    const formData = new FormData();
    formData.append("job_description", jobDescription);

    for (const file of resumeFiles) {
        formData.append("resumes", file);
    }

    try {
        submitButton.disabled = true;
        statusMessage.textContent = "Processing resumes and ranking candidates...";
        resultCount.textContent = "Loading...";

        const response = await fetch(`${API_BASE_URL}/api/rank-resumes`, {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong while ranking resumes.");
        }

        renderResults(data.results);
        statusMessage.textContent = "Ranking completed successfully.";
        resultCount.textContent = `${data.total_resumes} resumes`;
    } catch (error) {
        resultsBody.innerHTML = `
            <tr>
                <td colspan="4" class="empty-state">${error.message}</td>
            </tr>
        `;
        statusMessage.textContent = "The request failed. Please check that the backend server is running.";
        resultCount.textContent = "0 resumes";
    } finally {
        submitButton.disabled = false;
    }
});

function renderResults(results) {
    if (!results.length) {
        resultsBody.innerHTML = `
            <tr>
                <td colspan="4" class="empty-state">No ranked results were returned.</td>
            </tr>
        `;
        return;
    }

    resultsBody.innerHTML = results
        .map((result, index) => {
            return `
                <tr>
                    <td>${index + 1}</td>
                    <td>${escapeHtml(result.filename)}</td>
                    <td><span class="score-pill">${result.score.toFixed(2)}%</span></td>
                    <td>${escapeHtml(result.extracted_text_preview || "No preview available")}</td>
                </tr>
            `;
        })
        .join("");
}

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value;
    return div.innerHTML;
}
