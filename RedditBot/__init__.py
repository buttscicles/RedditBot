import sys
sys.path.insert(1, sys.path[0] + "/irctk")

#from irctk import Bot
from RedditBot.redditbot import Bot

from RedditBot.config import Config

from copy import deepcopy

# initialize the bot object
bot = Bot()

# configure the bot object based on a Python class
bot.config.from_object(Config)

if not bot.h_config:
    bot.h_config = deepcopy(bot.config)

# load our plugins
from RedditBot.plugins import reddit, twitter, botutils, youtube, badword, tell, minecraft, google, lastfm, silly, config, kickrejoin, grab, wolframalpha, mcbouncer
