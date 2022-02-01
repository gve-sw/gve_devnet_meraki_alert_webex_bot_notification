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

adaptive_card = {
    "type": "AdaptiveCard",
    "body": [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "items": [
                        {
                            "type": "Image",
                            "style": "Person",
                            "url": "https://i.pinimg.com/736x/76/69/c1/7669c1af96274747061b62a75cfda8fb.jpg",
                            "size": "Medium",
                            "height": "50px"
                        }
                    ],
                    "width": "auto"
                },
                {
                    "type": "Column",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Connected Bees",
                            "weight": "Lighter",
                            "color": "Accent"
                        },
                        {
                            "type": "TextBlock",
                            "weight": "Bolder",
                            "text": "Open Door Alert",
                            "wrap": True,
                            "color": "Light",
                            "size": "Large",
                            "spacing": "Small"
                        }
                    ],
                    "width": "stretch"
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": "The Meraki MT door sensor has been activated and a member of your team is about to enter the roof. Please ensure that another member is with you or a team member is viewing the cameras remotely. ",
            "wrap": True
        },
        {
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.OpenUrl",
                    "title": "View Bee Camera",
                    "url": "https://n40.meraki.com/Voorburgwal/n/uEpPsbO/manage/video/video_wall/585467951558165369"
                }
            ],
            "spacing": "None"
        }
    ],
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.2"
}

def get_open_door_alert_card(detected_clients):
    text_to_display = ""
    for client in detected_clients:
        text_to_display += f"- {client}\r"

    meraki_webhook_triggered_card = {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "Image",
                                "style": "Person",
                                "url": "https://i.pinimg.com/736x/76/69/c1/7669c1af96274747061b62a75cfda8fb.jpg",
                                "size": "Medium",
                                "height": "50px"
                            }
                        ],
                        "width": "auto"
                    },
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Connected Bees",
                                "weight": "Lighter",
                                "color": "Accent"
                            },
                            {
                                "type": "TextBlock",
                                "weight": "Bolder",
                                "text": "Open Door Alert",
                                "wrap": True,
                                "color": "Light",
                                "size": "Large",
                                "spacing": "Small"
                            }
                        ],
                        "width": "stretch"
                    }
                ]
            },
            {
                "type": "TextBlock",
                "text": "The Meraki MT door sensor has been activated and a member of your team is about to enter the roof. Please ensure that another member is with you or a team member is viewing the cameras remotely. A remote team member can confirm their remote observation. However, in case you don't need remote observance, then you can discard this message.",
                "wrap": True
            },
            {
                "type": "TextBlock",
                "text": f"The following people have been detected:\r{text_to_display}",
                "wrap": True
            },
            {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Confirm Remote Observation",
                        "data": {
                            "confirm_remote_observation": True
                        }
                    },
                    {
                        "type": "Action.Submit",
                        "title": "Observation not needed",
                        "data": {
                            "refuse_remote_observation": True
                        }
                    }
                ],
                "spacing": "None"
            }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2"
    }
    return meraki_webhook_triggered_card

observance_ended_card = {
    "type": "AdaptiveCard",
    "body": [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "items": [
                        {
                            "type": "Image",
                            "style": "Person",
                            "url": "https://i.pinimg.com/736x/76/69/c1/7669c1af96274747061b62a75cfda8fb.jpg",
                            "size": "Medium",
                            "height": "50px"
                        }
                    ],
                    "width": "auto"
                },
                {
                    "type": "Column",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Connected Bees",
                            "weight": "Lighter",
                            "color": "Accent"
                        },
                        {
                            "type": "TextBlock",
                            "weight": "Bolder",
                            "text": "Remote Observance ended",
                            "wrap": True,
                            "color": "Light",
                            "size": "Large",
                            "spacing": "Small"
                        }
                    ],
                    "width": "stretch"
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": "The remote observance session has ended. Hopefully the bees are happy and healthy. Happy beekeeping!",
            "wrap": True
        }
    ],
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.2"
}

def get_refuse_viewing_card(name):
    adaptive_card = {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "Image",
                                "style": "Person",
                                "url": "https://i.pinimg.com/736x/76/69/c1/7669c1af96274747061b62a75cfda8fb.jpg",
                                "size": "Medium",
                                "height": "50px"
                            }
                        ],
                        "width": "auto"
                    },
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Connected Bees",
                                "weight": "Lighter",
                                "color": "Accent"
                            },
                            {
                                "type": "TextBlock",
                                "weight": "Bolder",
                                "text": "No Need for Remote Observance",
                                "wrap": True,
                                "color": "Light",
                                "size": "Large",
                                "spacing": "Small"
                            }
                        ],
                        "width": "stretch"
                    }
                ]
            },
            {
                "type": "TextBlock",
                "text": f"Team member **{name}** has confirmed that there is no need for remote observance. However, remote team mates can still observe through the live stream",
                "wrap": True
            },
            {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.OpenUrl",
                        "title": "View Bee Camera",
                        "url": "https://n40.meraki.com/Voorburgwal/n/uEpPsbO/manage/video/video_wall/585467951558165369"
                    }
                ],
                "spacing": "None"
            }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2"
    }
    return adaptive_card

def get_confirm_viewing_card(name):
    adaptive_card = {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "Image",
                                "style": "Person",
                                "url": "https://i.pinimg.com/736x/76/69/c1/7669c1af96274747061b62a75cfda8fb.jpg",
                                "size": "Medium",
                                "height": "50px"
                            }
                        ],
                        "width": "auto"
                    },
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Connected Bees",
                                "weight": "Lighter",
                                "color": "Accent"
                            },
                            {
                                "type": "TextBlock",
                                "weight": "Bolder",
                                "text": "Confirmation Remote Observance",
                                "wrap": True,
                                "color": "Light",
                                "size": "Large",
                                "spacing": "Small"
                            }
                        ],
                        "width": "stretch"
                    }
                ]
            },
            {
                "type": "TextBlock",
                "text": f"Your remote team member **{name}** has confirmed to remotely observe you, while you are being a busy bee. Please click the button below for the live stream. If you are finished, then please click the button _End remote observance_.",
                "wrap": True
            },
            {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.OpenUrl",
                        "title": "View Bee Camera",
                        "url": "https://vision.meraki.com/n/659777345409850098/cameras/167231135003721"
                    },
                    {
                    "type": "Action.Submit",
                    "title": "End Remote Observation",
                    "data": {
                        "end_remote_observation": True
                    }
                }
                ],
                "spacing": "None"
            }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2"
    }
    return adaptive_card


def get_measurement_card(title, type_of_measurement, measurement_value, unit):
    measurement_card = {
    "type": "AdaptiveCard",
    "body": [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "items": [
                        {
                            "type": "Image",
                            "style": "Person",
                            "url": "https://i.pinimg.com/736x/76/69/c1/7669c1af96274747061b62a75cfda8fb.jpg",
                            "size": "Medium",
                            "height": "50px"
                        }
                    ],
                    "width": "auto"
                },
                {
                    "type": "Column",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Connected Bees",
                            "weight": "Lighter",
                            "color": "Accent"
                        },
                        {
                            "type": "TextBlock",
                            "weight": "Bolder",
                            "text": f"{title}",
                            "wrap": True,
                            "color": "Light",
                            "size": "Large",
                            "spacing": "Small"
                        }
                    ],
                    "width": "stretch"
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": f"The latest measurement of the **{type_of_measurement}** is **{measurement_value} {unit}**",
            "wrap": True
        }
    ],
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.2"
    }
    return measurement_card