import re
import yaml
from collections import namedtuple

#get slack token from yaml file
with open('token.yaml', 'r') as stream:
    token = yaml.load(stream)['token']

from slackclient import SlackClient

#slack stuff
sc = SlackClient(token)

#bot stuff
text = namedtuple('phrase', 'original response')
phrases = (
    text(original=re.compile("(what is|what's) my purpose", flags=re.IGNORECASE), response="You pass butter."),
)

#connect to slack and do stuff
if sc.rtm_connect():
    while True:
        event = sc.rtm_read()
        for item in event:
            message = item.get('text', None)

            if message:
                for phrase in phrases:
                    if phrase.original.search(message):
                        print phrase.response
