import os
import re
import yaml
import time
import random

from collections import namedtuple

#bot stuff
text = namedtuple('phrase', 'original response')

def do_regex(regex):
	return re.compile(regex, flags=re.IGNORECASE)

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

GAZORPAZORP = (
	"You dumb, stupid, weak, pathetic, white...uh...guilt...white guilt, milquetoast...",
	"Give me my enchiladas",
	"You're pretty mean to me Gazorpazorpfield, but that takes the cake",
)

ANTS_IN_MY_EYES = (
	"I'm ants in my eyes Johnson, here at ants in my eyes Johnson's electronics.",
	"I mean, there are so many ants in my eyes!",
	"There are so many TVs, Microwaves, Radios...I think...I'm not a hundred percent sure what we have in stock, because there are so many ants in my eyes!",
	"I can't see anything! Our prices, I hope aren't too low!",
	"Also I can't feel anything either, but that's not as catchy.",
)

FAKE_DOORS = (
	"Check this out! Mm, won't open, Mm, won't open",
	"Not this one, not this one. None of em open!",
	"www.fakedoors.com is our website. Check it out for a lot of really great deals on FAKE DOOORRRRSSSS!",
	"Hey everybody, so this is my house, just made a sandwich. Still here, still sellin' fake doors.",
	"We have fake doors, like you wouldn't believe. Don't even hesitate, don't even worry, don't even give it a second thought.",
)

TWO_BROTHERS = (
	"And then a meteor hits. And they ran as fast as they could, from giant cat monsters",
	"Then a giant tornado came, and that's when things got knocked into twelvth gear!",
	"A Mexican armada shows up. With weapons made from to..tomatoes.",
	"You better bet your bottom dollar that these two brothers know how to handle business.",
	"ALIEN INVASION TOMATO MONSTER MEXICAN ARMADA BROTHERS (WHO ARE JUST REGULAR BROTHERS) RUNNING IN A VAN FROM AN ASTEROID AND ALL SORTS OF THINGS THE MOVIE",
	"Old women are comin', and they're also in the movie, and they're gonna come and cross...attack...the two brothers",
	"They have a strong bond, but you don't wanna know about it here. But I'll tell you one thing...the moon, it comes crashing into earth. What do ya do then.",
)

BABY_LEGS = (
	"This is upsetting to me because I don't feel like I need no regular leg partner.",
	"Baby legs, don't talk back to me. Good luck you two, there's a criminal to kill.",
	"I'm comin' baby legs...I'm..regular..legs!",
)

VINCENT = (
	"Calling all Jan Michael Vincents. Calling all Jan Michael Vincents.",
	"We need one Jan Michael Vincent to quadrant C. We need two Jan Michael Vincents to quadrant E.",
	"In a world where there's eight jan Michael Vincents...and 16 quadrants, there's only enough time for a jan Michael Vincent to make it to a quadrant.",
	"He can't be in two quadrants at once.",
	"I need a goddamn Jan Michael Vincent!",
	"I-I refuse to send the legislation that allows more than eight jan Michael Vincents to a precinct.",
	"This jan-uary, it's time to Michael down your Vincents. Jan quadrant Vincent 16.",
)

MEESEEKS = (
	"I'm Mr. Meeseeks, look at me!",
	"Caaaannnnn dooooooo.",
	"Is he keeping his shoulders square? Ohhhhh he's tryyiingg.",
	"I have to fulfill my purpose, so I can go away!",
)

phrases = (
	text(original=do_regex("(what is|whats) my purpose"), response="You pass butter."),
	text(original=do_regex("schwifty"), response="Ohh yea, you gotta get schwifty in here."),
	text(original=do_regex("think (youre|you are|your) better than me"), response="Keep Summer safe."),
	text(original=do_regex("whats going on"), response="I have brokered a peace agreement between the giant spiders and the government."),
	text(original=do_regex("(ride|take) the stairs"), response="I can take you down there for 25 Schmeck-les"),
	text(original=do_regex("I dont (wanna|want to) shoot (nobody|anybody|noone|anyone)"), response="It's ok, they're just robots Morty, it's ok to shoot them, they're robots!"),
	text(original=do_regex("robots"), response="It's a figure of speech Morty, they're bureaucrats, I don't respect them. Just keep shooting Morty."),
	text(original=do_regex("human music"), response="Human music...I like it."),
	text(original=do_regex("(like to|can I) order"), response="I'd like to order one large phone with extra phones please. cell phone, no no no rotary... and payphone on half."),
	text(original=do_regex("new machine"), response="It's a new machine. It detects stuff all the way up your butt."),
	text(original=do_regex("monday"), response=GAZORPAZORP),
	text(original=do_regex("(near me|around me|personal space|too close)"), response=PERSONAL_SPACE),
	text(original=do_regex("(cant see|blind|in my eyes)"), response=ANTS_IN_MY_EYES),
	text(original=do_regex("(real|fake) doors?"), response=FAKE_DOORS),
	text(original=do_regex("(two brothers|in a van|mexican armada|cat monsters|twel.?th gear)"), response=TWO_BROTHERS),
	text(original=do_regex("(baby|regular|small|short|weird) legs"), response=BABY_LEGS),
	text(original=do_regex("((jan|michael|mikel|michal|michel|mikal) vincent|quadrant)"), response=VINCENT),
	text(original=do_regex("(meseeks|meeseeks|look at me)"), response=MEESEEKS),
)

def decide_on_response(message):
	"""
	pass in the slack event and get back a response that can then be posted
	"""
	for phrase in phrases:
		if phrase.original.search(message.replace('"', '').replace("'", '')):
			if isinstance(phrase.response, tuple):
				return (random.choice(phrase.response))
			else:
				return phrase.response

#connect to slack and do stuff
if __name__ == "__main__":
	from slackclient import SlackClient

	#get slack token from yaml file
	current_path = os.path.dirname(os.path.realpath(__file__))

	with open(current_path + '/token.yaml') as stream:
		token = yaml.load(stream)['token']

	#slack stuff
	sc = SlackClient(token)

	if sc.rtm_connect():
		while True:
			event = sc.rtm_read()

			for item in event:

				if item.get('type') == 'message' and item.get('user') != 'rick_and_morty_bot':
					message = item.get('text', '')
					channel = item.get('channel', '')

					response = decide_on_response(message)
					sc.rtm_send_message(channel, response)

			time.sleep(1)
