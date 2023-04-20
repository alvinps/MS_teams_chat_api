import sys


print('TEST')
import requests
import json

# Access token for your Microsoft account (you need to provide your own)
access_token = 'YOUR_ACCESS_TOKEN_HERE'

# ID of the team and channel to send messages to and retrieve messages from
team_id = 'YOUR_TEAM_ID_HERE'
channel_id = 'YOUR_CHANNEL_ID_HERE'

# Microsoft Graph API URL for sending a message to a channel
send_message_url = f'https://graph.microsoft.com/beta/teams/{team_id}/channels/{channel_id}/messages'

# Microsoft Graph API URL for retrieving messages in a channel
get_messages_url = f'https://graph.microsoft.com/beta/teams/{team_id}/channels/{channel_id}/messages'

# Microsoft Graph API URL for retrieving messages in a channel filtered by mentions
get_mentions_url = f'https://graph.microsoft.com/beta/teams/{team_id}/channels/{channel_id}/messages?$filter=@mention.me'

# Set headers for the API requests
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

def send_teams_message(message, user_id=None):
    """
    Sends a message to a Microsoft Teams chat or channel using the Microsoft Graph API.

    Args:
        message (str): The message content.
        user_id (str): (Optional) The ID of the user to send the message as. If not provided, the message will be sent
                       as the authenticated user.
    """
    data = {
        'body': {
            'content': message
        }
    }
    if user_id is not None:
        data['from'] = {
            'user': {
                'id': user_id
            }
        }
    response = requests.post(send_message_url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        print(f'Message "{message}" sent successfully.')
    else:
        print(f'Error sending message: {response.text}')


def get_most_recent_message():
    """
    Retrieves the most recent message in a Microsoft Teams chat or channel using the Microsoft Graph API.
    """
    response = requests.get(get_messages_url, headers=headers)
    response_json = response.json()
    if 'value' in response_json and len(response_json['value']) > 0:
        latest_message = response_json['value'][0]['body']['content']
        print(f'The most recent message in the channel is: {latest_message}')
    else:
        print('No messages found in the channel.')

def get_most_recent_mention():
    """
    Retrieves the most recent message that mentions the authenticated user in a Microsoft Teams chat or channel using the Microsoft Graph API.
    """
    response = requests.get(get_mentions_url, headers=headers)
    response_json = response.json()
    if 'value' in response_json and len(response_json['value']) > 0:
        latest_mention = response_json['value'][0]['body']['content']
        print(f'The most recent message that mentions you is: {latest_mention}')
    else:
        print('No messages found that mention you.')

# Example usage: send a message to the channel
send_teams_message('Hello, World!')

# Example usage: retrieve the most recent message in the channel
get_most_recent_message()

# Example usage: retrieve the most recent message that mentions the authenticated user in the channel
get_most_recent_mention()
x