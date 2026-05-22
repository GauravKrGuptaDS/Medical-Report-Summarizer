import streamlit as st
import fitz
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI Medical Report Summarizer")

uploaded_file = st.file_uploader(
    "Upload Medical Report",
    type=["pdf"]
)

def extract_text(pdf_file):
    text = ""

    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text


if uploaded_file:

    report_text = extract_text(uploaded_file)

    prompt = f"""
    You are a medical report summarization assistant.

    Summarize the report in this format:

    1. Key Findings
    2. Abnormal Values
    3. Attention Areas
    4. Easy-to-understand summary

    Medical Report:
    {report_text}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    st.subheader("Medical Summary")

    st.write(response.choices[0].message.content)
