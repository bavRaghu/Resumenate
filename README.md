# Resumenate: AI-Powered Resume Optimizer 

Resumenate is a web-based AI resume optimization platform that analyzes resumes against target job descriptions to improve ATS compatibility and professional presentation. The system extracts ATS-relevant keywords, evaluates resume-role alignment, and generates enhanced resumes using NLP pipelines and LLM-driven content enhancement.

The platform combines keyword extraction, structured resume enhancement workflows, automated PDF generation, and a modern Flask-based web interface to streamline resume tailoring for job applications.

---

## Getting Started

These instructions will help you set up Resumenate on your local machine for development and testing. Refer to the Deployment section for information on hosting the application in a production environment.

---

### Prerequisites

Requirements for running the project:

- Python 3.10 or higher  
- pip (Python package manager)  
- OpenRouter API key  
- spaCy English language model (`en_core_web_sm`)  

---

### Installing

Clone the repository:

```bash
git clone https://github.com/bavRaghu/Resumenate
cd resumenate
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download the spaCy model:

```bash
python -m spacy download en_core_web_sm
```

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Run the application:

```bash
python main.py
```

Open the application in a browser:

```text
http://localhost:5000
```

Upload a resume, paste a target job description, and generate an ATS-optimized enhanced resume.

---

## Running the tests

Testing is performed through functional validation of the resume analysis and enhancement workflow.

### Sample Tests

The system was tested using representative job descriptions and resumes across multiple domains:

- Software engineering resumes for ATS keyword optimization  
- Data science job descriptions for technical keyword extraction  
- Minimal resumes to test enhancement robustness  
- Multi-page PDF resumes for extraction consistency  
- DOCX resumes to validate cross-format compatibility  

Example:

```text
Input: Resume missing cloud and backend keywords
Expected: Extracted ATS keywords include missing technologies and generated resume integrates relevant terminology naturally
```

---

## Features

### ATS Keyword Extraction
- Uses KeyBERT and spaCy-based NLP pipelines to extract role-specific ATS keywords from job descriptions  
- Identifies technical skills, frameworks, tools, and domain terminology  
- Applies rule-based filtering and keyword deduplication for cleaner extraction  

### Resume-Role Match Analysis
- Compares extracted ATS keywords against uploaded resumes  
- Calculates a resume-role alignment percentage  
- Highlights detected ATS keywords for transparency and analysis  

### AI-Powered Resume Enhancement
- Uses OpenRouter-hosted GPT models to professionally rewrite and optimize resumes  
- Enhances wording, formatting consistency, and technical phrasing  
- Expands weak bullet points into stronger professional descriptions  
- Integrates ATS-relevant keywords naturally throughout the resume  

### Structured Resume Generation
- Uses controlled HTML templates for consistent formatting and layout  
- Separates content generation from rendering logic for improved stability  
- Maintains professional typography, spacing, and ATS-friendly formatting  

---

## Built With

- Flask (Python web framework)  
- Flask-CORS  
- KeyBERT  
- spaCy   
- OpenRouter API  
- GPT-based LLMs  
- WeasyPrint  
- pdfminer.six  
- docx2txt  
- HTML, CSS, JavaScript  
- Microsoft Azure  
- GitHub Actions  

---

## Deployment

The application is designed for deployment as a Flask web service using Microsoft Azure App Service.

Deployment process:

- Code is pushed to GitHub  
- Azure is integrated with the repository  
- GitHub Actions automatically triggers deployment workflows  
- Application updates are deployed on pushes to the main branch  
