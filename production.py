import streamlit as st
import spacy
from PyPDF2 import PdfReader
from io import BytesIO
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Sample job descriptions (converted to lowercase)
job_descriptions = [
    "we are looking for a software engineer with experience in python.",
    ''' Data Analyst – Excel expert

The company is based in - Enterprise Park, Enterprise Way, Cape Farms, Cape Town

The ideal candidate is adept at using large data sets to find insights and opportunities to enable business growth for our clients. We are looking for a detail-oriented, problem-solver who has proven capability to deliver business insights drawn from data.

Qualifications & Experience

At least three years in a support function in research, working intensively with Excel spreadsheets.
At least an undergraduate degree in accounting, statistics, econometrics or other quantitative field.
Outstanding Excel skills from basic functions through to entry-level macro programming.
Able to produce graphs, tables, and other visual representations of data in an insightful and meaningful way.
Strong problem-solving skills
Excellent written and verbal communication skills for coordinating across teams.
A drive to learn and master new technologies and techniques. ''',
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
    text = text.lower()  # Convert to lowercase
    # Remove special characters and punctuation
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    doc = nlp(text)
    # Tokenize, remove stop words, and lemmatize
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    cleaned_text = " ".join(tokens)  # Join the tokens back into a string
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
            job_scores.append(similarity_score)
        ranked_jobs.append({"cv_filename": filename, "job_scores": job_scores})
    return ranked_jobs


def main():
    st.title("🧭 CareerCompass")
    st.write("## ✍️ CV Ranking System")
    st.markdown("---")

    with st.sidebar:
        st.title("🧭 CareerCompass")
        st.write("Welcome to CareerCompass, your personal career guide!")
        st.write("We help you find the most suitable job opportunities based on the similarity between your CV and job descriptions.")
        st.markdown("---")
        st.markdown("# 💀 Cheat Code")
        if st.button("💡 Show Team Members"):
            st.markdown("👤 Mitheel Ramdaw")
            st.markdown("👤 Ryan Chitate")
            st.markdown("👤 Mikhaar Ramdaw")
            st.markdown("👤 Laeeka Adams")
        st.markdown("---")

    st.title("📄 **Upload CVs**")
    uploaded_files = st.file_uploader(
        "Upload PDFs", type=["pdf"], accept_multiple_files=True, key="cv_upload")
    st.write("")

    if st.button("Rank Jobs", key="rank_button") and uploaded_files:
        uploaded_cvs = []
        uploaded_filenames = []
        for uploaded_file in uploaded_files:
            cv_text = extract_text_from_pdf(uploaded_file)
            uploaded_cvs.append(cv_text)
            uploaded_filenames.append(uploaded_file.name)

        st.write("")
        ranked_jobs = rank_jobs(uploaded_cvs, uploaded_filenames)

        for i, ranked_job in enumerate(ranked_jobs):
            st.markdown("---")
            st.write(f"📃 **CV: {ranked_job['cv_filename'].split('.pdf')[0]}**")
            job_scores = ranked_job['job_scores']
            for j, job_desc in enumerate(job_descriptions):
                st.write(
                    f"👉 **Job {j + 1}**: {job_desc} (Similarity: {job_scores[j]:.2f}%)")
            # Plotting
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(
                x=list(range(1, len(job_scores) + 1)), y=job_scores, palette=['red', 'blue', 'purple', 'green', 'orange'])
            plt.title("Job Similarity Scores", color='white')
            plt.xlabel("Job", color='white')
            plt.ylabel("Similarity Score (%)", color='white')
            plt.ylim(0, 100)
            plt.xticks(ticks=list(range(0, len(job_scores) + 1)), color='white')
            plt.yticks(color='white')
            plt.style.use('dark_background')
            # Adding labels on top of bars
            for idx, score in enumerate(job_scores):
                ax.text(idx, score + 1, f"{score:.2f}%",
                        ha="center", color='white')
            st.pyplot(plt)
            st.write("")


if __name__ == "__main__":
    main()
