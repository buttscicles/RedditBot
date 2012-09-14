
import re

nick_user_host_re = r'^([^!@]+)!([^!@]+)@([^!@]+)$'

def matches(pattern, prefix):
    return glob(pattern).matches(prefix)

class glob(object):
    '''Represents a nick!user@host glob pattern'''
    def __init__(self, pattern):
        (self.nick, self.user, self.host) = self.str_to_tuple(pattern)
    
    def __eq__(self, other):
        return (self.nick, self.user, self.host) == (other.nick, other.user, other.host)
    
    def __repr__(self):
        return str((self.nick, self.user, self.host))
    
    @staticmethod
    def str_to_tuple(nick_user_host):
        '''Convert a "nick!user@host" to (nick, user, host)'''
        return re.match(nick_user_host_re, nick_user_host).groups()
    
    @staticmethod
    def pattern_to_re(pattern):
        '''Convert a glob pattern to a regex'''
        r = ''
        for bit in re.finditer(r'(?:[^\?\*]+|\?+|\*+)', pattern):
            if bit.group().startswith("*"):
                r += '[^!@]*'
            elif bit.group().startswith("?"):
                r += '[^!@]'
                if len(bit.group()) > 1:
                    r += '{%d}' % len(bit.group())
            else:
                r += re.escape(bit.group())
        return r
    
    @staticmethod
    def matches_piece(pattern, thing):
        '''Return True if thing matches pattern'''
        return re.match(glob.pattern_to_re(pattern), thing) != None
    
    def matches(self, test):
        '''Return True if 'test' is matched by the pattern we represent'''
        nick, user, host = self.str_to_tuple(test)
        return self.matches_piece(self.nick, nick) and self.matches_piece(self.user, user) and self.matches_piece(self.host, host)
    
    @staticmethod
    def pattern_to_super_re(pattern):
        '''Like glob.pattern_to_re but for superset testing'''
        r = ''
        for bit in re.finditer(r'(?:[^\?\*]+|\?+|\*+)', pattern):
            if bit.group().startswith("*"):
                r += '[^!@]*'
            elif bit.group().startswith("?"):
                r += '[^!@*]'
                if len(bit.group()) > 1:
                    r += '{%d}' % len(bit.group())
            else:
                r += re.escape(bit.group())
        return r
    
    @staticmethod
    def issuper_piece(a, b):
        '''Like glob.matches_piece but for superset testing'''
        return re.match(glob.pattern_to_super_re(a), b) != None
    
    def issuper(self, other):
        '''Return True if the set of all nick!user@host matched by this glob is a superset of those matched by 'other\''''
        return self.issuper_piece(self.nick, other.nick) and self.issuper_piece(self.user, other.user) and self.issuper_piece(self.host, other.host)
    
    def issub(self, other):
        '''Return True if the set of all nick!user@host matched by this glob is a subset of those matched by 'other\''''
        return other.issuper(self)
