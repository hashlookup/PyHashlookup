#!/usr/bin/env python3

from __future__ import annotations

import json
import typing

from importlib.metadata import version
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import dns.resolver
import requests


class PyHashlookupError(Exception):
    pass


class Hashlookup():

    def __init__(self, root_url: str='https://hashlookup.circl.lu/', useragent: str | None=None):
        '''Query a specific hashlookup instance.

        :param root_url: URL of the instance to query.
        '''
        self.root_url = root_url
        if not urlparse(self.root_url).scheme:
            self.root_url = 'http://' + self.root_url
        if not self.root_url.endswith('/'):
            self.root_url += '/'

        self.session = requests.session()
        self.session.headers['user-agent'] = useragent if useragent else f'PyHashlookup / {version("pyhashlookup")}'

    def info(self) -> dict[str, str]:
        '''Get the information about the database.'''
        r = self.session.get(urljoin(self.root_url, 'info'))
        return r.json()

    def top(self) -> dict[str, Any]:
        '''Get the information about the database.'''
        r = self.session.get(urljoin(self.root_url, 'stats/top'))
        return r.json()

    def info_over_dns(self) -> dict[str, str]:
        '''Get the information about the database.'''
        answer = dns.resolver.resolve('info.dns.hashlookup.circl.lu', 'TXT')
        a = str(answer[0])
        return json.loads(json.loads(a))

    def md5_lookup_over_dns(self, md5: str) -> dict[str, str | dict[str, str]]:
        '''Lookup a MD5, over DNS'''
        md5 = md5.lower()
        answer = dns.resolver.resolve(f'{md5}.dns.hashlookup.circl.lu', 'TXT')
        a = str(answer[0])
        return json.loads(json.loads(a))

    def sha1_lookup_over_dns(self, sha1: str) -> dict[str, str | dict[str, str]]:
        '''Lookup a SHA1, over DNS'''
        sha1 = sha1.lower()
        answer = dns.resolver.resolve(f'{sha1}.dns.hashlookup.circl.lu', 'TXT')
        a = str(answer[0])
        return json.loads(json.loads(a))

    def md5_lookup(self, md5: str) -> dict[str, str | dict[str, str]]:
        '''Lookup a MD5'''
        r = self.session.get(urljoin(self.root_url, str(Path('lookup', 'md5', md5))))
        return r.json()

    def sha1_lookup(self, sha1: str) -> dict[str, str | dict[str, str]]:
        '''Lookup a SHA1'''
        r = self.session.get(urljoin(self.root_url, str(Path('lookup', 'sha1', sha1))))
        return r.json()

    def sha256_lookup(self, sha256: str) -> dict[str, str | dict[str, str]]:
        '''Lookup a SHA256'''
        r = self.session.get(urljoin(self.root_url, str(Path('lookup', 'sha256', sha256))))
        return r.json()

    def md5_bulk_lookup(self, md5: list[str]) -> list[dict[str, str]]:
        '''Lookup a list of MD5'''
        to_post = {'hashes': md5}
        r = self.session.post(urljoin(self.root_url, str(Path('bulk', 'md5'))), json=to_post)
        return r.json()

    def sha1_bulk_lookup(self, sha1: list[str]) -> list[dict[str, str]]:
        '''Lookup a list of SHA1'''
        to_post = {'hashes': sha1}
        r = self.session.post(urljoin(self.root_url, str(Path('bulk', 'sha1'))), json=to_post)
        return r.json()

    def sha1_children(self, sha1: str, count: int=100, cursor: str='0') -> dict[str, list[str] | str | int]:
        """Return children from a given SHA1."""
        r = self.session.get(urljoin(self.root_url, str(Path('children', sha1, str(count), cursor))))
        return r.json()

    def sha1_parents(self, sha1: str, count: int=100, cursor: str='0') -> dict[str, list[str] | str | int]:
        """Return parents from a given SHA1."""
        r = self.session.get(urljoin(self.root_url, str(Path('parents', sha1, str(count), cursor))))
        return r.json()

    @typing.overload
    def lookup(self, to_lookup: list[str]) -> list[dict[str, str]]:
        ...  # pragma: no cover

    @typing.overload
    def lookup(self, to_lookup: str) -> dict[str, str | dict[str, str]]:
        ...  # pragma: no cover

    def lookup(self, to_lookup: list[str] | str) -> list[dict[str, str]] | dict[str, str | dict[str, str]]:
        """Lookup for (a list of) MD5 or SHA1"""
        if isinstance(to_lookup, str):
            if len(to_lookup) == 32:
                return self.md5_lookup(to_lookup)
            elif len(to_lookup) == 40:
                return self.sha1_lookup(to_lookup)
            elif len(to_lookup) == 64:
                return self.sha256_lookup(to_lookup)
            raise PyHashlookupError('The hash must be either MD5, SHA1 or SHA256')
        elif isinstance(to_lookup, list):
            if all(len(lookup_hash) == 32 for lookup_hash in to_lookup):
                return self.md5_bulk_lookup(to_lookup)
            elif all(len(lookup_hash) == 40 for lookup_hash in to_lookup):
                return self.sha1_bulk_lookup(to_lookup)
            raise PyHashlookupError('The hashes must be either MD5 or SHA1')
        raise PyHashlookupError('Only (list of) MD5 or SHA1 are support at this time.')
