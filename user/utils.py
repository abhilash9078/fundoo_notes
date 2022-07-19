from django.core.mail import EmailMessage
import os


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email='princeabhi966@gmail.com',
            to=['abhilashmeher1234@gmail.com']
        )
        email.send()
