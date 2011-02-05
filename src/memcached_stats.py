import re, telnetlib

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

    def key_details(self, sort=True):
        ' Return a list of tuples containing keys and details '
        keys = []
        slab_ids = self.slab_ids()
        for id in slab_ids:
            self.client.write("stats cachedump %s 100\n" % id)
            response = self.client.read_until('END')
            keys.extend(re.findall('ITEM (.*) \[(.*); (.*)\]', response))
        if sort:
            return sorted(keys)
        return keys

    def keys(self, sort=True):
        ' Return a list of keys in use '
        return [key[0] for key in self.key_details(sort=sort)]

    def slab_ids(self):
        ' Return a list of slab ids in use '
        self.client.write("stats items\n")
        response = self.client.read_until('END')
        return re.findall('STAT items:(.*):number', response)

    def stats(self):
        ' Return a dict containing memcached stats '
        self.client.write("stats\n")
        response = self.client.read_until('END')
        return dict(re.findall("STAT (.*) (.*)\r", response))
