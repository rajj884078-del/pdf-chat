# Chat with your PDF 

An AI webapp where anybody can upload their pdf and ask any question about it. AI will read the document. RAG is used 
to make it.


## What it does 

- User uploads pdf
- Asks anything about pdf
- AI reads PDF contents and answers 
- With loading spinner and clear interface


## Tech Stack

- Python 
- Streamlit (web app)
- Google Gemini API (AI model)
- pypdf (PDF text extraction)
- RAG (Retrieval-Augmented Generation)

## How to run

1. Install libraries: `pip install streamlit google-genai pypdf`
2. Put your Gemini API Key in `.streamlit/secrets.toml` 
3. Run `streamlit run pdfchat.py`


## Made by

Raj Jaiswal
