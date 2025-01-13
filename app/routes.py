import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from app.question_generator import generate_questions, evaluate_answers

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('upload.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['pdf_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            session['pdf_path'] = filepath
            return redirect(url_for('main.quiz'))
    return render_template('upload.html')

@bp.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        pdf_path = session.get('pdf_path')
        if not pdf_path:
            flash('No PDF file uploaded')
            return redirect(url_for('main.upload'))
        
        # Generate questions from the PDF
        generated_questions = generate_questions(pdf_path)
        
        # Format questions for template
        questions = [{'question': q} for q in generated_questions]
        
        # Store questions in session for later use
        session['questions'] = questions
        
        return render_template('quiz.html', questions=questions)
    
    elif request.method == 'POST':
        questions = session.get('questions', [])
        user_answers = {}
        
        # Collect user answers
        for i in range(len(questions)):
            answer_key = f'question_{i+1}'
            user_answers[answer_key] = request.form.get(answer_key, '')
        
        # Evaluate answers
        results = evaluate_answers(questions, user_answers)
        
        return render_template('results.html', results=results)