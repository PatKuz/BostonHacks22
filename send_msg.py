from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
import yaml


def send_message(messageToSend, toNum):
    # print('sending message')
    
    creds = yaml.safe_load(open("creds.yaml", "r"))
    account_sid = creds['TWILIO_ACCOUNT_SID']
    auth_token = creds['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    fromNum = creds['TWILIO_FROM']

    message = client.messages.create(
            body= messageToSend,
            from_=fromNum,
            to= "+1" + str(toNum),
        )
    print(f'sent message to: {toNum}')

# send_message("test message", 7817388373)