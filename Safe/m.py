import streamlit as st
import spacy
from PyPDF2 import PdfReader
from io import BytesIO
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

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
    return similarity * 100

# Function to extract text from a PDF file


def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


# Define and train the ML model and TF-IDF vectorizer
# Load your dataset
data = pd.read_csv('job_cv_dataset.csv')

# Split the dataset into features and target variable
X = data[['job_description', 'cv_text']]
y = data['similarity_score']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Feature extraction using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(
    X_train['job_description'] + X_train['cv_text'])
X_test_tfidf = tfidf_vectorizer.transform(
    X_test['job_description'] + X_test['cv_text'])

# Create and train a linear regression model
model = LinearRegression()
model.fit(X_train_tfidf, y_train)

# Function to combine NLP and ML for job recommendations


def recommend_jobs(uploaded_cvs):
    ranked_jobs = []
    for cv in uploaded_cvs:
        nlp_similarity_scores = [calculate_similarity(
            cv, job_desc) for job_desc in job_descriptions]
        ml_similarity_scores = model.predict(
            tfidf_vectorizer.transform([cv + job for job in job_descriptions]))

        combined_scores = [(nlp_score + ml_score) / 2 for nlp_score,
                           ml_score in zip(nlp_similarity_scores, ml_similarity_scores)]

        ranked_jobs.extend([(job_desc, combined_score) for job_desc,
                           combined_score in zip(job_descriptions, combined_scores)])

    ranked_jobs = sorted(ranked_jobs, key=lambda x: x[1], reverse=True)

    return ranked_jobs

# Main function


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

        # Get job recommendations
        recommended_jobs = recommend_jobs(uploaded_cvs)

        # Display the recommended jobs
        st.subheader("Recommended Jobs:")
        for i, job in enumerate(recommended_jobs):
            st.write(
                f"Rank {i + 1}: {job[0]} (Combined Score: {job[1]:.2f})")


if __name__ == "__main__":
    st.set_page_config(page_title="Job Recommendation System",
                       page_icon=":clipboard:")
    main()
