
from RedditBot import bot, utils

from RedditBot.plugins.mcbouncer import mcb_status

#from itertools import imap

import socket
import re

from requests import codes

statuses = {'green': 'Up!', 'red': 'Down'}
account  = {'true': '{} is a premium Minecaft account',
            'false': '{} is \x02not\x02 a premium Minecraft account'}

isup_re = re.compile(r'is (\w+) (?:up|down)', re.I)
server_re = re.compile(r'^\s*([A-Za-z0-9_-]+\.[A-Za-z0-9_.-]+)(?::([0-9]{1,5}))?\s*$')

nerd_nu = [
 ('c.nerd.nu', 25565, ['creative', 'c']),
 ('p.nerd.nu', 25565, ['pve', 'p']),
 ('s.nerd.nu', 25565, ['survival', 's'])
]


def get_info(host, port):
    try:
        #Set up our socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((host, port))

        #Send 0xFE: Server list ping
        s.send('\xfe')
        #Send a payload of 0x01 to trigger a new response if the server supports it
        s.send('\x01')

        #Read as much data as we can (max packet size: 241 bytes)
        d = s.recv(256)
        s.close()

        #Check we've got a 0xFF Disconnect
        assert d[0] == '\xff'

        #Remove the packet ident (0xFF) and the short containing the length of the string
        #Decode UCS-2 string
        d = d[3:].decode('utf-16be')
        
        #If the response string starts with simolean1, then we're dealing with the new response
        if (d.startswith(u'\xa7' + '1')):
            d = d.split(u'\x00')
            #Return a dict of values
            return {'protocol_version': int(d[1]),
                    'minecraft_version':    d[2],
                    'motd':                 d[3],
                    'players':          int(d[4]),
                    'max_players':      int(d[5])}
        else:
            d = d.split(u'\xa7')
            #Return a dict of values
            return {'motd':         d[0],
                    'players':   int(d[1]),
                    'max_players': int(d[2])}
                    
    except Exception, e:
        print e
        return False


def find_server(name):
    name = name.lower()
    for server in nerd_nu:
        if name == server[0] or name in server[2]:
            return server
    return None


def silly_label(server):
    n = 'PLAYERS_{}'.format(server[0])
    return bot.config.get(n, 'players')


def manual_login():
    params = {'user': bot.config['MINECRAFT_USER'],
              'password': bot.config['MINECRAFT_PASSWORD'],
              'version': 9001}

    r = utils.make_request('https://login.minecraft.net', params=params, method='POST')
    if isinstance(r, str):
        return 'Down ({})'.format(r)
    else:
        if r.status_code == codes.ok:
            return 'Up!'
        else:
            return 'Down ({})'.format(r.status_code)


def manual_session():
    params = {'user': bot.config['MINECRAFT_USER'],
              'sessionId': 'invalid',
              'serverId': 'invalid'}

    r = utils.make_request('http://session.minecraft.net/game/joinserver.jsp', params=params)
    if isinstance(r, str):
        return 'Down ({})'.format(r)
    else:
        if r.status_code == codes.ok:
            return 'Up!'
        else:
            return 'Down ({})'.format(r.status_code)


@bot.command('login')
@bot.command('session')
def minecraft_status(context):
    '''Usage: .session'''
    r = utils.make_request('http://status.mojang.com/check')
    response = {}
    try:
        for i in r.json:
            for k, v in i.iteritems():
                response[k.split('.')[0]] = statuses[v]
    except:
        response['session'] = manual_session()
        response['login'] = manual_login()

    line = '[Login] {login} [Session] {session}'.format(**response)
    return line


@bot.command
def status(context):
    '''Usage: .status'''
    def server_info(host, port):
        info = get_info(host, port)
        if not info:
            return '{} seems to be down'.format(host)
        return '{motd}: [{players}/{max_players}]'.format(**info)
    def mcb_info():
        up = mcb_status()['success']
        return 'MCBouncer: {}'.format('Up!' if up else 'Down')
    servers = [server_info(s[0], s[1]) for s in nerd_nu]
    if bot.config.get('MCBOUNCER_KEY', False):
        servers.append(mcb_info())
    return ' | '.join(servers)


@bot.regex(isup_re)
def is_x_up(context):
    server = find_server(context.line['regex_search'].group(1))
    if not server:
        return
    info = get_info(server[0], server[1])
    if info:
        return '{0} is online with {players}/{max_players} {1} online.'.format(server[0], silly_label(server), **info)
    else:
        return '{0} seems to be down :(.'.format(server[0])


@bot.command
def isup(context):
    '''Usage: .isup <MC server address>'''
    server = find_server(context.args)
    if not server:
        match = server_re.match(context.args)
        if not match:
            return
        server = (match.group(1), match.group(2) or 25565, 'players')
    info = get_info(server[0], server[1])
    if info:
        return '{0} is online with {players}/{max_players} {1} online.'.format(server[0], silly_label(server), **info)
    else:
        return '{0} seems to be down :(.'.format(server[0])


@bot.command('mcaccount')
@bot.command('mcpremium')
def premium(context):
    '''Usage: .mcaccount <username>'''
    arg = context.args.split(' ')[0]
    if len(arg) < 1:
        return premium.__doc__
    params = {'user': arg}
    r = utils.make_request('http://minecraft.net/haspaid.jsp', params=params)

    try:
        return account.get(r.text, 'Unexpected Response').format(arg)
    except AttributeError:
        return r
