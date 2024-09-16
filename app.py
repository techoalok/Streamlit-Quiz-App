import streamlit as st
from teacher import teacher_dashboard
from student import student_dashboard, view_student_results

def main():
    st.sidebar.title("Navigation")
    if 'user' in st.session_state:
        if st.session_state['role'] == 'teacher':
            option = st.sidebar.selectbox("Choose a dashboard", ["Teacher Dashboard"])
            if option == "Teacher Dashboard":
                teacher_dashboard()
        elif st.session_state['role'] == 'student':
            option = st.sidebar.selectbox("Choose a dashboard", ["Student Dashboard", "View Results"])
            if option == "Student Dashboard":
                student_dashboard()
            elif option == "View Results":
                view_student_results()
    else:
        option = st.sidebar.selectbox("Choose a dashboard", ["Teacher Login", "Student Login"])
        if option == "Teacher Login":
            teacher_dashboard()
        elif option == "Student Login":
            student_dashboard()

if __name__ == "__main__":
    main()
