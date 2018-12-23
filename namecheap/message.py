"""
Contains implementation of function that sends email messages
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ
import smtplib


def send_message(subject: str, message: str) -> None:
    """
    Sends email message
    :param subject:
    :param message:
    :return:
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] = environ['error_mailto']
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP(host=environ['email_hostname'], port=environ['email_port'])
    server.starttls()
    server.login(user=environ['sender_addr'], password=environ['sender_pw'])
    server.sendmail(
        from_addr=environ['sender_addr'],
        to_addrs=environ['error_mailto'],
        msg=msg.as_string())
    server.quit()
