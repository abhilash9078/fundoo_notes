from django.core.mail import EmailMessage
import os
from celery import shared_task
from time import sleep


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


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
