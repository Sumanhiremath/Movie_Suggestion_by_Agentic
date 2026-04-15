import streamlit as st
import requests

query = st.text_input("Ask me about movies")

if st.button("Search"):
    res = requests.post("http://localhost:8000/chat", json={"query": query})
    st.write(res.json()["response"])