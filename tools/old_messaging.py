''' LEGACY COMPONENT
This is a legacy version of messaging.py from before we integrated with SendGrid API to resolve
issues related to deploying the app onto Heroku. 
For more insight why this implemenation didn't work: 
https://help.heroku.com/CFG547YP/why-am-i-getting-errors-when-sending-email-with-gmail-via-smtp
'''
from email.mime.multipart import MIMEMultipart
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
#send_message(msg)