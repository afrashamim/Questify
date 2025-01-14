# 📄 Questify- Question generator cum Answer checker

## 🌟 Overview

This project is a web application that allows users to:
- Upload a PDF file for processing. 📤
- Extract its content automatically. 📜
- Generate questions based on the text using GROC API key. ❓
- Input answers for evaluation. 📝
- Receive immediate feedback on the correctness of the answers. ✔️

## ✨ Features

### 📤 PDF Upload
- Users can upload a PDF file for processing.
- The application extracts text content from the uploaded file.

### ❓ Question Generation
- Questions are automatically generated using the GROC API key

### 📝 Answer Input and Feedback
- Users can input their answers to the generated questions.
- The application checks answers against correct ones and provides feedback.

### 💻 Responsive Web Interface
- Built with Flask, HTML, CSS, and JavaScript for a seamless user experience.
  


## ⚙️ Installation

### Prerequisites

-🐍 Python 3.9

-📦 Pip for package management.

### Steps:

1.Clone the repository:

```
git clone https://github.com/your-username/Questify.git
```

2.Install dependencies:

```
pip install Flask PyPDF2 requests groq
```

3.Run the flask application:

```
python run.py
```

4.Navigate to your given browser.

## 📂File Structure

```
Questify/
| ├── app/
| |    └── static/
| |        |   └── css/
| |        |   │   ├── styles.css
| |        |   │   └── upload.png
| |        |   └── images/
| |        |   |      └──logo.png
| |        |   └──js/
| |        |       └──app.js
| |        └── templates/ 
| |                ├──quiz.html
| |                ├──results.html
| |                └──upload.html
| ├──__init__.py 
| ├──question_generator.py
| └── routes.py
├──uploads/
└──run.py
```

## 🔚 Conclusion

The Questify Application serves as a powerful tool for automating the process of extracting content from PDF files, generating questions, and evaluating answers. The application simplifies learning and assessment processes.
This project demonstrates the potential of combining technologies like Flask, API Keys, and web development to create practical and impactful solutions.
