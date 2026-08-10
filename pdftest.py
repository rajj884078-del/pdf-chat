from pypdf import PdfReader
reader = PdfReader("test.pdf")
text = ""
for page in reader .pages:
	text = text + page.extract_text()
print(text)

