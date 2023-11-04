import streamlit as st
import spacy
from PyPDF2 import PdfReader  # Import PdfReader instead of PdfFileReader
from io import BytesIO
import re

# Load the spaCy model
nlp = spacy.load("en_core_web_md")

# Sample job descriptions
job_descriptions = [
    "We are looking for a software engineer with experience in Python.",
    "Hiring a data analyst with strong SQL skills.",
    "Seeking a marketing manager with social media expertise.",
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
    # Use len(pdf_reader.pages) instead of numPages
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to rank jobs based on CV similarity


def rank_jobs(uploaded_cvs):
    ranked_jobs = []
    for cv in uploaded_cvs:
        for i, job_desc in enumerate(job_descriptions):
            similarity_score = calculate_similarity(cv, job_desc)
            ranked_jobs.append(
                {"job_description": job_desc, "similarity_score": similarity_score})

    ranked_jobs = sorted(
        ranked_jobs, key=lambda x: x["similarity_score"], reverse=True)

    return ranked_jobs


def main():
    st.title("CV Ranking System")

    # User uploads multiple PDFs
    uploaded_files = st.file_uploader(
        "Upload PDFs", type=["pdf"], accept_multiple_files=True)

    if st.button("Rank Jobs") and uploaded_files:
        uploaded_cvs = []
        for uploaded_file in uploaded_files:
            cv_text = extract_text_from_pdf(uploaded_file)
            uploaded_cvs.append(cv_text)

        # Calculate similarity and rank jobs
        ranked_jobs = rank_jobs(uploaded_cvs)

        # Display the ranked jobs
        st.subheader("Ranked Jobs:")
        for i, job in enumerate(ranked_jobs):
            st.write(
                f"Rank {i + 1}: {job['job_description']} (Similarity: {job['similarity_score']:.2f}%)")


if __name__ == "__main__":
    main()
