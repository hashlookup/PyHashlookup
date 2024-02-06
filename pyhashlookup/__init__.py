from __future__ import annotations

import argparse
import json

from .api import Hashlookup, PyHashlookupError  # noqa

__all__ = ['Hashlookup', 'PyHashlookupError']


def main() -> None:
    parser = argparse.ArgumentParser(description='Query hashlookup')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--query', action="extend", nargs="+", type=str, help='(list of) hash(es) (md5 or sha1) to lookup.')
    group.add_argument('--info', action='store_true', help='Get info about database')
    group.add_argument('--top', action='store_true', help='Get top requests against database')
    args = parser.parse_args()

    hashlookup = Hashlookup()

    if args.query:
        if len(args.query) == 1:
            query = args.query[0]
        else:
            query = args.query
        response = hashlookup.lookup(query)
    elif args.info:
        response = hashlookup.info()
    elif args.top:
        response = hashlookup.top()
    print(json.dumps(response, indent=2))
