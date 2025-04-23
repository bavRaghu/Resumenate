from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil, os

from enhancer.extractor import extract_text_from_file
from enhancer.resume_enhancer import prompt_gemini, generate_pdf_from_html
from keyword_extraction import extract_keywords_from_jobdesc

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63342",
        "http://127.0.0.1:8000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/files", StaticFiles(directory="."), name="files")


@app.post("/enhance")
async def enhance_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    temp_path = f"temp_{resume.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(resume.file, f)

    resume_text = extract_text_from_file(temp_path)
    os.remove(temp_path)

    keyword_list = extract_keywords_from_jobdesc(job_description)

    resume_set = set(resume_text.lower().split())
    jd_set = set(" ".join(keyword_list).lower().split())
    matched = resume_set & jd_set
    match_percent = int((len(matched) / len(jd_set)) * 100) if jd_set else 0

    enhanced_html = prompt_gemini(resume_text, keyword_list)

    enhanced_path = f"enhanced_{resume.filename.replace('.pdf', '')}.pdf"
    generate_pdf_from_html(enhanced_html, enhanced_path)

    print(match_percent)
    return JSONResponse({
        "keywords": keyword_list,
        "match_percent": match_percent,
        "download_url": f"http://127.0.0.1:8000/files/{enhanced_path}"
    })
