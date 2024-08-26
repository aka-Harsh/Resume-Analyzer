from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import streamlit as st 
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content(input,pdf_content[0],prompt)
    return response.text

def input_pdf_setup(uploaded_files):
    if uploaded_files is not None:
        images=pdf2image.convert_from_bytes(uploaded_files.read())

        first_page=images[0]

        img_byte_arr =io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts=[
            {
            "mime_type":"image/jpeg",
            "data":base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Resume Analyzer")
st.header("Analyze your Resume and check ATS score")

