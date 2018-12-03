from docx import Document

# Extract and translate text from the paragraphs of a .docx file
def get_docx(filename):
	doc = Document(f'{UPLOAD_FOLDER}/{filename}')
	for para in doc.paragraphs:
		para.text = get_translated(para.text)
	doc.save(f'{UPLOAD_FOLDER}/{filename}')


# Extract and translate text of a .txt file
def get_text(filename):
	with open(f'{UPLOAD_FOLDER}/{filename}', 'r+') as file:
		text = file.read()
		file.seek(0)
		file.write(get_translated(text))
		file.truncate()

