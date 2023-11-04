import streamlit as st
import spacy
from PyPDF2 import PdfReader
from io import BytesIO
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Load the spaCy model
nlp = spacy.load("en_core_web_md")

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


def main():
    st.title("🧭 CareerCompass")

    # Add section header for CV upload
    st.write("## ✍️ CV Ranking System")

    # Add a break for spacing
    st.markdown("---")

    # Create a sidebar with a title and an "About Us" section
    with st.sidebar:
        # st.markdown("---")
        st.title("🧭 CareerCompass")  # Add a compass emoji to the title
        st.write("Welcome to CareerCompass, your personal career guide!")
        st.write("We help you find the most suitable job opportunities based on the similarity between your CV and job descriptions.")
        st.markdown("---")

        st.markdown("# 💀 Cheat Code")

        # Create a button with a light bulb emoji to display team members
        if st.button("💡 Show Team Members"):
            st.markdown("👤 Mitheel Ramdaw")
            st.markdown("👤 Ryan Chitate")
            st.markdown("👤 Mikhaar Ramdaw")
            st.markdown("👤 Laeeka Adams")
            st.markdown("👤 Swift")
            st.markdown("👤 TJ")

        st.markdown("---")

    # Use emojis for a playful touch
    st.title("📄 **Upload CVs**")

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


if __name__ == "__main__":
    main()
