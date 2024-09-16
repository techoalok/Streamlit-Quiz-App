import streamlit as st
from utils import add_question, get_student_results, add_class, questions, authenticate_user

def teacher_login():
    st.title("Teacher Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = authenticate_user(username, password)
        if role == 'teacher':
            st.session_state['user'] = username
            st.session_state['role'] = role
            st.success("Logged in successfully!")
            st.session_state['reload'] = True  # Trigger a form reset
        else:
            st.error("Invalid credentials")

def teacher_dashboard():
    if 'user' not in st.session_state or st.session_state.get('role') != 'teacher':
        teacher_login()
        return

    st.title("Teacher Dashboard")

    # Check if reload is needed
    if 'reload' in st.session_state and st.session_state['reload']:
        st.session_state['reload'] = False  # Reset reload flag

    st.header("Add New Class")
    new_class = st.text_input("Enter New Class Name", key='new_class')
    if st.button("Add Class"):
        if add_class(new_class):
            st.success(f"Class '{new_class}' added successfully!")
            st.session_state['reload'] = True
        else:
            st.warning(f"Class '{new_class}' already exists!")

    st.header("Add New Questions")
    class_name = st.selectbox("Select Class", list(questions.keys()), key='class_name')
    question = st.text_input("Enter Question", key='question')
    options = st.text_input("Enter Options (comma-separated)", key='options')
    answer = st.text_input("Enter Answer", key='answer')

    if st.button("Add Question"):
        options_list = [option.strip() for option in options.split(',')]
        if add_question(class_name, question, options_list, answer):
            st.success("Question added successfully!")
            st.session_state['reload'] = True
        else:
            st.warning("Failed to add question. Class might not exist.")

    st.header("View Student Results")
    results_df = get_student_results()
    st.dataframe(results_df)

    if st.button("Logout"):
        st.session_state.pop('user', None)
        st.session_state.pop('role', None)
        st.session_state['reload'] = True
