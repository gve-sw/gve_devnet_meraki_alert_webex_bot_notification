""" Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import os
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
import sys
import json
import requests

from dotenv import load_dotenv
from adaptive_card import adaptive_card, get_measurement_card, get_confirm_viewing_card, get_refuse_viewing_card, observance_ended_card, get_open_door_alert_card
from send import generate_snapshot, download_file, send_file

# load all environment variables
load_dotenv()

bot_email = os.getenv("TEAMS_BOT_EMAIL")
teams_token = os.getenv("TEAMS_BOT_TOKEN")
bot_url = os.getenv("TEAMS_BOT_URL")
bot_app_name = os.getenv("TEAMS_BOT_APP_NAME")

room_id = os.getenv("WEBEX_ROOM_ID")
beehive_id = os.getenv("BEEHIVE_ID")
beep_api_token = os.getenv("BEEP_API_TOKEN")

meraki_api_key = os.getenv("MERAKI_API_KEY")
merak_serial_front = os.getenv("MERAKI_CAMERA_SERIAL_FRONT")
meraki_serial_side = os.getenv("MERAKI_CAMERA_SERIAL_SIDE")
meraki_serial_distance = os.getenv("MERAKI_CAMERA_SERIAL_DISTANCE")
meraki_serial_ap = os.getenv("MERAKI_CAMERA_SERIAL_AP")
meraki_device_clients = os.getenv("MERAKI_DEVICE_CLIENTS")

WEBEX_BASE_URL = "https://webexapis.com/v1"
MERAKI_BASE_URL = "https://api.meraki.com/api/v0"
BEEP_BASE_URl = "https://api.beep.nl/api"

# If any of the bot environment variables are missing, terminate the app
if not bot_email or not teams_token or not bot_url or not bot_app_name:
    print(
        "bot.py - Missing Environment Variable. Please see the 'Usage'"
        " section in the README."
    )
    if not bot_email:
        print("TEAMS_BOT_EMAIL")
    if not teams_token:
        print("TEAMS_BOT_TOKEN")
    if not bot_url:
        print("TEAMS_BOT_URL")
    if not bot_app_name:
        print("TEAMS_BOT_APP_NAME")
    sys.exit()

# Create a Bot Object
#   Note: debug mode prints out more details about processing to terminal
#   Note: the `approved_users=approved_users` line commented out and shown as reference
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=False,
    # approved_users=approved_users,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},
    ],
)

# Create a custom bot greeting function returned when no command is given.
# The default behavior of the bot is to return the '/help' command response
def greeting(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, I'm the Connected Bees bot. I am a busy bee that can collect data and info for you. ".format(sender.firstName)
    response.markdown += "See what I can do by asking for **/help**."
    return response


# Function to send a message with a card attachment
def create_message_with_attachment(rid, msgtxt, attachment, toPersonEmail=""):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = f"{WEBEX_BASE_URL}/messages"
    if toPersonEmail == "":
        data = {"roomId": rid, "attachments": [attachment], "markdown": msgtxt}
    else:
        data = {"toPersonEmail": toPersonEmail, "attachments": [attachment], "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def handle_meraki_webhook():
    try:
        # Get the Clients that are connected to the AP
        session = requests.Session()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Cisco-Meraki-API-Key": meraki_api_key
        }
        # Note: timespan indicates the last x seconds you would like to search for
        clients_response = session.get(
            f'{MERAKI_BASE_URL}/devices/{meraki_serial_ap}/clients?timespan=300', 
            headers=headers
        )
        clients_response.raise_for_status()
        clients = clients_response.json()

        # Match the detected clients with the known clients
        detected_clients = []
        for client in clients:
            if not client["description"]:
                continue
            if client["description"] in meraki_device_clients:
                detected_clients.append(client["description"])

        attachment = {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": get_open_door_alert_card(detected_clients)
            }
        print("Successfully created attachment")

        c = create_message_with_attachment(room_id, "hello, the Meraki webhook has been triggered", attachment)
        return ""
    except:
        print("something went wrong!")
        return ""

def get_weight(incoming_msg):
    """
    A function to retrieve the latest weight of the bee hive
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)
    room_id = incoming_msg.roomId

    url = f"{BEEP_BASE_URl}/sensors/lastvalues?id={beehive_id}"

    headers = {
        'Authorization': f'Bearer {beep_api_token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))
    weight = round(response.json()['weight_kg'], 3)

    adaptive_card = get_measurement_card("Weight", "weight", weight, "kilograms")
    attachment = {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": adaptive_card
            }

    c = create_message_with_attachment(room_id, f"Hello {sender.firstName}, the latest weight of the bee hive is {weight} kilograms", attachment)
    return ""

def get_temperature_outside(incoming_msg):
    """
    A function to retrieve the latest temperature around the bee hive
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)
    room_id = incoming_msg.roomId

    url = f"{BEEP_BASE_URl}/sensors/lastvalues?id={beehive_id}"

    headers = {
        'Authorization': f'Bearer {beep_api_token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))
    temperature = response.json()['t']

    adaptive_card = get_measurement_card("Temperature around beehive", "temperature around the beehive", temperature, "degrees celsius")
    attachment = {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": adaptive_card
            }

    c = create_message_with_attachment(room_id, f"Hello {sender.firstName}, the latest weight of the bee hive is {temperature} degrees celsius", attachment)
    return ""

def get_temperature_inside(incoming_msg):
    """
    A function to retrieve the latest temperature inside the bee hive
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)
    room_id = incoming_msg.roomId

    url = f"{BEEP_BASE_URl}/sensors/lastvalues?id={beehive_id}"

    headers = {
        'Authorization': f'Bearer {beep_api_token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    temperature = response.json()['t_i']

    adaptive_card = get_measurement_card("Temperature inside beehive", "temperature inside the beehive", temperature, "degrees celsius")
    attachment = {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": adaptive_card
            }

    c = create_message_with_attachment(room_id, f"Hello {sender.firstName}, the latest weight of the bee hive is {temperature} degrees celsius", attachment)
    return ""

def get_humidity(incoming_msg):
    """
    A function to retrieve the latest temperature inside the bee hive
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)
    room_id = incoming_msg.roomId

    url = f"{BEEP_BASE_URl}/sensors/lastvalues?id={beehive_id}"

    headers = {
        'Authorization': f'Bearer {beep_api_token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    relative_humidity = response.json()['h']

    adaptive_card = get_measurement_card("Humidity", "relative humidity around the beehive", relative_humidity, "%RH")
    attachment = {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": adaptive_card
            }

    c = create_message_with_attachment(room_id, f"Hello {sender.firstName}, the latest measurement of the relative humidity is {relative_humidity} %RH", attachment)
    return ""

def get_snapshot_base(incoming_msg, serial_number, msg="Snapshot of the beehive"): 
    # Loopkup details about sender
    room_id = incoming_msg.roomId

    session = requests.Session()

    # Format message
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': f'Bearer {teams_token}'
    }
    payload = {
        'roomId': room_id,
    }

    # Generating screenshot for latest time since when I selected a timestamp that was too close
    # to real time the camera had not had a chance to store it and make it available for sending
    print("About to generate snapshot with serial ",serial_number)
    theScreenShotURL=generate_snapshot(serial_number, None, session)
    print("theScreenShotURL=",theScreenShotURL)
    file_url=theScreenShotURL

    if file_url:  # download/GET image from URL
        temp_file = download_file(session, merak_serial_front, file_url)
        if temp_file:
              send_file(session, headers, payload, msg, temp_file, file_type='image/jpg')
              return ""
        else:
            return 'snapshot unsuccessfully retrieved'


def get_snapshot_front(incoming_msg):
    """
    A function to generate a snapshot of the camera facing the front of the bee hive
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    return get_snapshot_base(incoming_msg, merak_serial_front, "Snapshot of the front of the beehive")

def get_snapshot_side(incoming_msg):
    """
    A function to generate a snapshot of the camera facing the side of the bee hive
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    return get_snapshot_base(incoming_msg, meraki_serial_side, "Snapshot of the side of the beehive")

def get_snapshot_distance(incoming_msg):
    """
    A function to generate a snapshot of the camera facing the side of the bee hive
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    return get_snapshot_base(incoming_msg, meraki_serial_distance, "Snapshot of beehive in the distance")

def handle_cards(api, incoming_msg):
    m = get_attachment_actions(incoming_msg["data"]["id"])
    print(json.dumps(incoming_msg, indent=2))
    sender = bot.teams.people.get(incoming_msg["data"]["personId"])
    name = sender.firstName

    print(m)
    if "confirm_remote_observation" in m["inputs"]:
        #delete previous message
        api.messages.delete(messageId=m["messageId"]) 

        attachment = {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": get_confirm_viewing_card(name)
            }
        c = create_message_with_attachment(room_id, "Remote observance has been confirmed", attachment)
        return ""
    elif "refuse_remote_observation" in m["inputs"]:
        #delete previous message
        api.messages.delete(messageId=m["messageId"]) 

        attachment = {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": get_refuse_viewing_card(name)
            }
        c = create_message_with_attachment(room_id, "Remote observance has been refused", attachment)
        return ""
    elif "end_remote_observation" in m["inputs"]:
        #delete previous message
        api.messages.delete(messageId=m["messageId"]) 
        attachment = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": observance_ended_card
            }
        c = create_message_with_attachment(room_id, "Remote observance has ended", attachment)
        return ""

    return "Could not find the right action"



