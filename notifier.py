from os import environ
from slack_sdk import WebClient
from time import sleep
from twilio.rest import Client


class Notifier:
    def __init__(self):
        self.url = "https://handler.twilio.com/twiml/EH3ab3f9548b34cca8c5f6f2c5bc26f5d9"
        self.phone_number = "+17792329315"
        self.phone_to_call = environ.get("DESTINATION_PHONE_NUMBER", default="+351913558518")
        self.twilio_client = Client()
        self.slack_web_client = WebClient(token=environ.get("SLACK_BOT_TOKEN"))
        self.slack_user_monitor_id = environ.get("SLACK_MONITOR_USER_ID")

    def call(self):
        print("CREATING CALL")
        call = self.twilio_client.calls.create(
            from_=self.phone_number,
            to=self.phone_to_call,
            url=self.url
        )
        for i in range(30):
            if self.twilio_client.calls.get(sid=call.sid).fetch().status == "busy" or self.twilio_client.calls.get(sid=call.sid).fetch().status == "no-answer":
                print("CALL ANSWERED! EXITING CALL")
                return call
            else:
                print(f"TENTATIVE {i + 1} TO GET BUSY STATUS")
                sleep(1)

        print("WAITING TIME FOR CALL ANSWER FINISHED, RETRYING THE CALL")
        self.call()

    def slack_message(self, violation_list: list):
        if len(violation_list) > 0:
            message = f"Hey bro the following jobs violated the SLA: {violation_list}"
        else:
            message = "The monitor had an unknown problem, please open the ETL_MONITOR job on Jenkins to check."
        self.slack_web_client.chat_postMessage(channel=self.slack_user_monitor_id, text=message)
        print("Slack message sent")

    @staticmethod
    def notify(violation_list=None):
        if violation_list is None:
            violation_list = []
        notifier = Notifier()
        notification_method = environ.get("NOTIFICATION_METHOD", default="call").lower()
        if notification_method.find("call") >= 0:
            notifier.call()
        elif notification_method.find("slack") >= 0:
            notifier.slack_message(violation_list=violation_list)
