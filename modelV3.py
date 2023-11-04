import streamlit as st
import openai  # Import OpenAI library
from PyPDF2 import PdfReader
from io import BytesIO

# Set up your OpenAI API key
# Replace with your actual API key
openai.api_key = "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"

# Sample job descriptions
job_descriptions = [
    "We are looking for a software engineer with experience in Python.",
    "Hiring a data analyst with strong SQL skills.",
    "Seeking a marketing manager with social media expertise.",
]

# Function to calculate similarity between two texts using GPT-3 API


def calculate_similarity(text1, text2):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Compare the similarity between:\nText 1: {text1}\nText 2: {text2}\nSimilarity score:",
            max_tokens=50  # Adjust as needed
        )
        similarity = float(response.choices[0].text)
        return similarity
    except Exception as e:
        st.error(f"An error occurred while calculating similarity: {e}")
        return 0.0

# Function to extract text from a PDF file


def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
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
