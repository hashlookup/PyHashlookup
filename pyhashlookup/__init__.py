import argparse
import json

from .api import Hashlookup


def main() -> None:
    parser = argparse.ArgumentParser(description='Query hashlookup')
    parser.add_argument('--query', help='Hash (md5 or sha1) to lookup.')
    args = parser.parse_args()

    hashlookup = Hashlookup()

    response = hashlookup.lookup(args.query)
    print(json.dumps(response, indent=2))