def get_attachment_actions(attachmentid):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "{WEBEX_BASE_URl}/attachment/actions/" + attachmentid
    response = requests.get(url, headers=headers)
    return response.json()


bot.add_new_url("/meraki_webhook", "meraki_webhook", handle_meraki_webhook)

# Set the bot greeting.
bot.set_greeting(greeting)

# Add new commands to the bot.
bot.add_command("attachmentActions", "*", handle_cards)
bot.add_command("/weight", "Get the latest weight of the bee hive", get_weight)
bot.add_command("/temp_outside", "Get the latest temperature around the bee hive", get_temperature_outside)
bot.add_command("/temp_inside", "Get the latest temperature inside the bee hive", get_temperature_inside)
bot.add_command("/humidity", "Get the latest humidity around the bee hive", get_humidity)
bot.add_command("/snapshot_front", "Get the latest snapshot of the front of the bee hive", get_snapshot_front)
bot.add_command("/snapshot_side", "Get the latest snapshot of the side of the bee hive", get_snapshot_side)
bot.add_command("/snapshot_distance", "Get the latest snapshot of the bee hive in the distance", get_snapshot_distance)

# Every bot includes a default "/echo" command.  You can remove it, or any
# other command with the remove_command(command) method.
bot.remove_command("/echo")


if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5001)