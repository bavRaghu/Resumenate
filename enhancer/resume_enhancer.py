import google.generativeai as genai
import pdfkit


# Load Gemini API key
genai.configure(api_key="AIzaSyBKmQ3zca2Ad1FCXes45_RIs1M9clJ4VHw")


def prompt_gemini(resume_text: str, keywords: list) -> str:
    prompt = f"""
    You are a professional resume designer. Return ONLY a raw HTML file (not markdown, not explanation).
    
    Given the following resume:
    {resume_text}

    And the following keywords to include:
    {', '.join(keywords)}

    Generate a complete HTML resume that consist of all of these keywords using the details provided below. The HTML should follow **these strict styling rules**:
    
    1. The output MUST include the aforementioned keywords, naturally while preserving professionalism. You may exclude any keywords that may seem unnecessary in the context, or too complex to include. The keywords must however, be incorporated in a seamless manner, and must be included in natural language. Do not lazily copy-paste all the keywords together in one section. Make it look natural, and enhance the readability of the resume.
    2. The **name** of the candidate should be in font size 20px, bold, and **center-aligned**.
    3. Contact details (email, phone, LinkedIn, location) should be directly below the name in **font size 12px**, **center-aligned**, and separated with vertical bars. DO NOT INCLUDE THE USER'S LINKEDIN EVEN IF IT HAS BEEN PROVIDED.
    4. Each section (**Education**, **Technical Skills**, **Experience**, **Projects**, **Awards**) must:
       - Have a section heading in **font size 16px**, bold, with a bottom border (like a horizontal line).
       - Content in **font size 12px**, aligned to the **left** or **justified** for longer text.
       - Some content like experience/projects may use bullet points.
    5. The entire resume must be in **Arial** font.
    6. Use margins/padding suitable for a clean resume look. Space out sections slightly.
    7. The page size should be **A4 dimensions (2480 x 3508 pixels)** in CSS.
    8. **Do not include any CSS or content that may prevent the file from being converted to PDF.**
    9. The page should be formatted for printing on A4 paper, with 1 inch margins on all sides, using font sizes in pt (not px).
    10. Ensure that no parts are compressed like a web page — the layout must be spaced out like a printable resume.
    11. Do not include any dates in the final resume, only bolden the required sideheadings.
    12. Do not include any unnecessary sections in the resume other than the ones in this list - Name & Personal Information, Objective (if already in the resume DO NOT include if it isn't), Skills (very importantly), Education, Experience, Awards/Honours.
    13. Please correct any, and all spelling / grammatic errors in the resume - considering British English as the standard.
    
    
    Your output should only be the complete HTML document — starting from '<!DOCTYPE html>' to '</html>'.
    Respond ONLY with raw HTML — starting from '<!DOCTYPE html>' to '</html>', without any commentary, markdown formatting, explanation, or code blocks.
    """
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text.strip()


def generate_pdf_from_html(html_content: str, output_path="final_resume.pdf"):
    # Path to your local wkhtmltopdf.exe file
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    options = {
        "page-size": "A4",
        "encoding": "UTF-8",
        "margin-top": "10mm",
        "margin-bottom": "10mm",
        "margin-left": "10mm",
        "margin-right": "10mm",
        "dpi": 300,
        "zoom": "1.3",  # makes the content scale up a bit
        "enable-local-file-access": "",
    }

    try:
        pdfkit.from_string(html_content, output_path, configuration=config, options=options)
        print("✅ PDF successfully generated:", output_path)
    except Exception as e:
        print("❌ Error generating PDF:", e)
