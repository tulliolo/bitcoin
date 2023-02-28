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
SLIP-0132 : Registered HD version bytes for BIP-0032
Link: https://github.com/satoshilabs/slips/blob/master/slip-0132.md
"""
import enum

__SUPPORTED_VERSIONS = {
    # MAINNET
    'mainnet': {
        # P2SH
        'p2sh': {
            'path': 'm/44h/0h',
            'pubkey': 0x0488b21e,
            'prvkey': 0x0488ade4
        },
        # P2SH-P2WPKH
        'p2sh-p2wpkh': {
            'path': 'm/49h/0h',
            'pubkey': 0x049d7cb2,
            'prvkey': 0x049d7878
        },
        # P2WPKH
        'p2wpkh': {
            'path': 'm/84h/0h',
            'pubkey': 0x04b24746,
            'prvkey': 0x04b2430c
        }
    },
    # TESTNET
    'testnet': {
        # P2SH
        'p2sh': {
            'path': 'm/44h/1h',
            'pubkey': 0x043587cf,
            'prvkey': 0x04358394
        },
        # P2SH-P2WPKH
        'p2sh-p2wpkh': {
            'path': 'm/49h/1h',
            'pubkey': 0x044a5262,
            'prvkey': 0x044a4e28
        },
        # P2WPKH
        'p2wpkh': {
            'path': 'm/84h/1h',
            'pubkey': 0x045f1cf6,
            'prvkey': 0x045f18bc
        }
    }
}


class NetworkId(enum.Enum):
    """
    ID of the supported network (mainnet or testnet)
    """
    MAINNET = DEFAULT = 'mainnet'
    TESTNET = 'testnet'


class AddressTypeId(enum.Enum):
    """
    ID of the supported address type (p2sh, p2sh_p2wpkh, p2wpkh)
    """
    P2SH = 'p2sh'
    P2SH_P2WPKH = 'p2sh_p2wpkh'
    P2WPKH = DEFAULT = 'p2wpkh'


class KeyTypeId(enum.Enum):
    """
    ID of the supported key type (pubkey or prvkey)
    """
    PUBKEY = DEFAULT = 'pubkey'
    PRVKEY = 'prvkey'


def find_by_version(value: int) -> tuple[NetworkId, AddressTypeId, KeyTypeId]:
    """
    Find network_id, addresstype_id and keytype_id for a supported version value.\n
    :param value: a public or a private key version value
    :return: network_id, addresstype_id and keytype_id supporting the value, or none if not found
    """
    result = [
        (NetworkId(network_id), AddressTypeId(addresstype_id), KeyTypeId(keytype_id))
        for network_id in __SUPPORTED_VERSIONS.keys()
        for addresstype_id in __SUPPORTED_VERSIONS[network_id].keys()
        for keytype_id in __SUPPORTED_VERSIONS[network_id][addresstype_id].keys()
        if value == __SUPPORTED_VERSIONS[network_id][addresstype_id][keytype_id]
    ]

    return result[0] if result else None


def find_by_path(value):
    """
    Find network_id and addresstype_id for a supported default path value.\n
    :param value: a default path value
    :return: network_id and addresstype_id supporting the value, or none if not found
    """
    result = [
        (NetworkId(network_id), AddressTypeId(addresstype_id))
        for network_id in __SUPPORTED_VERSIONS.keys()
        for addresstype_id in __SUPPORTED_VERSIONS[network_id].keys()
        if value == __SUPPORTED_VERSIONS[network_id][addresstype_id]['path']
    ]

    return result[0] if result else None


def get_path(network_id: NetworkId, addresstype_id: AddressTypeId) -> str:
    """
    Get the default path for network_id and addresstype_id (e.g. m/84h/0h for mainnet p2wpkh).\n
    :param network_id: network id (e.g mainnet)
    :param addresstype_id: address type id (e.g. p2wpkh)
    :return: the default path value
    """
    return __SUPPORTED_VERSIONS[network_id.value][addresstype_id.value]['path']


def get_version(network_id: NetworkId, addresstype_id: AddressTypeId, keytype_id: KeyTypeId) -> int:
    """
    Get the key version value for network_id, addresstype_id and keytype_id
    (e.g. '04b24746' for mainnet, p2wpkh, pubkey)\n
    :param network_id: network id (e.g mainnet)
    :param addresstype_id: address type id (e.g. p2wpkh)
    :param keytype_id: key type id (e.g. pubkey)
    :return: the public or private key version value
    """
    return __SUPPORTED_VERSIONS[network_id.value][addresstype_id.value][keytype_id.value]