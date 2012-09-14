
from RedditBot import bot, utils

from itertools import groupby

@bot.command('.')
@bot.command('help')
@bot.command
def usage(context):
    '''.usage <plugin>'''
    plugin = context.args
    if plugin:
        for p in bot.config['PLUGINS']:
            if plugin == p['hook']:
                return p['funcs'][0].__doc__
    else:
        p = [(p['hook'], p['funcs']) for p in bot.config['PLUGINS']]
        p.sort(key=lambda t: t[1])
        result = []
        # group by function
        for k, v in groupby(p, key=lambda t: t[1]):
            grouped = [v[0] for v in v]
            grouped[0] = '\x02' + grouped[0] + '\x02'
            if len(grouped) > 1:
                # shortcuts/secondary
                for i, hook in enumerate(grouped[1:]):
                    grouped[i+1] = '[' + grouped[i+1] + ']'
            result.append(' '.join(grouped))
        result.sort()
        p = ', '.join(result)
        return 'Plugins currently loaded: ' + p

@bot.command
def raw(context):
    '''.raw <command>'''
    #if not context.line['prefix'] in bot.config.get('ADMINS', []):
    #    return
    if not utils.isadmin(context.line['prefix']):
        return
    if context.args:
        command = context.args.split(' ', 1)[0]
        args = list(context.args.split(' ', 1)[-1])
        bot.irc.send_command(command, args)
    else:
        return raw.__doc__
