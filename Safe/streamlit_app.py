import streamlit as st 

st.set_page_config(page_title="CV", page_icon=":tada:", layout="wide")

with st.container():
    st.title ("CV JOBS")
    st.write("After filling in your information below you will find all the current jobs which are available")
    
with st.container():
    st.subheader("Field of work")
    selected_option = st.selectbox("Select an option:", ["Accounting", "Law", "Engineer", "Information Technology", "Medicine", "Education", "Agriulture"])
    st.write("My field of work is:", selected_option)
    options_dict = {
    "Accounting": ["Bookkeeper", "Budget Analyst", "Actuary", "Charted Accountant"],
    "Law": ["Criminal Law", "Commerical Law", "Family law"],
    "Engineer": ["Electrical Engineer", "Chemical Engineer", "Civil Engineer"],
    "Information Technology": ["Cyber Security", "Cloud Computing", "Business Analyst"],
    "Medicine": ["Pediatrics", "Orthodontist", "Optometrist", "Genral Physician"],
    "Education": ["Foundation", "Senior Phase"],
    "Agriculture": [" Morgen", "Meadow", "Coastal"]
}
    if selected_option in options_dict:
        selected_option_2 = st.selectbox("Select a sub-option:", options_dict[selected_option])
    st.write("My role in my sepcified field is :", selected_option_2)
    
with st.container():
    st.subheader("Experience")
    selected_option = st.selectbox("Select an option:", ["1-2yrs", "3-5yrs", "5-10yrs", "10yrs+"])
    st.write("I have been working for:")
    
with st.container():
    st.subheader("Skills")
    user_info = st.text_area("Enter your skills:")
    st.write(user_info)
    
with st.container():
    st.subheader("Interests")
    user_info = st.text_area("Enter your interests:")
    st.write(user_info)
    st.write("Some of my interests include:")    
    
    
    