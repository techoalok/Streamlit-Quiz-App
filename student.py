import streamlit as st
from utils import register_student, get_questions_for_class, update_score, get_student_results, authenticate_user, get_classes

def student_login():
    st.title("Student Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = authenticate_user(username, password)
        if role == 'student':
            st.session_state['user'] = username
            st.session_state['role'] = role
            st.success("Logged in successfully!")
            st.session_state['reload'] = True  # Trigger a form reset
        else:
            st.error("Invalid credentials")

def student_dashboard():
    if 'user' not in st.session_state or st.session_state.get('role') != 'student':
        student_login()
        return

    st.title("Student Dashboard")

    # Initialize or clear answers in session state
    if 'answers' not in st.session_state:
        st.session_state['answers'] = {}

    st.header("Register for the Quiz")
    name = st.text_input("Enter Your Name", key='name')
    student_class = st.selectbox("Select Class", get_classes(), key='student_class')

    if st.button("Register"):
        if register_student(name, student_class):
            st.success("Registered successfully!")
            st.session_state['reload'] = True
        else:
            st.warning("You are already registered or the class does not exist.")

    st.header("Take the Quiz")
    student_class = st.selectbox("Select Class to Quiz", get_classes(), key='quiz_class')
    questions_for_class = get_questions_for_class(student_class)

    if questions_for_class:
        score = 0

        for q in questions_for_class:
            question = q["question"]
            options = q["options"]
            default_option = ""  # Initialize default option

            # Display question and options
            st.write(question)
            
            if question not in st.session_state['answers']:
                st.session_state['answers'][question] = default_option  # Set default answer
            
            selected_option = st.radio(
                "Options", 
                options, 
                key=question,
                index=options.index(st.session_state['answers'][question]) if st.session_state['answers'][question] in options else None
            )
            
            # Update the selected option in session state
            st.session_state['answers'][question] = selected_option
            
            if selected_option == q["answer"]:
                score += 1

        if st.button("Submit Quiz"):
            if not name or student_class not in get_classes():
                st.error("Please ensure all fields are filled correctly.")
            else:
                update_score(name, student_class, score)
                st.success(f"Quiz submitted! Your score is {score}/{len(questions_for_class)}")

def view_student_results():
    if 'user' not in st.session_state or st.session_state.get('role') != 'student':
        student_login()
        return

    st.title("View My Results")

    name = st.session_state['user']
    results_df = get_student_results(name=name)
    if not results_df.empty:
        st.write(results_df)
    else:
        st.write("No results found.")

    if st.button("Logout"):
        st.session_state.pop('user', None)
        st.session_state.pop('role', None)
        st.session_state['reload'] = True
