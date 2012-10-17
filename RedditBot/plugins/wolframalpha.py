
from RedditBot import bot, utils

import xml.etree.ElementTree as ET

import re
import random

### begin insult code, shamelessly stolen from rbot

adj = [
"acidic",
"antique",
"contemptible",
"culturally-unsound",
"despicable",
"evil",
"fermented",
"festering",
"foul",
"fulminating",
"humid",
"impure",
"inept",
"inferior",
"industrial",
"left-over",
"low-quality",
"malodorous",
"off-color",
"penguin-molesting",
"petrified",
"pointy-nosed",
"salty",
"sausage-snorfling",
"tastless",
"tempestuous",
"tepid",
"tofu-nibbling",
"unintelligent",
"unoriginal",
"uninspiring",
"weasel-smelling",
"wretched",
"spam-sucking",
"egg-sucking",
"decayed",
"halfbaked",
"infected",
"squishy",
"porous",
"pickled",
"coughed-up",
"thick",
"vapid",
"hacked-up",
"unmuzzled",
"bawdy",
"vain",
"lumpish",
"churlish",
"fobbing",
"rank",
"craven",
"puking",
"jarring",
"fly-bitten",
"pox-marked",
"fen-sucked",
"spongy",
"droning",
"gleeking",
"warped",
"currish",
"milk-livered",
"surly",
"mammering",
"ill-borne",
"beef-witted",
"tickle-brained",
"half-faced",
"headless",
"wayward",
"rump-fed",
"onion-eyed",
"beslubbering",
"villainous",
"lewd-minded",
"cockered",
"full-gorged",
"rude-snouted",
"crook-pated",
"pribbling",
"dread-bolted",
"fool-born",
"puny",
"fawning",
"sheep-biting",
"dankish",
"goatish",
"weather-bitten",
"knotty-pated",
"malt-wormy",
"saucyspleened",
"motley-mind",
"it-fowling",
"vassal-willed",
"loggerheaded",
"clapper-clawed",
"frothy",
"ruttish",
"clouted",
"common-kissing",
"pignutted",
"folly-fallen",
"plume-plucked",
"flap-mouthed",
"swag-bellied",
"dizzy-eyed",
"gorbellied",
"weedy",
"reeky",
"measled",
"spur-galled",
"mangled",
"impertinent",
"bootless",
"toad-spotted",
"hasty-witted",
"horn-beat",
"yeasty",
"boil-brained",
"tottering",
"hedge-born",
"hugger-muggered",
"elf-skinned"
]

amt = [
"accumulation",
"bucket",
"coagulation",
"enema-bucketful",
"gob",
"half-mouthful",
"heap",
"mass",
"mound",
"petrification",
"pile",
"puddle",
"stack",
"thimbleful",
"tongueful",
"ooze",
"quart",
"bag",
"plate",
"ass-full",
"assload"
]

noun = [
"bat toenails",
"bug spit",
"cat hair",
"chicken piss",
"dog vomit",
"dung",
"fat-woman's stomach-bile",
"fish heads",
"guano",
"gunk",
"pond scum",
"rat retch",
"red dye number-9",
"Sun IPC manuals",
"waffle-house grits",
"yoo-hoo",
"dog balls",
"seagull puke",
"cat bladders",
"pus",
"urine samples",
"squirrel guts",
"snake assholes",
"snake bait",
"buzzard gizzards",
"cat-hair-balls",
"rat-farts",
"pods",
"armadillo snouts",
"entrails",
"snake snot",
"eel ooze",
"slurpee-backwash",
"toxic waste",
"Stimpy-drool",
"poopy",
"poop",
"craptacular carpet droppings",
"jizzum",
"cold sores",
"anal warts"
]

def generate_insult():
    adj1 = random.choice(adj)
    adj2 = adj1
    while adj2 == adj1:
        adj2 = random.choice(adj)
    
    amt1 = random.choice(amt)
    noun1= random.choice(noun)
    return "%s %s of %s %s" % (adj1, amt1, adj2, noun1)
    

url = 'http://www39.wolframalpha.com/input/'

letters_re = re.compile(r'^(?:\w \| )+\w$')


@bot.command('wa')
@bot.command('wolframalpha')
def wa_api(context):
    if not bot.config['WOLFRAMALPHA_KEY']:
        return 'WolframAlpha support not configured.'
    url = 'http://api.wolframalpha.com/v2/query'
    params = {'format': 'plaintext', 'appid': bot.config['WOLFRAMALPHA_KEY'], 'input': context.args}
    result = utils.make_request(url, params=params, timeout=10)
    if type(result) is str:
        return result
    xml = ET.fromstring(result.text.encode('utf8'))
    success = xml.get('success') == 'true'
    if success:
        pods = xml.findall('.//pod[@primary=\'true\']/subpod/plaintext')

        if len(pods) < 1:
            return 'No primary node returned.'

        results = pods[-1].text.split('\n')

        def format_result_nicely(result):
            if letters_re.match(result):
                return result.replace(' | ', '')
            return result

        results = [format_result_nicely(r) for r in results]
        return ', '.join(results)
    else:
        return 'Failed, you %s.' % generate_insult()
