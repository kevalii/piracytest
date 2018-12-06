from docx import Document

# Extract and translate most text of a .txt file
def get_docx(filename):
	doc = Document(f'{UPLOAD_FOLDER}/{filename}')
	for para in doc.paragraphs:
		para.text = get_translated(escape(para.text).replace('<br>'), '\n')
	doc.save(f'{UPLOAD_FOLDER}/{filename}')


# Extract and translate text of a .txt file
def get_text(filename):
	with open(f'{UPLOAD_FOLDER}/{filename}', 'r+') as file:
		text = file.read()
		file.seek(0)
		# First 'escape' all newlines with <br> then reverse once translated
		# The translation API doesn't accept newline characters in the request body
		file.write(get_translated(escape(text)).replace('<br>', '\n'))
		file.truncate()

# Use to escape newlines
def escape(text):
	return text.replace('\n', '<br>')