from os import environ
from time import sleep
from twilio.rest import Client


class Notifier:
    def __init__(self):
        self.url = "https://handler.twilio.com/twiml/EH3ab3f9548b34cca8c5f6f2c5bc26f5d9"
        self.phone_number = environ.get("SOURCE_PHONE_NUMBER", default="+16786662308")
        self.phone_to_call = environ.get("DESTINATION_PHONE_NUMBER", default="+351913558518")
        self.client = Client()

    def call(self):
        print("CREATING CALL")
        call = self.client.calls.create(
            from_=self.phone_number,
            to=self.phone_to_call,
            url=self.url
        )
        for i in range(30):
            if self.client.calls.get(sid=call.sid).fetch().status == "busy" or self.client.calls.get(sid=call.sid).fetch().status == "no-answer":
                print("CALL ANSWERED! EXITING CALL")
                return call
            else:
                print(f"TENTATIVE {i + 1} TO GET BUSY STATUS")
                sleep(1)

        print("WAITING TIME FOR CALL ANSWER FINISHED, RETRYING THE CALL")
        self.call()
