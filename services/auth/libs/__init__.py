import os, config
from twilio.rest import Client

client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
service = config.VERIFY_SERVICE_SID

from .twilio import Twilio