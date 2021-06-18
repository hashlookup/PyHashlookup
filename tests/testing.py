#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from typing import Dict, Union, List

from pyhashlookup import Hashlookup


class UnitTesting(unittest.TestCase):

    public_instance: Hashlookup

    @classmethod
    def setUpClass(cls) -> None:
        setattr(cls, "public_instance", Hashlookup())

    def test_info(self) -> None:
        response = self.public_instance.info()
        self.assertTrue('hashlookup-version' in response)

    def test_lookup(self) -> None:
        md5 = '8ED4B4ED952526D89899E723F3488DE4'
        sha1 = 'FFFFFDAC1B1B4C513896C805C2C698D9688BE69F'
        bulk_md5 = ['6E2F8616A01725DCB37BED0A2495AEB2', '8ED4B4ED952526D89899E723F3488DE4', '344428FA4BA313712E4CA9B16D089AC4']
        bulk_sha1 = ['FFFFFDAC1B1B4C513896C805C2C698D9688BE69F', 'FFFFFF4DB8282D002893A9BAF00E9E9D4BA45E65', 'FFFFFE4C92E3F7282C7502F1734B243FA52326FB']
        response_md5: Dict[str, Union[str, Dict[str, str]]] = self.public_instance.lookup(md5)  # type: ignore
        response_sha1: Dict[str, Union[str, Dict[str, str]]] = self.public_instance.lookup(sha1)  # type: ignore
        response_bulk_md5: List[Dict[str, Union[str, Dict[str, str]]]] = self.public_instance.lookup(bulk_md5)  # type: ignore
        response_bulk_sha1: List[Dict[str, Union[str, Dict[str, str]]]] = self.public_instance.lookup(bulk_sha1)  # type: ignore

        self.assertEqual(response_md5['CRC32'], '7A5407CA', response_md5)

        self.assertEqual(response_sha1['CRC32'], 'CBD64CD9', response_sha1)

        self.assertEqual(response_bulk_md5[0]['CRC32'], 'E774FD92', response_bulk_md5)
        self.assertEqual(response_bulk_md5[1]['CRC32'], '7A5407CA', response_bulk_md5)
        self.assertEqual(response_bulk_md5[2]['CRC32'], '7516A25F', response_bulk_md5)

        self.assertEqual(response_bulk_sha1[0]['CRC32'], 'CBD64CD9', response_bulk_sha1)
        self.assertEqual(response_bulk_sha1[1]['CRC32'], '8654F11A', response_bulk_sha1)
        self.assertEqual(response_bulk_sha1[2]['CRC32'], '8E51A269', response_bulk_sha1)

    def test_dns_lookup(self) -> None:
        md5 = '6E2F8616A01725DCB37BED0A2495AEB2'.lower()
        response_md5: Dict[str, Union[str, Dict[str, str]]] = self.public_instance.md5_lookup_over_dns(md5)
        self.assertEqual(response_md5['CRC32'], 'E774FD92', response_md5)

        sha1 = 'FFFFFDAC1B1B4C513896C805C2C698D9688BE69F'.lower()
        response_sha1: Dict[str, Union[str, Dict[str, str]]] = self.public_instance.sha1_lookup_over_dns(sha1)
        self.assertEqual(response_sha1['CRC32'], 'CBD64CD9')
        sha1 = 'FFFFFF4DB8282D002893A9BAF00E9E9D4BA45E65'.lower()
        response_sha1 = self.public_instance.sha1_lookup_over_dns(sha1)
        self.assertEqual(response_sha1['CRC32'], '8654F11A')


if __name__ == '__main__':
    unittest.main()
