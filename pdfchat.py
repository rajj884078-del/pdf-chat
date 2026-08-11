import streamlit as st
from pypdf import PdfReader 
from google import genai

client = genai.Client(api_key=st.secrets["GEMINI_KEY"])

st.title("📄 Chat with your PDF")
st.write("Apni koi bhi PDF upload karo aur uske baare mein sawaal poocho. AI aapki file padhke jawab dega.")

uploaded_file = st.file_uploader("Apni PDF upload karo", type="pdf")

if uploaded_file:
	reader = PdfReader(uploaded_file)
	text = ""
	for page in reader.pages:
		text = text + page.extract_text()
	st.success("✅ PDF load ho gayi! Now ask question.")

	que = st.text_input("ASK ABOUT PDF:")
	
	if que:
		with st.spinner("thinking..."):		
			full_prompt = "Ye document ka content hai:\n" + text + "\n\nIske base par answer do: " + que
			ans = client.models.generate_content(
				model = "gemini-3.6-flash",
				contents = full_prompt
		)
			st.write(ans.text)
	

