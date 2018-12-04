from flask import Flask, session, render_template, request, Markup, redirect, url_for, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from tools.messaging import compose_message, send_message
from tools.translate import get_translated
from tools.doc import get_docx, get_text
from tempfile import mkdtemp
from os import path, urandom
from werkzeug.utils import secure_filename
from datetime import datetime
from docx import Document

UPLOAD_FOLDER = 'usrfiles'
ALLOWED_EXTENSIONS = set(['.txt', '.docx'])

app = Flask(__name__)
#### CONFIGS ####
app.secret_key = urandom(16)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Local db for testing
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/translations'
# Cookie-related stuff
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
#### END CONFIGS ####
Session(app)

# Production env database setup
heroku = Heroku(app)
db = SQLAlchemy(app)

# Easiest to include these functions in the main app.py
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


def check_file(filename):
	ext = path.splitext(filename)[1]
	if ext in ALLOWED_EXTENSIONS:
		return ext
	return False


# Message model
class Message(db.Model):
	__tablename__ = 'messages'
	id = db.Column(db.Integer, primary_key=True)
	translation = db.Column(db.Text, nullable=False)
	time = db.Column(db.DateTime, nullable=False)

	def __init__(self, translation, time):
		self.translation = translation
		self.time = time


	def __repr__(self):
		return f'Message sent at {str(self.time)}'


@app.route('/')
def index():
	# Get sorted 'messages' table and pass into index.html
	sorted_query = Message.query.order_by(Message.time.desc()).all()
	data = list()
	for message in sorted_query:
		data.append((message.translation, str(message.time)))
	return render_template('index.html', data=data)


@app.route('/translate', methods=['GET', 'POST'])
def translate():
	if request.method == 'POST':
		# Get form inputs and validate
		text = request.form.get('translation_text')
		addressee = request.form.get('addressee')
		addresser = request.form.get('addresser')

		if not text or not addressee or not addresser:
			flash('Bad input')
			return redirect(url_for('index'))

		# Validate presence of file input
		file = None
		if 'document_upload' in request.files:
			file = request.files['document_upload']

		# Get file input
		ext = None
		filename = None

		if file:
			# Check if extension of file is valid
			ext = check_file(file.filename)
			if ext and file.filename != '':
				# Save file
				filename = secure_filename(file.filename)
				file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
				# Translate contents of file
				if ext == '.docx':
					get_docx(filename)
				if ext == '.txt':
					get_text(filename)

		# Handling multiple recipients
		recipients = [recipient.strip() for recipient in addressee.split(',')]

		# Save translated message as a cookie
		try:
			text = get_translated(text)
		except Exception:
			flash('Failed to query translation API!')
			return redirect(url_for('index'))
		session['message'] = {'text': text, 'addressee': addressee, 'addresser': addresser, 'file': filename}

		return redirect('preview')
	if request.method == 'GET':
		return render_template('translate.html')


@app.route('/preview', methods=['GET', 'POST'])
def preview():
	# Ensures the cookie has loaded
	try:
		message = session['message']
	except KeyError:
		redirect('preview')

	if request.method == 'GET':
		return render_template('preview.html', message=message)
	if request.method == 'POST':
		# Translate text and send email 
		text = message['text']
		msg = compose_message([message['addressee']], 'parcel from ' + message['addresser'], text, f"{UPLOAD_FOLDER}/{message['file']}" if message['file'] is not None else None)
		send_message(msg)

		# Commit new Message to database
		message = Message(text, datetime.now())
		db.session.add(message)
		db.session.commit()

		flash('Successfully sent!')
		return redirect(url_for('index'))


if __name__ == '__main__':
	app.run()
