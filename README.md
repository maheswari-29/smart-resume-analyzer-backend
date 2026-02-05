Smart Resume Analyzer – Backend

This folder contains the backend logic for resume parsing, OCR processing, skill extraction, and match calculation.

Technologies Used

Python 3

Flask

Flask-CORS

Gunicorn

pytesseract

pdfplumber

python-docx

API Endpoints
Health Check
GET /health


Response:

{
  "status": "ok"
}

Analyze Resume
POST /analyze


Form Data

resume – PDF, DOCX, or TXT file

job_description – Text

Response Example

{
  "match_percentage": 78,
  "matched_skills": ["Python", "Flask"],
  "missing_skills": ["Docker"]
}

Run Backend Locally
Step 1: Create Virtual Environment
python -m venv venv
venv\Scripts\activate

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Start the Server
python app.py


Backend will run at:

http://127.0.0.1:5000

Deployment Notes

Backend is deployed using Docker on Render

Gunicorn is used for production

CORS is enabled for frontend access

OCR Notes

Scanned PDFs are processed using OCR

OCR takes more time compared to normal PDFs

Accuracy depends on scan quality