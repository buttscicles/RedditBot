import sys
sys.path.insert(1, sys.path[0] + "/irctk")

#from irctk import Bot
from RedditBot.redditbot import Bot

from RedditBot.config import Config

# initialize the bot object
bot = Bot()

# configure the bot object based on a Python class
bot.config.from_object(Config)

# load our plugins
from RedditBot.plugins import reddit, twitter, botutils, youtube, badword, tell, minecraft, google
