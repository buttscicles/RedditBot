
from RedditBot import bot, utils


@bot.command('mcb')
def mcbouncer(context):
    '''Usage: .mcb'''
    if not bot.config["MCBOUNCERKEY"]:
        return "MCBouncer not configured"
    url = "http://mcbouncer.com/api/getBanCount/%s/AlcoJew" % bot.config["MCBOUNCERKEY"]
    r = utils.make_request(url)
    if r:
        if type(r) is str:
            return r
        if r.status_code == 200:
                if r.json:
                    return "MCBouncer API operational"
                else:
                    return "MCBouncer Error - malformed data"
        else:
            return "MCBouncer Error - server error"
    else:
        return "MCBouncer Error - no data returned"
    
