import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv


def email_sender(text, link):
    load_dotenv()
    email_sender = os.environ.get("EMAIL_SENDER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_receiver = os.environ.get("EMAIL_RECEIVER")
    email_receiver2 = os.environ.get("EMAIL_RECEIVER2")
    subject = "Nowa Promka na Wakacje :)"
    body = f"""
Nowa promocja na wakacje :):
\n{text},
\nLink do promki: {link}
"""
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        smtp.sendmail(email_sender, email_receiver2, em.as_string())
        return "Wiadomosc wyslana"
