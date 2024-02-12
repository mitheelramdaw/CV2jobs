import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from io import BytesIO
import re
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_lg")

# Sample job descriptions (converted to lowercase)
job_descriptions = [
    "we are looking for a software engineer with experience in python.",
    "hiring a data analyst with strong SQL skills.",
    "seeking a marketing manager with social media expertise.",
]

# Function to calculate similarity between two texts
def calculate_similarity(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    similarity = doc1.similarity(doc2)
    return similarity * 100  # Convert similarity score to a percentage

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to preprocess and clean text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove special characters and punctuation
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Tokenize the text using spaCy
    doc = nlp(text)

    # Remove stop words and lemmatize tokens
    tokens = [token.lemma_ for token in doc if not token.is_stop]

    # Join the tokens back into a string
    cleaned_text = " ".join(tokens)

    return cleaned_text

# Function to rank jobs based on CV similarity
def rank_jobs(uploaded_cvs, uploaded_filenames):
    ranked_jobs = []
    for cv, filename in zip(uploaded_cvs, uploaded_filenames):
        job_scores = []
        cv_cleaned = preprocess_text(cv)
        for i, job_desc in enumerate(job_descriptions):
            # Preprocess and clean the job description text
            job_desc_cleaned = preprocess_text(job_desc)

            similarity_score = calculate_similarity(
                cv_cleaned, job_desc_cleaned)
            job_scores.append(
                {"job_description": job_desc, "similarity_score": similarity_score}
            )
        job_scores = sorted(
            job_scores, key=lambda x: x["similarity_score"], reverse=True)
        ranked_jobs.append({"cv_filename": filename, "job_scores": job_scores})

    return ranked_jobs

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create a user table
def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

# Function to insert a new user
def insert_user(conn, username, password):
    insert_user_sql = """
    INSERT INTO users (username, password) VALUES (?, ?)
    """
    try:
        c = conn.cursor()
        c.execute(insert_user_sql, (username, password))
        conn.commit()
        return c.lastrowid
    except sqlite3.Error as e:
        print(e)

# Function to check if a user exists
def check_user(conn, username, password):
    check_user_sql = """
    SELECT * FROM users WHERE username=? AND password=?
    """
    try:
        c = conn.cursor()
        c.execute(check_user_sql, (username, password))
        user = c.fetchone()
        if user:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(e)

# Function for login/signup page
def login_signup_page():
    conn = create_connection("users.db")
    if conn is not None:
        create_table(conn)

        st.title("Login/Signup Page")

        # Sidebar for login/signup forms
        login_signup = st.sidebar.radio("Login/Signup", ("Login", "Signup"))

        if login_signup == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.button("Login")
            if login_button:
                if check_user(conn, username, password):
                    st.success("Login successful!")
                    return True  # Return True to indicate successful login
                else:
                    st.error("Invalid username or password")
        elif login_signup == "Signup":
            st.subheader("Signup")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            signup_button = st.button("Signup")
            if signup_button:
                if insert_user(conn, new_username, new_password):
                    st.success("Signup successful! You can now login.")
                else:
                    st.error("Error signing up. Please try again.")

    else:
        st.error("Error creating database connection")
    return False  # Return False to indicate unsuccessful login

# Function for main content page
def main_content_page():
    st.title("Main Content")
    st.write("## ✍️ CV Ranking System")

    # Add a break for spacing
    st.markdown("---")

    # Style the file uploader button with a background color
    uploaded_files = st.file_uploader(
        "Upload PDFs", type=["pdf"], accept_multiple_files=True, key="cv_upload")

    st.write("")

    # Style the "Rank Jobs" button with a blue background
    if st.button("Rank Jobs", key="rank_button") and uploaded_files:
        uploaded_cvs = []
        uploaded_filenames = []
        for uploaded_file in uploaded_files:
            cv_text = extract_text_from_pdf(uploaded_file)
            uploaded_cvs.append(cv_text)
            uploaded_filenames.append(uploaded_file.name)

        st.write("")

        # Calculate similarity and rank jobs
        ranked_jobs = rank_jobs(uploaded_cvs, uploaded_filenames)

        # Create a horizontal rule for separation
        # st.markdown("---")

        # Style the CV subheaders with emojis and container layout
        for i, ranked_job in enumerate(ranked_jobs):
            st.markdown("---")
            st.write(f"📃 **CV: {ranked_job['cv_filename'].split('.pdf')[0]}**")

            # Use emojis to style the job list
            for j, job in enumerate(ranked_job['job_scores']):
                st.write(
                    f"👉 **Job {j + 1}**: {job['job_description']} (Similarity: {job['similarity_score']:.2f}%)")
            st.write("")
            # st.markdown("---")

            # Customize the line graph with a darker color and white text
            fig, ax = plt.subplots()
            job_numbers = [
                f"Job {j + 1}" for j in range(len(ranked_job['job_scores']))]
            similarity_scores = [job['similarity_score']
                                 for job in ranked_job['job_scores']]

            # Set a stylish and modern dark theme
            plt.style.use('seaborn-darkgrid')

            # Customize the line graph with a darker color
            ax.plot(job_numbers, similarity_scores,
                    marker='o', linestyle='-', color='#1f77b4')
            ax.set_xlabel('Jobs', color='white')
            ax.set_ylabel('Similarity Score', color='white')
            ax.set_title(
                f'Similarity Scores for CV: {ranked_job["cv_filename"].split(".pdf")[0]}', color='white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')

            st.pyplot(fig)
            plt.close()

        st.markdown("---")

# Main function
def main():
    if login_signup_page():
        st.empty()  # Clear the content of the page
        main_content_page()

if __name__ == "__main__":
    main()