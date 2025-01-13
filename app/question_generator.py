import requests
from PyPDF2 import PdfReader

GROC_API_KEY = "your_api_key"
GROC_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Fixed API endpoint

def extract_text_from_pdf(pdf_path):
    """Extracts text from the uploaded PDF."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_questions(pdf_path):
    """Generates questions using the GROC API."""
    text = extract_text_from_pdf(pdf_path)

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that generates quiz questions. Generate exactly 5 questions in a structured format. Each question should be a complete sentence ending with a question mark. Do not include answers or additional formatting."
            },
            {
                "role": "user",
                "content": f"Based on this text, generate exactly 5 questions:\n\n{text}"
            }
        ],
        "model": "llama-3.3-70b-versatile"
    }

    headers = {
        "Authorization": f"Bearer {GROC_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(GROC_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        api_response = response.json()
        try:
            messages = api_response.get('choices', [])
            if messages:
                question_content = messages[0].get('message', {}).get('content', "")
                # Split content into questions and clean them up
                questions = [q.strip() for q in question_content.split('\n') if q.strip() and '?' in q]
                # Take only the first 5 questions
                questions = questions[:5]
                return questions
            else:
                print("Error: No choices found in the API response.")
        except KeyError as e:
            print(f"Error: Missing expected key in the API response: {e}")
        return []
    else:
        print("API Error:", response.status_code, response.text)
        raise Exception(f"Failed to generate questions: {response.status_code} {response.text}")

def evaluate_answers(questions, user_answers):
    """Evaluates user answers using the GROC API."""
    # Prepare the evaluation prompt
    evaluation_prompts = []
    for idx, question in enumerate(questions):
        user_answer = user_answers.get(f"question_{idx + 1}", "").strip()
        evaluation_prompts.append(f"Question: {question['question']}\nUser Answer: {user_answer}")
    
    evaluation_text = "\n\n".join(evaluation_prompts)
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": """You are an answer evaluator. For each question and answer pair, determine if the answer is correct (1) or incorrect (0). 
                Evaluate based on meaning rather than exact wording. Be somewhat lenient - if the answer shows understanding of the concept, 
                consider it correct. Return only a comma-separated list of 1s and 0s, nothing else."""
            },
            {
                "role": "user",
                "content": f"Evaluate these question-answer pairs:\n\n{evaluation_text}"
            }
        ],
        "model": "llama-3.3-70b-versatile"
    }

    headers = {
        "Authorization": f"Bearer {GROC_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GROC_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            api_response = response.json()
            evaluation_result = api_response['choices'][0]['message']['content'].strip()
            
            # Convert the comma-separated string to a list of integers
            scores = [int(score.strip()) for score in evaluation_result.split(',')]
            
            total_correct = sum(scores)
            total_questions = len(questions)
            percentage = (total_correct / total_questions) * 100 if total_questions else 0
            
            # Create feedback for each answer
            feedback = []
            for idx, (score, question) in enumerate(zip(scores, questions)):
                user_answer = user_answers.get(f"question_{idx + 1}", "").strip()
                feedback.append({
                    'question': question['question'],
                    'user_answer': user_answer,
                    'is_correct': bool(score)
                })
            
            return {
                "score": total_correct,
                "total": total_questions,
                "percentage": round(percentage, 1),
                "feedback": feedback
            }
        else:
            print(f"API Error: {response.status_code}")
            return {"score": 0, "total": len(questions), "percentage": 0, "feedback": []}
            
    except Exception as e:
        print(f"Evaluation error: {str(e)}")
        return {"score": 0, "total": len(questions), "percentage": 0, "feedback": []}


if __name__ == "__main__":
    pdf_path = r"C:\Users\ACER\OneDrive\Desktop\Afra\Questify\uploads\sample.pdf"  # Correct file path
    extracted_text = extract_text_from_pdf(pdf_path)
    print("Extracted Text:", extracted_text)

    questions = generate_questions(pdf_path)
    if questions:
        print("Generated Questions:", questions)
    else:
        print("No questions generated.")
