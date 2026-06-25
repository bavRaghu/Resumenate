import re

from weasyprint import HTML

from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_resume_html(
    resume_text: str,
    keywords: list,
    job_description: str
) -> str:

    resume_text = resume_text[:5000]
    keywords = keywords[:20]

    prompt = f"""
            You are an expert technical recruiter, ATS optimization specialist, and professional resume writer with experience reviewing resumes for companies such as Google, Microsoft, Amazon, Meta, Apple, NVIDIA, and other top technology companies.

            Your task is to transform the candidate's resume into a highly competitive, ATS-optimized, one-page professional resume tailored specifically for the provided job description.

            =====================================================
            INPUTS
            =====================================================

            CURRENT RESUME

            {resume_text}

            -----------------------------------------------------

            TARGET JOB DESCRIPTION

            {job_description}

            -----------------------------------------------------

            EXTRACTED ATS KEYWORDS

            The following ATS keywords were extracted from the target job description. Incorporate every keyword that is technically relevant to the candidate's existing projects or experience. If a keyword cannot be justified, omit it. For keywords that can be justified, ensure each appears naturally at least once.

            {keywords}

            =====================================================
            YOUR OBJECTIVES
            =====================================================

            Your goal is NOT simply to rewrite the resume.

            Instead, think like an experienced recruiter whose objective is to maximize the candidate's interview chances while keeping the resume realistic and professional.

            Before writing, silently perform these steps:

            STEP 1
            Understand the candidate's existing experience, skills, education, projects and technical strengths.

            STEP 2
            Understand what the employer is looking for from the job description.

            STEP 3
            Identify missing technical skills, tools, frameworks and ATS keywords.

            STEP 4
            Determine which missing keywords can be naturally incorporated WITHOUT changing the candidate's overall profile.

            STEP 5
            Rewrite the resume to maximize ATS relevance while remaining coherent and believable.

            =====================================================
            RULES
            =====================================================

            1. Preserve the candidate's overall profile. You may expand existing project descriptions, add realistic implementation details, strengthen technical explanations, and naturally incorporate relevant ATS keywords, provided the additions remain technically plausible and consistent with the original resume

            2. Improve wording wherever possible.

            3. Rewrite weak bullet points into strong accomplishment-oriented statements.

            4. Use powerful action verbs.

            5. Quantify achievements whenever reasonable.

            6. Incorporate as many relevant ATS keywords as naturally possible.

            7. Every keyword that logically fits the candidate's profile should appear somewhere in the resume.

            8. If the resume lacks measurable impact, create realistic, believable metrics that improve readability.

            9. NEVER keyword stuff.

            10. NEVER produce repetitive bullets.

            11. NEVER repeat technologies unnecessarily.

            12. Keep the resume to ONE PAGE.

            13. Prioritize quality over quantity.

            14. Remove unnecessary filler words.

            15. Ensure every bullet communicates:
            - what was built
            - how it was built
            - technologies used
            - impact or outcome

            =====================================================
            PROJECTS
            =====================================================

            For every project:

            • Write exactly 3 bullet points.

            Each bullet should:

            - begin with a strong action verb
            - mention important technologies
            - include implementation details
            - mention technical impact whenever possible
            - naturally include relevant ATS keywords

            =====================================================
            EXPERIENCE
            =====================================================

            Rewrite experience bullets to sound professional and technically strong.

            Avoid generic phrases like:

            "Worked on..."

            "Responsible for..."

            Instead use verbs such as:

            Developed
            Engineered
            Designed
            Implemented
            Optimized
            Automated
            Integrated
            Built
            Created
            Architected
            Enhanced
            Improved

            =====================================================
            SKILLS
            =====================================================

            Reorganize skills into these sections:

            Languages

            Frameworks & Libraries

            Databases

            Cloud & DevOps

            Developer Tools

            Technologies

            =====================================================
            ATS OPTIMIZATION
            =====================================================

            Prioritize the following extracted ATS keywords whenever appropriate:

            {keywords}

            Every relevant keyword should appear at least once if it can naturally fit.

            =====================================================
            FORMATTING
            =====================================================

            Return ONLY the following sections in EXACTLY this format.

                NAME

                <name>

                CONTACT

                <contact>

                EDUCATION

                - bullet
                - bullet

                EXPERIENCE

                Role Name

                - bullet

                - bullet

                PROJECTS

                Project Name

                - bullet

                - bullet

                SKILLS

                Languages: ...

                Frameworks: ...

                ACHIEVEMENTS

                - bullet

                - bullet

                Do NOT return HTML.

                Do NOT return Markdown.

                Do NOT wrap anything in code fences.

                Do NOT explain anything.

                Output ONLY these sections.
            """
    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content
    content = (
        content
            .replace("```html", "")
            .replace("```", "")
            .strip()
    )

    def extract_section(section_name):

        pattern = rf"{section_name}\s*:?\s*(.*?)(?=\n[A-Z][A-Z &]+:?|\Z)"

        match = re.search(
            pattern,
            content,
            re.DOTALL
        )

        return match.group(1).strip() if match else ""
    name = extract_section("NAME")
    contact = extract_section("CONTACT")
    education = extract_section("EDUCATION")
    experience = extract_section("EXPERIENCE")
    projects = extract_section("PROJECTS")
    skills = extract_section("SKILLS")
    achievements = extract_section("ACHIEVEMENTS")

    def format_bullets(text):

        if not text:

            return ""

        html = "<ul>"

        for line in text.split("\n"):

            line = line.strip()

            if not line:

                continue

            if line.startswith("-"):

                html += f"<li>{line[1:].strip()}</li>"

            else:

                html += f"<p><strong>{line}</strong></p>"

        html += "</ul>"

        return html
    
    html = f"""
        <!DOCTYPE html>

        <html>

        <head>

        <meta charset="UTF-8">

        <style>

        @page{{
    size:A4;
    margin:0.42in;
}}

body{{

    font-family:"Times New Roman", serif;

    font-size:10pt;

    color:#111;

    line-height:1.18;

    margin:0;
}}

h1{{

    text-align:center;

    font-size:22px;

    margin-bottom:4px;
}}

.contact{{

    text-align:center;

    font-size:10px;

    margin-bottom:10px;
}}

.section{{

    margin-top:8px;
}}

.section h2{{

    font-size:13px;

    text-transform:uppercase;

    margin-bottom:3px;

    border-bottom:1.4px solid black;

    padding-bottom:2px;
}}

ul{{

    margin:2px 0 5px 18px;

    padding:0;
}}

li{{

    margin-bottom:2px;

    line-height:1.22;
}}

p{{

    margin:3px 0;
}}

strong{{

    font-weight:bold;
}}

.project{{

    margin-bottom:8px;
}}

        </style>

        </head>

        <body>

        <h1>{name}</h1>

        <div class="contact">

        {contact}

        </div>

        <div class="section">

        <h2>Education</h2>

        {format_bullets(education)}

        </div>

        <div class="section">

        <h2>Experience</h2>

        {format_bullets(experience)}

        </div>

        <div class="section">

        <h2>Projects</h2>

        {format_bullets(projects)}

        </div>

        <div class="section">

        <h2>Skills</h2>

        {format_bullets(skills)}

        </div>

        <div class="section">

        <h2>Achievements</h2>

        {format_bullets(achievements)}

        </div>

        </body>

        </html>
        """

    # content = (
    #     content.replace("```html", "")
    #         .replace("```", "")
    #         .strip()
    # )

    # review_prompt = f"""
    # You are an experienced ATS reviewer.

    # Review ONLY the following resume.

    # {content}

    # Evaluate it using these criteria.

    # Return EXACTLY in this format.

    # ATS_SCORE: <number>

    # MISSING_KEYWORDS:
    # - ...

    # WEAK_POINTS:
    # - ...

    # SUGGESTIONS:
    # - ...

    # Do NOT rewrite the resume.
    # Only review it.
    # """

    # review = client.chat.completions.create(
    #     model="qwen/qwen3-32b",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": review_prompt
    #         }
    #     ],
    #     temperature=0
    # )

    # review = review.choices[0].message.content

    # match = re.search(
    #     r"ATS_SCORE:\s*(\d+)",
    #     review
    # )

    # score = 0

    # if match:
    #     score = int(match.group(1))

    # if score < 85:

    #     improve_prompt = f"""
    #         You previously generated this resume.

    #         Resume:

    #         {content}

    #         An ATS reviewer reviewed it.

    #         Review:

    #         {review}

    #         Improve the resume using EVERY suggestion.

    #         Requirements:

    #         - Include missing keywords naturally.

    #         - Strengthen weak bullet points.

    #         - Improve formatting.

    #         - Keep it to one page.


    #         Do not explain anything.

    #         Return ONLY the following sections.

    #         NAME

    #         CONTACT

    #         EDUCATION

    #         EXPERIENCE

    #         PROJECTS

    #         SKILLS

    #         ACHIEVEMENTS

    #         Use exactly these section names.

    #         Do not return HTML.

    #         Do not return Markdown.

    #         Do not explain anything.
    #         """

    #     improved = client.chat.completions.create(
    #         model="qwen/qwen3-32b",
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": improve_prompt
    #             }
    #         ],
    #         temperature=0.2
    #     )

    #     content = (
    #         improved.choices[0]
    #         .message.content
    #         .replace("```html", "")
    #         .replace("```", "")
    #         .strip()
    #     )

    return html



def generate_pdf_from_html(html_content: str, output_path="final_resume.pdf"):
    try:
        HTML(string=html_content).write_pdf(output_path)
        print(f"PDF generated successfully: {output_path}")
    except Exception as e:
        print("Error generating PDF:", e)
        raise
