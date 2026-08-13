import streamlit as st
from pypdf import PdfReader 
from google import genai

client = genai.Client(api_key=st.secrets["GEMINI_KEY"])

st.title("📄 Chat with your PDF")
st.write("Apni koi bhi PDF upload karo aur uske baare mein sawaal poocho. AI aapki file padhke jawab dega.")

if st.button("New Chat"):
	st.session_state.messages = []

uploaded_file = st.file_uploader("Apni PDF upload karo", type="pdf")

if uploaded_file:
	reader = PdfReader(uploaded_file)
	text = ""
	for page in reader.pages:
		text = text + page.extract_text()
	st.success("✅ PDF load ho gayi! Now ask question.")
	
	if "messages" not in st.session_state:
		st.session_state.messages = []
		try:
			f = open("chats.txt")
			old = f.read()
			f.close()
			if old:
				st.session_state.messages.append({"role": "assistant", "content": "Old chat:\n" + old})
		except:
			pass

	for msg in st.session_state.messages:
		with st.chat_message(msg["role"]):
			st.write(msg["content"])
	que = st.text_input("ASK ABOUT PDF:")
	
	if que:
		st.session_state.messages.append({"role": "user", "content": que})
		
		conversation = ""
		for msg in st.session_state.messages:
			conversation = conversation + msg["role"] + ": " + msg["content"] + "\n"


		with st.spinner("thinking..."):		
			full_prompt = "Ye document hai:\n" + text + "\n\nYe ab tak ki baat-cheet hai:\n" + conversation + "\nAb aakhri que ka chhota, seedha jawab do."
			ans = client.models.generate_content(
				model = "gemini-3.6-flash",
				contents = full_prompt
		)
			st.session_state.messages.append({"role": "assistant", "content": ans.text})
			f = open("chats.txt", "w")
			f.write(conversation + "Bot: " + ans.text)
			f.close()
			with st.chat_message("assistant"):	
				st.write(ans.text)
	

