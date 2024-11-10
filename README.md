Resume Parsing Flask Application
This Flask application allows users to upload a resume (in PDF or text format) and receive a parsed analysis based on specific company criteria. The application leverages the OpenAI API to analyze resumes and match them against predefined criteria, such as required skills, education, and experience.

Features
Upload Resumes: Users can upload resumes in PDF or text format.
Automatic Parsing and Analysis: Extracts and analyzes sections related to experience, skills, education, and certifications.
Criteria Matching: Compares parsed resume data against predefined company criteria and provides a match result.
Prerequisites
To run this project locally, you’ll need:

Python 3.x installed on your machine.
An OpenAI API Key: Sign up at OpenAI if you don’t have one.
Project Structure
bash
Copy code
project_folder/
├── app.py               # Main Flask application file
├── templates/
│   └── upload.html      # HTML template for the upload page
├── uploads/             # Directory for uploaded files
├── .env                 # Environment file for sensitive keys (not included in Git)
└── requirements.txt     # List of dependencies
Installation and Setup
Follow these steps to set up and run the application on your local machine:

1. Clone the Repository
Clone the repository to your local machine and navigate into the project folder:

bash
Copy code
git clone <your-github-repo-url>
cd project_folder
2. Create and Activate a Virtual Environment
It’s recommended to use a virtual environment to manage dependencies:

Create a virtual environment:

bash
Copy code
python -m venv venv
Activate the virtual environment:

On Windows:
bash
Copy code
venv\Scripts\activate
On macOS/Linux:
bash
Copy code
source venv/bin/activate
3. Install Dependencies
Install the required Python packages listed in requirements.txt:

bash
Copy code
pip install -r requirements.txt
4. Configure the OpenAI API Key
To keep the API key secure, the application loads it from a .env file.

Create a .env file in the project root directory (the same directory as app.py) and add the OpenAI API key:

plaintext
Copy code
OPENAI_API_KEY=sk-yourapikeyhere
Replace sk-yourapikeyhere with your actual OpenAI API key.

5. Run the Application
Start the Flask application using the following command:

bash
Copy code
flask run
If you encounter an error, you may need to set the FLASK_APP environment variable:

On Windows:
bash
Copy code
set FLASK_APP=app.py
On macOS/Linux:
bash
Copy code
export FLASK_APP=app.py
Then, rerun:

bash
Copy code
flask run
Once the server is running, open a web browser and go to http://127.0.0.1:5000/ to access the application.

6. Usage
Open the App: In your web browser, navigate to http://127.0.0.1:5000/.
Upload a Resume: Click on the "Upload Resume" button, select a PDF or text file, and submit it.
View Results: The application will display parsed resume details and a comparison against the company criteria.
Dependencies
All dependencies are listed in requirements.txt. Key dependencies include:

Flask: A micro web framework for Python.
PyMuPDF (fitz): Used to read and extract text from PDF files.
OpenAI: For interacting with the OpenAI API.
python-dotenv: To load environment variables from a .env file.
Notes
Ensure your OpenAI API key is kept secure and not shared in public repositories.
The uploads/ directory is created automatically to store uploaded files.
