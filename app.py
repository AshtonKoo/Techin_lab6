from tempfile import NamedTemporaryFile
import os
import openai
import streamlit as st
import pdfplumber

OPENAI_API_KEY = "4AqqYoTn277PDToPlplxH8LAE97BShji4jbcFBE57RA"
OPENAI_API_BASE = "https://openai.0x1.tw/api/providers/openai/v1"

openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_API_BASE

st.set_page_config(page_title="PDF AI Chat Bot", page_icon="🤖")

st.title("Chat ONLY with the PDF")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Ask me a question about your document!"}]

uploaded_file = st.file_uploader("Upload a file", type=["pdf"])
document_text = ""
if uploaded_file:
    with NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp.seek(0)
        with pdfplumber.open(tmp.name) as pdf:
            document_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

if prompt := st.text_input("Your question", key="prompt"):
    if document_text and prompt:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert on the content of the document, provide detailed answers to the questions. Use the document to support your answers."},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response.choices[0].message['content']
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Failed to generate a response: {e}")
    else:
        st.error("Please upload a document and ask a question.")

for message in st.session_state.messages:
    role = "You" if message["role"] == "user" else "AI"
    st.text(f"{role}: {message['content']}")
