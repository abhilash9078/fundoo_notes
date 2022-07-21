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
    @shared_task
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email='princeabhi966@gmail.com',
            to=[data['to_email']]
        )
        email.send()
