import os
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackHistoryDownloader:
    def __init__(self):
        # Initialize Slack client
        slack_token = os.environ["SLACK_BOT_TOKEN"]
        self.client = WebClient(token=slack_token)

    def fetch_channel_history(self, channel_id, user_ids=None, oldest=None, latest=None):
        messages = []
        try:
            response = self.client.conversations_history(
                channel=channel_id,
                oldest=oldest,
                latest=latest
            )
            messages.extend(response['messages'])
            while response['has_more']:
                response = self.client.conversations_history(
                    channel=channel_id,
                    cursor=response['response_metadata']['next_cursor'],
                    oldest=oldest,
                    latest=latest
                )
                messages.extend(response['messages'])
            
            # Filter messages by user IDs if provided
            if user_ids:
                messages = [msg for msg in messages if msg.get('user') in user_ids]
                
        except SlackApiError as e:
            print(f"Error fetching messages: {e}")
        return messages

    def save_history_to_file(self, channel_id, file_name, user_ids=None, oldest=None, latest=None):
        messages = self.fetch_channel_history(channel_id, user_ids, oldest, latest)
        with open(file_name, 'w') as f:
            json.dump(messages, f, indent=4)
        print(f"Saved {len(messages)} messages to {file_name}")

# Example usage
if __name__ == "__main__":
    downloader = SlackHistoryDownloader()
    # Replace 'CHANNEL_ID' with the actual channel ID
    # Optionally, replace 'USER_IDS' with a list of user IDs to filter messages
    downloader.save_history_to_file('CHANNEL_ID', 'channel_history.json', user_ids=['USER_ID1', 'USER_ID2'])