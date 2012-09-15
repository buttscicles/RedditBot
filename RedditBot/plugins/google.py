from RedditBot import bot, utils

import HTMLParser

h = HTMLParser.HTMLParser()

# the Google search API URL
search_url = 'http://ajax.googleapis.com/ajax/services/search/web'

@bot.command('g')  # also bind this function to '.g'
@bot.command  # register the wrapped function as a plugin
def google(context):
    global h
    # notice that we provide one arg, context: this is optional but if you
    # want access to the IRC line that triggered the plugin you need to
    # pass in some variable; we'll use context for this

    query = context.args  # args are parsed automatically by IrcTK

    # make the request, should give us back some JSON
    r = utils.make_request(search_url, params=dict(v='1.0', safe='off', q=query))

    # if we don't have results, bail out of the plugin
    if not r.json['responseData']['results']:
        return 'no results found'

    # otherwise grab the first result
    first_result = r.json['responseData']['results'][0]

    title = h.unescape(first_result['titleNoFormatting'])

    # build our return string
    ret = title + ' - ' \
            + first_result['unescapedUrl']

    # finally return the result to the channel or user the plugin was called
    # from
    return ret
