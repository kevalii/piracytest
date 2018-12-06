import sendgrid
from sendgrid.helpers.mail import *
from os import environ
from os.path import basename
from base64 import b64encode, decode

sg = sendgrid.SendGridAPIClient(apikey=environ.get('SENDGRID_API_KEY'))

def send_message(recipients, subject, body, attachmentpath=None):
	body = Content('text/html', body + "<br><em>Delivered by Book O' Piracy</em>")
	mail = Mail()
	mail.subject = subject
	mail.from_email = Email("pirate-parceler@book-o-piracy.com")

	personalization = Personalization()
	for recipient in recipients:
		personalization.add_to(Email(recipient))

	mail.add_personalization(personalization)
	mail.add_content(body)

	if attachmentpath:
		attachment = Attachment()
		filename = basename(attachmentpath)
		with open(attachmentpath, 'rb') as file:
			content = file.read()

		# Required encoding
		attachment.content = b64encode(content).decode()
		attachment.type = 'application/octet-stream'
		attachment.filename = basename(attachmentpath)
		attachment.disposition = 'attachment'
		mail.add_attachment(attachment)

	response = sg.client.mail.send.post(request_body=mail.get())
	## Logging
	print(response.status_code)
	print(response.body)
	print(response.headers)