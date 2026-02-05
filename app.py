from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

from resume_parser import parse_resume
from skills import extract_skills, calculate_match

app = Flask(__name__)
CORS(app)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend is live 🚀"}), 200

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route("/analyze", methods=["OPTIONS"])
def analyze_options():
    return jsonify({"ok": True}), 200

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    try:
        if "resume" not in request.files or "job_description" not in request.form:
            return jsonify({"error": "Missing resume file or job description"}), 400

        file = request.files["resume"]
        job_description = request.form.get("job_description", "").strip()

        if file.filename == "" or not job_description:
            return jsonify({"error": "Empty file or job description"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Unsupported file type"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        resume_text = parse_resume(filepath)

        if not resume_text:
            os.remove(filepath)
            return jsonify({"error": "Unable to extract text"}), 400

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        matched_skills = list(set(resume_skills) & set(job_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))

        match_percentage = calculate_match(matched_skills, job_skills)

        os.remove(filepath)

        return jsonify({
            "match_percentage": match_percentage,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Resume processing failed",
            "details": str(e)
        }), 500
