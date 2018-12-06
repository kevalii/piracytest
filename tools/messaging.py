import sendgrid
from sendgrid.helpers.mail import *
from os import environ
from os.path import basename
from base64 import b64encode, decode
# Initialize SendGrid client
sg = sendgrid.SendGridAPIClient(apikey=environ.get('SENDGRID_API_KEY'))

def send_message(recipients, subject, body, attachmentpath=None):
	# Setting up email 
	data = compose_message(recipients, subject, body, attachmentpath)
	response = sg.client.mail.send.post(request_body=data)
	## Logging
	print(response.status_code)
	print(response.body)
	print(response.headers)

def compose_message(recipients, subject, body, attachmentpath):
	# Set up headers of request
	body = Content('text/html', body + "<br><em>Delivered by Book O' Piracy</em>")
	mail = Mail()
	mail.subject = subject
	mail.from_email = Email("pirate-parceler@book-o-piracy.com")

	# For adding multiple recipients
	personalization = Personalization()
	for recipient in recipients:
		personalization.add_to(Email(recipient))
	mail.add_personalization(personalization)
	# Adding content to email
	mail.add_content(body)
	# Setting up attachment content
	if attachmentpath:
		attachment = Attachment()
		filename = basename(attachmentpath)
		with open(attachmentpath, 'rb') as file:
			content = file.read()

		# Data of the attachment must be encoded to be successfully sent
		attachment.content = b64encode(content).decode()
		# MIMEType encompassing .docx and .txt among other file types
		attachment.type = 'application/octet-stream'
		attachment.filename = basename(attachmentpath)
		attachment.disposition = 'attachment'
		mail.add_attachment(attachment)

	return mail.get()