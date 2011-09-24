#!/usr/bin/env python
import re, telnetlib, sys
from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL, '')


class MemcachedStats:
    # https://github.com/dlrust/python-memcached-stats
    _client = None
    _key_regex = re.compile(ur'ITEM (.*) \[(.*); (.*)\]')
    _slab_regex = re.compile(ur'STAT items:(.*):number')
    _stat_regex = re.compile(ur"STAT (.*) (.*)\r")

    def __init__(self, host='localhost', port='11211'):
        self._host = host
        self._port = port

    def __str__(self):
        return  self.format_details(self.get_details())

    @property
    def client(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port)
        return self._client

    def command(self, cmd):
        ' Write a command to telnet and return the response '
        self.client.write("%s\n" % cmd)
        return self.client.read_until('END')

    def get_details(self, sort=True, limit=100):
        cmd = 'stats cachedump %s %s'
        stats = []
        for idn in self.slab_ids():
            dump = self.command(cmd % (idn, limit))
            tokens = re.split(r'[ :\[\]]', dump)
            stats.append(tokens)

        if sort:
            return sorted(stats, key=lambda x: x[3])
        else:
            return stats

    def format_details(self, stats, header=True, headerlens=[-40, 20, -20]):
        fmtstrs = [ ('%%%s.%ss ' % (l, abs(l))) for l in headerlens ]
        details = ''
        if header:
            details += fmtstrs[0] % 'KEY '
            details += fmtstrs[1] % 'SIZE    '
            details += (fmtstrs[2] + '\n') % 'EXPIRES'

        for stat in stats:
            details += fmtstrs[0] % stat[3]        # name
            details += fmtstrs[1] % (              # bytes
                locale.format('%d', int(stat[5]), True) + ' b    ')
            datestr = str(datetime.fromtimestamp(int(stat[7])) - datetime.now())
            datestr = ''.join(datestr.partition('.')[0])  # chop ms
            details += (fmtstrs[2] + '\n') % datestr       # date
        return details

    def key_details(self, sort=True, limit=100):
        ' Return a list of tuples containing keys and details '
        cmd = 'stats cachedump %s %s'
        keys = [key for id in self.slab_ids()
            for key in self._key_regex.findall(self.command(cmd % (id, limit)))]
        if sort:
            return sorted(keys)
        else:
            return keys

    def keys(self, sort=True, limit=100):
        ' Return a list of keys in use '
        return [key[0] for key in self.key_details(sort=sort, limit=limit)]

    def slab_ids(self):
        ' Return a list of slab ids in use '
        return self._slab_regex.findall(self.command('stats items'))

    def stats(self):
        ' Return a dict containing memcached stats '
        return dict(self._stat_regex.findall(self.command('stats')))

def main(argv=None):
    if not argv:
        argv = sys.argv
    host = argv[1] if len(argv) >= 2 else '127.0.0.1'
    port = argv[2] if len(argv) >= 3 else '11211'
    import pprint
    m = MemcachedStats(host, port)
    print m

if __name__ == '__main__':
    main()
