import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

def send_message(recipients, subject, body, attachmentpath=None):
	body = Content('text/html', body + "<br><em>Delivered by Book O' Piracy</em>")
	mail = Mail("pirate-parceler@book-o-piracy.com", subject, recipients[0], body)
	response = sg.client.mail.send.post(request_body=mail.get())
	print(response.status_code)
	print(response.body)
	print(response.headers)
'''from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email import encoders
from os.path import basename
import smtplib

def compose_message(recipients, subject, body, attachmentpath=None):
	# Create MIME message
	msgs = list()
	for recipient in recipients:
		msg = MIMEMultipart()
		msg['To'] = recipient
		msg['Subject'] = subject
		msg['From'] = "pirate-parceler@book-o-piracy.com"

		# Text part
		text = MIMEText(body + "<br><em>Delivered by Book O' Piracy</em>", 'html')
		msg.attach(text)

		# Attachment part, if applicable
		if attachmentpath:
			filename = basename(attachmentpath)
			with open(attachmentpath, 'rb') as file:
				attachment = MIMEApplication(file.read(), Name=filename)
			encoders.encode_base64(attachment)
			attachment['Content-Disposition'] = f'attachment; filename="{filename}"'
			msg.attach(attachment)
		msgs.append(msg)
	return msgs

def send_message(msgs):
	# Connect to Gmail's smtp server
	server = smtplib.SMTP('gmail-smtp-in.l.google.com', 25)
	print(server)
	server.starttls()
	server.ehlo("book-o-piracy.com")
	for msg in msgs:
		# Verify that the sender actually exists and send it if so
		try:
			server.verify(msg['To'])
			server.send_message(msg)
			print('Sent!')
		except Exception:
			print('Failed')
			continue
	server.quit()

# Testing
#msg = compose_message(["alexrankine@college.harvard.edu"], "hello", "testing", None)
#send_message(msg)'''