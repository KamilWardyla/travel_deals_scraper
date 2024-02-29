from twilio.rest import Client
import os
from dotenv import load_dotenv


def sms_sender(text, link):
    load_dotenv()
    account_SID = os.environ.get("ACCOUNT_SID")
    auth_token = os.environ.get("AUTH_TOKEN")
    twilio_client = Client(account_SID, auth_token)

    message = twilio_client.messages.create(
        to="534990089",
        from_="+17579749883",
        body=f"{text}\n, Link: {link}"
    )
    print(message.sid)
