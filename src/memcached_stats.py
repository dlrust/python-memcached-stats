import re, telnetlib

key_regex = re.compile(ur'ITEM (.*) \[(.*); (.*)\]')
slab_regex = re.compile(ur'STAT items:(.*):number')
stat_regex = re.compile(ur"STAT (.*) (.*)\r")

class MemcachedStats:

    _client = None

    def __init__(self, host='localhost', port='11211'):
        self._host = host
        self._port = port

    @property
    def client(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port)
        return self._client

    def command(self, cmd):
        ' Write a command to telnet and return the response '
        self.client.write("%s\n" % cmd)
        return self.client.read_until('END')

    def key_details(self, sort=True):
        ' Return a list of tuples containing keys and details '
        cmd = 'stats cachedump %s 100'
        keys = []
        for id in self.slab_ids():
            keys.extend(key_regex.findall(self.command(cmd % id)))
        if sort:
            return sorted(keys)
        else:
            return keys

    def keys(self, sort=True):
        ' Return a list of keys in use '
        return [key[0] for key in self.key_details(sort=sort)]

    def slab_ids(self):
        ' Return a list of slab ids in use '
        return slab_regex.findall(self.command('stats items'))

    def stats(self):
        ' Return a dict containing memcached stats '
        return dict(stat_regex.findall(self.command('stats')))
