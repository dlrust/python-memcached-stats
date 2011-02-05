# python-memcached-stats

Python class to gather stats and slab keys from memcached via the memcached telnet interface

## Usage

Usage is simple:

    from memcached_stats import MemcachedStats
    mem = MemcachedStats()

By default, it connects to localhost on port 11211. If you need to specify a host and/or port:

    mem = MemcachedStats('1.2.3.4', '11211')

Retrieve a dict containing the current stats from memcached:

    >>> mem.stats()
    {'accepting_conns': '1',
     'auth_cmds': '0',
     'auth_errors': '0',
     ... }

Retrieve a list of keys currently in use:

    >>> mem.keys()
    ['key-1',
     'key-2',
     'key-3',
     ... ]
