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
                You are an expert ATS resume writer and career coach.

                Your task is to professionally enhance and rewrite the resume content.

                IMPORTANT GOALS:
                - Make the resume sound stronger, more technical, and more impactful
                - Expand weak or short bullet points into meaningful professional descriptions
                - Naturally integrate relevant ATS keywords from the provided keyword list
                - Improve wording, grammar, clarity, and professionalism
                - Add strong action verbs and technical phrasing
                - Make the candidate sound competent and technically skilled
                - Keep the content realistic and aligned with the original resume
                - You MAY improve and elaborate existing experience/project descriptions substantially
                - Do NOT leave sections empty or overly short

                VERY IMPORTANT:
                - The output should contain substantial content under each section
                - Skills should contain multiple technologies/tools
                - Experience and Projects should contain detailed bullet points
                - The keywords should appear naturally throughout the resume

                RETURN YOUR RESPONSE IN THIS EXACT FORMAT:

                NAME:
                ...

                CONTACT:
                ...

                SKILLS:
                - ...
                - ...
                - ...

                EDUCATION:
                - ...
                - ...

                EXPERIENCE:
                - ...
                - ...
                - ...

                PROJECTS:
                - ...
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

    def format_bullets(text):

        lines = [
            line.strip("- ").strip()
            for line in text.split("\n")
            if line.strip()
        ]

        if not lines:
            return ""

        html_lines = "".join(
            f"<li>{line}</li>"
            for line in lines
        )

        return f"<ul>{html_lines}</ul>"

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
                    <div class="section-title">Education</div>
                    <p>{format_bullets(education)}</p>
                </div>

                <div class="section">
                    <div class="section-title">Skills</div>
                    <p>{format_bullets(skills)}</p>
                </div>


                <div class="section">
                    <div class="section-title">Experience</div>
                    <p>{format_bullets(experience)}</p>
                </div>

                <div class="section">
                    <div class="section-title">Projects</div>
                    <p>{format_bullets(projects)}</p>
                </div>

                <div class="section">
                    <div class="section-title">Awards</div>
                    <p>{format_bullets(awards)}</p>
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
