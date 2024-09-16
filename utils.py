import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

# In-memory data storage (use a database for production)
users = {
    'teacher': {'password': generate_password_hash('teacherpass'), 'role': 'teacher'},
    'student': {'password': generate_password_hash('studentpass'), 'role': 'student'}
}

questions = {
    'Class 1': [
        {"question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"},
        {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin", "Madrid"], "answer": "Paris"}
    ],
    'Class 2': [
        {"question": "What is 5 + 3?", "options": ["6", "7", "8", "9"], "answer": "8"},
        {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "answer": "Mars"}
    ]
}

students = pd.DataFrame(columns=['Name', 'Class', 'Score'])

# Functions for user authentication and registration
def authenticate_user(username, password):
    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        return user['role']
    return None

def register_user(username, password, role):
    if username not in users:
        users[username] = {'password': generate_password_hash(password), 'role': role}
        return True
    return False

# Functions for managing classes
def add_class(class_name):
    if class_name not in questions:
        questions[class_name] = []
        return True
    return False

def get_classes():
    return list(questions.keys())

# Functions for managing questions
def add_question(class_name, question, options, answer):
    if class_name in questions:
        questions[class_name].append({
            "question": question,
            "options": options,
            "answer": answer
        })
        return True
    return False

def get_questions_for_class(class_name):
    return questions.get(class_name, [])

# Functions for managing students
def register_student(name, student_class):
    global students
    if (students['Name'] == name).any():
        return False  # Student already registered
    if student_class not in get_classes():
        return False  # Class does not exist
    score = 0  # Default score
    students = pd.concat([
        students,
        pd.DataFrame([[name, student_class, score]], columns=['Name', 'Class', 'Score'])
    ], ignore_index=True)
    return True

def update_score(name, student_class, score):
    global students
    students.loc[(students['Name'] == name) & (students['Class'] == student_class), 'Score'] = score

def get_student_results(name=None, student_class=None):
    global students
    if name and student_class:
        return students[(students['Name'] == name) & (students['Class'] == student_class)]
    return students
