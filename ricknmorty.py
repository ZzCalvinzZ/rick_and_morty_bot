import os
import re
import yaml
import time
import random

from collections import namedtuple

#bot stuff
text = namedtuple('phrase', 'original response')

PERSONAL_SPACE = (
        "We got a one, personal space",
        "Two, personal space",
        "Three, stay out of my personal space!",
        "Four, keep away from my personal space!!",
        "Five, get outta that personal space!",
        "Six, stay away from my personal space!",
        "Seven, keep away from dat personal space!!",
        "Eight, personal space.",
        "Nine, PERSONAL SPACE",
        "You know, I take personal space pretty seriously, up to the point that I'm not even interested in having this...skin on my personal space.",
)

phrases = (
    text(original=re.compile("(what is|what's) my purpose", flags=re.IGNORECASE), response="You pass butter."),
    text(original=re.compile("schwifty", flags=re.IGNORECASE), response="Ohh yea, you gotta get schwifty in here."),
    text(original=re.compile("think (you're|you are|your) better than me", flags=re.IGNORECASE), response="Keep Summer safe."),
    text(original=re.compile("what'?s going on", flags=re.IGNORECASE), response="I have brokered a peace agreement between the giant spiders and the government."),
    text(original=re.compile("(ride|take) the stairs", flags=re.IGNORECASE), response="I can take you down there for 25 Schmeck-les"),
    text(original=re.compile("I don'?t (wanna|want to) shoot (nobody|anybody|noone|anyone)", flags=re.IGNORECASE), response="It's ok, they're just robots Morty, it's ok to shoot them, they're robots!"),
    text(original=re.compile("robots", flags=re.IGNORECASE), response="It's a figure of speech Morty, they're bureaucrats, I don't respect them. Just keep shooting Morty."),
    text(original=re.compile("human music", flags=re.IGNORECASE), response="Human music...I like it."),
    text(original=re.compile("(like to|can I) order", flags=re.IGNORECASE), response="I'd like to order one large phone with extra phones please. cell phone, no no no rotary... and payphone on half."),
    text(original=re.compile("(near me|around me|personal space|too close)", flags=re.IGNORECASE), response=PERSONAL_SPACE),
)

def decide_on_response(message):
    """
    pass in the slack event and get back a response that can then be posted
    """
    for phrase in phrases:
        if phrase.original.search(message):
            if isinstance(response, tuple):
                return (random.choice(response))
            else:
                return response

#connect to slack and do stuff
if __name__ == "__main__":
    from slackclient import SlackClient

    #get slack token from yaml file
    current_path = os.path.dirname(os.path.realpath(__file__))

    with open(current_path + '/token.yaml', 'r') as stream:
        token = yaml.load(stream)['token']

    #slack stuff
    sc = SlackClient(token)

    if sc.rtm_connect():
        while True:
            event = sc.rtm_read()

            for item in event:

                if item.get('type', None) == 'message' and item.get('user', None) != 'rick_and_morty_bot':
                    message = item.get('text', '')
                    channel = item.get('channel', '')

                    response = decide_on_response(message)
                    sc.rtm_send_message(channel, response)

            time.sleep(1)
