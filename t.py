from django.core.mail import EmailMessage
import threading
class EmailThread(threading.Thread):
	def __init__(self, subject, html_content, rcpt):
		self.subject = subject
		self.rcpt = rcpt
		self.html_content = html_content
		threading.Thread.__init__(self)
	def run (self):
		msg = EmailMessage(self.subject, self.html_content, to = self.rcpt)
		msg.send()

def send_email(subject, html_content, rcpt):
	EmailThread(subject, html_content, rcpt).start()


send_email('123123', '123123213', ['mike111133@yandex.ru'])
