from flask import Flask, render_template, request, send_file, jsonify
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

app = Flask(__name__)

# -------------------- PAGE ROUTES --------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


# -------------------- GENERATE RESUME + COVER LETTER --------------------

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    name = data.get("name", "")
    role = data.get("role", "")
    skills = data.get("skills", "")
    education = data.get("education", "")
    projects = data.get("projects", "")
    experience = data.get("experience", "")

    resume_html = f"""
    <h1>{name}</h1>
    <h3>{role}</h3>

    <h2>Professional Summary</h2>
    <p>Motivated and detail-oriented aspiring {role} with strong knowledge in {skills}. 
    Passionate about learning and building impactful solutions.</p>

    <h2>Skills</h2>
    <p>{skills}</p>

    <h2>Education</h2>
    <p>{education}</p>

    <h2>Projects</h2>
    <p>{projects}</p>

    <h2>Experience</h2>
    <p>{experience}</p>
    """

    cover_letter = f"""
    Dear Hiring Manager,

    I am writing to apply for the {role} position.
    With my background in {skills} and academic experience in {education},
    I am eager to contribute effectively to your team.

    Thank you for considering my application.

    Sincerely,
    {name}
    """

    return jsonify({
        "resume": resume_html,
        "cover_letter": cover_letter
    })


# -------------------- DOWNLOAD PDF --------------------

@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    data = request.json

    name = data.get("name", "")
    role = data.get("role", "")
    skills = data.get("skills", "")
    education = data.get("education", "")
    projects = data.get("projects", "")
    experience = data.get("experience", "")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    section_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    # Header
    elements.append(Paragraph(name, title_style))
    elements.append(Paragraph(role, styles["Heading3"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Summary
    elements.append(Paragraph("Professional Summary", section_style))
    elements.append(Paragraph(
        f"Motivated aspiring {role} skilled in {skills}. Passionate about continuous learning.",
        normal_style
    ))
    elements.append(Spacer(1, 0.2 * inch))

    # Other Sections
    sections = {
        "Skills": skills,
        "Education": education,
        "Projects": projects,
        "Experience": experience
    }

    for title, content in sections.items():
        elements.append(Paragraph(title, section_style))
        elements.append(Paragraph(content, normal_style))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Professional_Resume.pdf",
        mimetype="application/pdf"
    )


# -------------------- RUN APP --------------------

if __name__ == "__main__":
    app.run(debug=True)