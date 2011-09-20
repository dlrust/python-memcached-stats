# python-memcached-stats

Python class to gather stats and slab keys from memcached via the memcached telnet interface

## Usage

Basic usage:

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

## List the keys

If you just want to list some of the keys in memcached, run this from the command line:

    python -m memcached_stats <ip> <port>

ip defaults to 127.0.0.1 and port defaults to 11211.

## Installation

    pip install 'git+git://github.com/dlrust/python-memcached-stats.git'

## License

python-memcached-stats is released under the [MIT license](http://creativecommons.org/licenses/MIT/).
