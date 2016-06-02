import os
import re
import yaml
import time

from collections import namedtuple

#get slack token from yaml file
current_path = os.path.dirname(os.path.realpath(__file__))

with open(current_path + '/token.yaml', 'r') as stream:
    token = yaml.load(stream)['token']

from slackclient import SlackClient

#slack stuff
sc = SlackClient(token)

#bot stuff
text = namedtuple('phrase', 'original response')
phrases = (
    text(original=re.compile("(what is|what's) my purpose", flags=re.IGNORECASE), response="You pass butter."),
    text(original=re.compile("schwifty", flags=re.IGNORECASE), response="Ohh yea, you gotta get schwifty in here."),
    text(original=re.compile("think (you're|you are|your) better than me", flags=re.IGNORECASE), response="Keep Summer safe."),
    text(original=re.compile("what'?s going on", flags=re.IGNORECASE), response="I have brokered a peace agreement between the giant spiders and the government."),
    text(original=re.compile("(ride|take) the stairs", flags=re.IGNORECASE), response="I can take you down there for 25 Schmeck-les"),
    text(original=re.compile("I don'?t (wanna|want to) shoot (nobody|anybody|noone|anyone)", flags=re.IGNORECASE), response="It's ok, they're just robots Morty, it's ok to shoot them, they're robots!"),
    text(original=re.compile("(they're|there|their) not robots", flags=re.IGNORECASE), response="It's a figure of speech Morty, they're bureaucrats, I don't respect them. Just keep shooting Morty."),
    text(original=re.compile("human music", flags=re.IGNORECASE), response="Human music...I like it."),
    text(original=re.compile("(like to|can I) order", flags=re.IGNORECASE), response="I'd like to order one large phone with extra phones please. cell phone, no no no rotary... and payphone on half."),
)

#connect to slack and do stuff
if sc.rtm_connect():
    while True:
        event = sc.rtm_read()

        for item in event:
            if item.get('type', None) == 'message' and item.get('user', None) != 'rick_and_morty_bot':
                message = item.get('text', '')
                channel = item.get('channel', '')

                for phrase in phrases:
                    if phrase.original.search(message):
                        sc.rtm_send_message(channel, phrase.response)

        time.sleep(1)
