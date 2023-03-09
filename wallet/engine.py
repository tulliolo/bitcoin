#!/usr/bin/python3
#
#   Copyright (C) 2022 Tullio Loffredo, @tulliolo
#
#   It is subject to the license terms in the LICENSE file found in the top-level
#   directory of this distribution.
#
#   No part of this software, including this file, may be copied, modified,
#   propagated, or distributed except according to the terms contained in the
#   LICENSE file.
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
"""
BIP-032: HD Wallets
Link: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki
"""
import hmac
import logging

import base58 as base58
import coincurve as coincurve

from wallet import version

SEED_SIZE_RANGE = range(16, 65)  # bytes

LOGGER = logging.getLogger(__name__)


class Node:
    """
    A Node of an HD wallet.
    """
    __create_key = object()

    def __init__(
            self, create_key,
            network_id: version.NetworkId, address_type: version.AddressType,
            prvkey: bytes | None, pubkey: bytes | None, chacod: bytes,
            depth: int = 0, index: int = 0, path: str = "m",
            parent_fingerprint: bytes = bytes(4),
    ):
        assert create_key == Node.__create_key, \
            "node objects must be created from_seed or..."

        self.__network_id = network_id
        self.__address_type = address_type

        self.__prvkey = prvkey
        self.__pubkey = \
            pubkey if pubkey else \
            coincurve.PublicKey.from_valid_secret(prvkey).format()
        self.__chacod = chacod

        self.__depth = depth
        self.__index = index

        self.__path = path

        self.__parent_fingerprint = parent_fingerprint

    def __serialize(self, key_type: version.KeyType) -> bytes:
        assert self.__prvkey or key_type == version.KeyType.PUBKEY, \
            "invalid key type!\n\t" \
            "this is a view only wallet, private key is not present"

        return \
            version.get_version(self.__network_id, self.__address_type, key_type).to_bytes(4, byteorder='big') + \
            self.__depth.to_bytes(1, byteorder='big') + self.__parent_fingerprint + \
            self.__index.to_bytes(4, byteorder='big') + self.__chacod + \
            ((bytes(1) + self.__prvkey) if key_type == version.KeyType.PRVKEY else self.__pubkey)

    @classmethod
    def from_seed(
            cls, seed: bytes,
            network_id: version.NetworkId = version.NetworkId.DEFAULT,
            address_type: version.AddressType = version.AddressType.DEFAULT):
        """
        Generates the master node from seed
        https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#master-key-generation
        :param address_type: address type (e.g. p2wpkh)
        :param network_id: network id (e.g mainnet)
        :param seed: a seed value in bytes
        :return: the master Node object
        """

        if len(seed) not in SEED_SIZE_RANGE:
            raise ValueError("invalid seed size!\n\t"
                             f"expected: {min(SEED_SIZE_RANGE)}-{max(SEED_SIZE_RANGE)-1} bytes\n\t"
                             f"obtained: {len(seed)} bytes")

        seed = hmac.new(bytes('Bitcoin seed', 'utf-8'), seed, 'sha512').digest()

        return Node(
            create_key=cls.__create_key,
            network_id=network_id, address_type=address_type,
            prvkey=seed[:32], pubkey=None, chacod=seed[32:],
        )

    @property
    def path(self) -> str:
        """
        The node path
        :return:
        """
        return self.__path

    @property
    def xprvkey(self) -> str:
        """
        The extended private key
        :return:
        """
        return base58.b58encode_check(self.__serialize(version.KeyType.PRVKEY)).decode()

    @property
    def xpubkey(self) -> str:
        """
        The extended public key
        :return:
        """
        return base58.b58encode_check(self.__serialize(version.KeyType.PUBKEY)).decode()

    @property
    def info(self) -> dict:
        """
        The node information
        :return:
        """
        return {
            "path": self.__path,
            "cansign": True if self.__prvkey else False,
            "xpubkey": self.xpubkey,
            "network": self.__network_id,
            "version": self.__address_type
        }
