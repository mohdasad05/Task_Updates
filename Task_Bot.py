import os
import schedule
import time
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve tokens from .env
slack_token = os.getenv("SLACK_BOT_TOKEN")
channel_id = os.getenv("SLACK_CHANNEL_ID")

client = WebClient(token=slack_token)

def send_task_to_slack():
    current_hour = datetime.now().hour

    if 9 <= current_hour or current_hour == 0:
        try:
            task_message = """
            🚀 Task Update Reminder 🚀
            Hey team! 👋 It's time for your hourly update.
            🔹 What’s the update on your current task?
            🔹 Which task are you working on this hour?
            Please reply with your status! ✅
            """

            response = client.chat_postMessage(channel=channel_id, text=task_message)
            print(f"Task sent to Slack at {datetime.now().strftime('%I:%M %p')}: {response['message']['text']}")

        except SlackApiError as e:
            print(f"Error sending message to Slack: {e.response['error']}")
    else:
        print(f"Skipping message, current time is {datetime.now().strftime('%I:%M %p')}")

def run_scheduler():
    schedule.every().hour.at(":00").do(send_task_to_slack)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    print("Starting Slack Bot...")
    run_scheduler()
