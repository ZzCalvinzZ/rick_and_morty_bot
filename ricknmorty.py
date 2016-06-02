import re
from collections import namedtuple

text = namedtuple('phrase', 'original response')
phrases = (
    text(original=re.compile("(what is|what's) my purpose", flags=re.IGNORECASE), response="You pass butter."),
)

message = 'test, what is my purpose'

for phrase in phrases:
    if phrase.original.search(message):
        print phrase.response
