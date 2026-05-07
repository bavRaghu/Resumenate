from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS

import os
import uuid

from enhancer.extractor import extract_text_from_file
from enhancer.resume_enhancer import (
    prompt_gemini,
    generate_pdf_from_html
)

from keyword_extraction import (
    extract_keywords_from_jobdesc
)

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = "generated_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/files/<filename>")
def download_file(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
        as_attachment=True
    )

@app.route("/enhance", methods=["POST"])
def enhance_resume():

    try:
        if "resume" not in request.files:
            return jsonify({
                "error": "No resume uploaded"
            }), 400

        resume = request.files["resume"]
        job_description = request.form.get("job_description")

        if not job_description:
            return jsonify({
                "error": "Job description missing"
            }), 400

        extension = os.path.splitext(resume.filename)[1]

        temp_path = f"temp_{uuid.uuid4().hex}{extension}"

        resume.save(temp_path)

        resume_text = extract_text_from_file(temp_path)

        os.remove(temp_path)

        keyword_list = extract_keywords_from_jobdesc(
            job_description
        )

        matched = [
            kw for kw in keyword_list
            if kw.lower() in resume_text.lower()
        ]

        match_percent = int(
            (len(matched) / len(keyword_list)) * 100
        ) if keyword_list else 0

        enhanced_html = prompt_gemini(
            resume_text,
            keyword_list
        )

        output_filename = (
            f"enhanced_{uuid.uuid4().hex}.pdf"
        )

        output_path = os.path.join(
            UPLOAD_FOLDER,
            output_filename
        )

        generate_pdf_from_html(
            enhanced_html,
            output_path
        )

        return jsonify({
            "keywords": keyword_list,
            "match_percent": match_percent,
            "download_url":
                f"http://127.0.0.1:5000/files/{output_filename}"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=False)