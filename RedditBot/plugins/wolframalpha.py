from RedditBot import bot, utils
import urllib

uri = 'http://tumbolia.appspot.com/wa/'

@bot.command
def wa(context):
    '''.wa <query>'''
    query = context.args
    answer = utils.make_request(uri + urllib.quote(query.replace('+', '%2B')), timeout=10)
    if answer: 
       return u'{0}: {1}'.format(context.line['user'], utils.unescape_html(answer.text)[:300])
    else: return 'Sorry, no result.'

