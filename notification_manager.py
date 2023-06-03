from twilio.rest import Client
import os
from dotenv.main import load_dotenv

load_dotenv()

account_sid = os.environ.get("ACC_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def send_message(self, message):
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=message,
            from_='+13613261561',
            to='+40765559630')

        print(message.status)
