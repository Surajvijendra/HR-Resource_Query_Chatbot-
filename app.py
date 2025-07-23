import streamlit as st
from hr_bot import ask_hr_bot  

# Streamlit page settings
st.set_page_config(page_title="HR Bot", layout="centered")
st.title("HR Resource Query Chatbot ")

st.write("Ask your HR Query Chatbot for candidates, for example: 'Find Python developers with 3+ years experience'.")

query = st.text_input("Enter your HR query:", placeholder="e.g., Find Python developers with 3+ years experience")

if st.button("Search"):
    if query.strip() == "":
        st.warning("Please enter a query to search for candidates.")
    else:
        with st.spinner("Fetching candidates, please wait..."):
            response = ask_hr_bot(query)
        st.success("Candidates Found:")
        st.write(response)
