#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, List, Union
from urllib.parse import urljoin, urlparse
from pathlib import Path

import requests


class PyHashlookupError(Exception):
    pass


class Hashlookup():

    def __init__(self, root_url: str='https://hashlookup.circl.lu/'):
        '''Query a specific hashlookup instance.

        :param root_url: URL of the instance to query.
        '''
        self.root_url = root_url

        if not urlparse(self.root_url).scheme:
            self.root_url = 'http://' + self.root_url
        if not self.root_url.endswith('/'):
            self.root_url += '/'
        self.session = requests.session()

    def info(self) -> Dict[str, str]:
        '''Get the information about the database.'''
        r = self.session.get(urljoin(self.root_url, 'info'))
        return r.json()

    def md5_lookup(self, md5: str) -> Dict[str, Union[str, Dict[str, str]]]:
        '''Lookup a MD5'''
        r = self.session.get(urljoin(self.root_url, str(Path('lookup', 'md5', md5))))
        return r.json()

    def sha1_lookup(self, sha1: str) -> Dict[str, Union[str, Dict[str, str]]]:
        '''Lookup a SHA1'''
        r = self.session.get(urljoin(self.root_url, str(Path('lookup', 'sha1', sha1))))
        return r.json()

    def md5_bulk_lookup(self, md5: List[str]) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        '''Lookup a list of MD5'''
        to_post = {'hashes': md5}
        r = self.session.post(urljoin(self.root_url, str(Path('bulk', 'md5'))), json=to_post)
        return r.json()

    def sha1_bulk_lookup(self, sha1: List[str]) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        '''Lookup a list of SHA1'''
        to_post = {'hashes': sha1}
        r = self.session.post(urljoin(self.root_url, str(Path('bulk', 'sha1'))), json=to_post)
        return r.json()

    def lookup(self, to_lookup: Union[str, List[str]]) -> Union[Dict[str, Union[str, Dict[str, str]]], List[Dict[str, Union[str, Dict[str, str]]]]]:
        """Lookup for (a list of) MD5 or SHA1"""
        if isinstance(to_lookup, str):
            if len(to_lookup) == 32:
                return self.md5_lookup(to_lookup)
            elif len(to_lookup) == 40:
                return self.sha1_lookup(to_lookup)
            raise PyHashlookupError('The hash must be either MD5 or SHA1')
        elif isinstance(to_lookup, list):
            if all(len(lookup_hash) == 32 for lookup_hash in to_lookup):
                return self.md5_bulk_lookup(to_lookup)
            elif all(len(lookup_hash) == 40 for lookup_hash in to_lookup):
                return self.sha1_bulk_lookup(to_lookup)
            raise PyHashlookupError('The hashes must be either MD5 or SHA1')
        raise PyHashlookupError('Only (list of) MD5 or SHA1 are support at this time.')
