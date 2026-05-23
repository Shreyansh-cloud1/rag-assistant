import streamlit as st
import requests

st.title("RAG Knowledge Assistant")

question = st.text_input("Ask a question")

if st.button("Submit") and question:
    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"question": question},
        timeout=300,
    )
    data = response.json()

    st.subheader("Answer")
    st.write(data["answer"])

    st.subheader("Retrieved Sources")
    for source in data["sources"]:
        st.write(source)