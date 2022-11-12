import os, yaml
from twilio.rest import Client

creds = yaml.safe_load(open("creds.yaml", "r"))
account_sid = creds['TWILIO_ACCOUNT_SID']
auth_token = creds['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def start_verify(number):
    verification = client.verify \
                     .v2 \
                     .services(creds['TWILIO_SERVICE']) \
                     .verifications \
                     .create(to='+1' + str(number), channel='sms')
    return verification.status

def check_verify(number, code):
    verification_check = client.verify \
                           .v2 \
                           .services(creds['TWILIO_SERVICE']) \
                           .verification_checks \
                           .create(to='+1' + str(number), code=str(code))
    return verification_check.status