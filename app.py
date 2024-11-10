from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import fitz  # PyMuPDF
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)
def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def parse_resume(resume_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI that specializes in analyzing resumes, even if they are written in unstructured, paragraph form. "
                        "Extract any relevant information related to 'Experience', 'Skills', 'Education', and 'Certifications'. "
                        "If these sections are not explicitly labeled, use contextual clues to identify and list relevant information. "
                        "For example, identify years of experience, job roles, specific skills, degrees, or certifications mentioned within the text."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Please analyze the following resume and extract relevant information:\n\n{resume_text}"
                }
            ],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "Error occurred while parsing the resume."

def match_fields(parsed_resume, company_criteria):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that matches resume fields with company criteria and provides a percentage match."},
            {
                "role": "user",
                "content": (
                    f"Evaluate the following parsed resume against the company's criteria: {json.dumps(company_criteria)}.\n\n"
                    f"Resume data: {parsed_resume}\n"
                    "Please provide a detailed comparison and a percentage match of how well the resume meets the criteria."
                )
            }
        ],
        temperature=0.5
    )
    response_text = response.choices[0].message.content.strip()

    return response_text

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith(('.pdf', '.txt')):
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_path)
        else:
            with open(file_path, 'r') as f:
                resume_text = f.read()

        # Sample company criteria
        company_criteria = {
            "Experience": "At least 3 years in software engineering",
            "Skills": ["Python", "Machine Learning", "Data Analysis", "Cloud Computing"],
            "Education": "B.Sc. in Computer Science or related field",
            "Certifications": ["AWS Certified Solutions Architect"]
        }

        parsed_resume = parse_resume(resume_text)
        matching_result = match_fields(parsed_resume, company_criteria)

        # Save the result to a file
        result_data = {
            "parsed_resume": parsed_resume,
            "matching_result": matching_result
        }
        result_file_path = os.path.join('uploads', f"{os.path.splitext(file.filename)[0]}_result.json")
        with open(result_file_path, 'w') as result_file:
            json.dump(result_data, result_file, indent=4)

        # Clean up uploaded file
        os.remove(file_path)
        return jsonify(result_data)
    return jsonify({"error": "Invalid file type. Please upload a .pdf or .txt file."}), 400

if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
