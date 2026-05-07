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
    keywords: list
) -> str:

    resume_text = resume_text[:5000]
    keywords = keywords[:20]

    prompt = f"""
                You are a professional ATS resume writer.

                Your task:
                - Improve and rewrite the resume professionally
                - Naturally incorporate relevant keywords
                - Correct grammar and wording
                - Keep content concise and impactful
                - Do NOT invent fake experience/projects
                - Return ONLY structured resume content

                RETURN YOUR RESPONSE IN THIS EXACT FORMAT:

                NAME:
                ...

                CONTACT:
                ...

                SKILLS:
                - ...
                - ...

                EDUCATION:
                - ...

                EXPERIENCE:
                - ...
                - ...

                PROJECTS:
                - ...
                - ...

                AWARDS:
                - ...
                - ...

                Resume:
                {resume_text}

                Keywords:
                {', '.join(keywords)}
            """

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()

    # ---------- Parse Sections ----------

    def extract_section(section_name):

        import re

        pattern = rf"{section_name}:\s*(.*?)(?=\n[A-Z ]+?:|\Z)"

        match = re.search(
            pattern,
            content,
            re.DOTALL
        )

        return match.group(1).strip() if match else ""

    name = extract_section("NAME")
    contact = extract_section("CONTACT")
    skills = extract_section("SKILLS")
    education = extract_section("EDUCATION")
    experience = extract_section("EXPERIENCE")
    projects = extract_section("PROJECTS")
    awards = extract_section("AWARDS")

    # ---------- Fixed HTML Template ----------

    html = f"""
                <!DOCTYPE html>
                <html>

                <head>
                <meta charset="UTF-8">

                <style>

                @page {{
                    size: A4;
                    margin: 0.5in;
                }}

                body {{
                    font-family: "Times New Roman", serif;
                    font-size: 12px;
                    line-height: 1.4;
                    color: black;
                }}

                h1 {{
                    text-align: center;
                    font-size: 24px;
                    margin-bottom: 5px;
                }}

                .contact {{
                    text-align: center;
                    font-size: 12px;
                    margin-bottom: 20px;
                }}

                .section {{
                    margin-top: 18px;
                }}

                .section-title {{
                    font-size: 16px;
                    font-weight: bold;
                    border-bottom: 1px solid black;
                    margin-bottom: 8px;
                    padding-bottom: 2px;
                }}

                ul {{
                    margin-top: 5px;
                    padding-left: 18px;
                }}

                li {{
                    margin-bottom: 5px;
                }}

                p {{
                    margin: 0;
                }}

                </style>
                </head>

                <body>

                <h1>{name}</h1>

                <div class="contact">
                    {contact}
                </div>

                <div class="section">
                    <div class="section-title">Skills</div>
                    <p>{skills.replace(chr(10), "<br>")}</p>
                </div>

                <div class="section">
                    <div class="section-title">Education</div>
                    <p>{education.replace(chr(10), "<br>")}</p>
                </div>

                <div class="section">
                    <div class="section-title">Experience</div>
                    <p>{experience.replace(chr(10), "<br>")}</p>
                </div>

                <div class="section">
                    <div class="section-title">Projects</div>
                    <p>{projects.replace(chr(10), "<br>")}</p>
                </div>

                <div class="section">
                    <div class="section-title">Awards</div>
                    <p>{awards.replace(chr(10), "<br>")}</p>
                </div>

                </body>
                </html>
            """

    return html

def generate_pdf_from_html(html_content: str, output_path="final_resume.pdf"):
    try:
        HTML(string=html_content).write_pdf(output_path)
        print(f"PDF generated successfully: {output_path}")
    except Exception as e:
        print("Error generating PDF:", e)
        raise
