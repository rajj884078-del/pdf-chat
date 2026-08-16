import streamlit as st
from pypdf import PdfReader
from google import genai
import sqlite3

client = genai.Client(api_key=st.secrets["GEMINI_KEY"])

conn = sqlite3.connect("chats.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS chats (role TEXT, message TEXT)")
conn.commit()

st.title("📄 Chat with your PDF")
st.write("Upload your pdf and ask anything.")

if st.button("New Chat"):
	st.session_state.messages = []
	cursor.execute("DELETE FROM chats")
	conn.commit()

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
	reader = PdfReader(uploaded_file)
	text = ""
	for page in reader.pages:
		text = text + page.extract_text()

st.success("PDF loaded! Now ask.")

if "messages" not in st.session_state:
	st.session_state.messages = []
	cursor.execute("SELECT * FROM chats")
	old = cursor.fetchall()
	for row in old:
		st.session_state.messages.append({"role": row[0], "content": row[1]})

for msg in st.session_state.messages:
	with st.chat_message(msg["role"]):
		st.write(msg["content"])

que = st.text_input("ASK ABOUT PDF:")

if que:
	st.session_state.messages.append({"role": "user", "content": que})
	cursor.execute("INSERT INTO chats VALUES (?, ?)", ("user", que))
	conn.commit()

	conversation = ""
	for msg in st.session_state.messages:
		conversation = conversation + msg["role"] + ": " + msg["content"] + "\n"

	with st.spinner("thinking..."):
		full_prompt = "Ye document hai:\n" + text + "\n\nYe ab tak ki baat-cheet hai:\n" + conversation + "\nAb aakhri sawaal ka chota jawab do."
		ans = client.models.generate_content(
			model="gemini-3.6-flash",
			contents=full_prompt
		)
	st.session_state.messages.append({"role": "assistant", "content": ans.text})
	cursor.execute("INSERT INTO chats VALUES (?, ?)", ("assistant", ans.text))
	conn.commit()
	
	with st.chat_message("assistant"):
		st.write(ans.text)

