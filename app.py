import streamlit as st
import os 
from dotenv import load_dotenv
load_dotenv()

import PyPDF2 as pdf
from  PyPDF2 import PdfReader
import io
import base64 
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input): 
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    
    reader= pdf.PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        
        text = text + str(page.extract_text())
    return text


### PROMPT TEMPLATE

input_prompt = """
Hey Act like a very skilled and experience ATS (Application Tracking System) with a deep understanding of various Technical fields like
software engineering, aritifical intelligence, data science, machine learning, big data, cloud computing, cybersecurity, MLOps, DevOPs, Web Development, App Development and more.
Your task is to analyze and evaluate the resume based on the provided job description. 
You must consider that the job market is highly competitive and the candidate must have a strong technical background according to the job description.
You should provide the best possible assistance for improving the resume. Assign the percentage score matching the resume with the job description.
and the missing skills that the candidate should add to the resume.

resume : {text}
description : {jd}

I want the response in a proper format: 
Job Description Percentage: "%",
Missing Skills: [], Summary: " ", Things to improve: "".






"""



# Streamlit app

st.title("Smart Resume Analyzer")
st.text("Improve your resume with AI")
jd = st.text_area("Enter Job Description", height=200)

uploaded_file = st.file_uploader("Upload your Resume", type = "pdf", help = "Only PDF files are supported")

submit_button = st.button("Analyze")

if submit_button:
    if uploaded_file is not None: 
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input= input_prompt.format(text=text, jd=jd))
        st.subheader(response)
        st.success("Resume analyzed successfully!")
        
        
        
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.subheader("Resume Improvement Chat Assistant")
user_input = st.chat_input("Ask anything about your resume...")
resume_text = input_pdf_text(uploaded_file) 
st.session_state.chat_history = [
    {"role": "user", "parts": [f"This is my resume:\n{resume_text}"]},
    {"role": "model", "parts": ["Got it! You can now ask me anything about your resume."]},
]




if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)

    # Generate response
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=st.session_state.chat_history)
    response = chat.send_message(user_input)

    # Store & show bot response
    st.chat_message("assistant").markdown(response.text)
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})
    st.session_state.chat_history.append({"role": "model", "parts": [response.text]})



