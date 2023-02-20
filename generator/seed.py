#!/usr/bin/python3
#
#   Copyright (C) 2022 Tullio Loffredo, @tulliolo
#
#   This file is implementing official bip-0039 specs at:
#   https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
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
import hashlib
import logging
import math

from collections.abc import Iterable

from generator.wordlist import wordlist

ENTROPY_SIZE_MIN = 128
ENTROPY_SIZE_MAX = 256
ENTROPY_SIZE_DIV = 32
ENTROPY_SIZE_ALL = sorted(tuple(
    set(
        math.ceil(i / ENTROPY_SIZE_DIV) * ENTROPY_SIZE_DIV for i in range(ENTROPY_SIZE_MIN, ENTROPY_SIZE_MAX + 1)
    )
))

WORD_SIZE = 11
WORD_COUNT_ALL = sorted(tuple(
    set(math.ceil(wc / WORD_SIZE) for wc in ENTROPY_SIZE_ALL)
))

LOGGER = logging.getLogger(__name__)


class Seed(object):
    __create_key = object()

    def __init__(self, create_key, entropy: bytes):
        assert create_key == Seed.__create_key, \
            "seed objects must be created from_entropy or from_mnemonic."

        self.__entropy = entropy
        self.__passphrase = ""

    def __eq__(self, other):
        result = False
        if isinstance(other, Seed):
            result = self.__entropy == other.__entropy and self.__passphrase == other.__passphrase

        return result

    @classmethod
    def from_entropy(cls, entropy: bytes | int | str) -> 'Seed':
        if isinstance(entropy, bytes):
            entropy_size = len(entropy) * 8
        elif isinstance(entropy, int):
            entropy_size = math.ceil(entropy.bit_length() / ENTROPY_SIZE_DIV) * ENTROPY_SIZE_DIV
            entropy = entropy.to_bytes(entropy_size // 8, byteorder='big')
        elif isinstance(entropy, str):
            try:
                entropy = bytes.fromhex(entropy)
            except ValueError as ve:
                raise ValueError(f"invalid entropy value\n\t{ve}") from None
            entropy_size = len(entropy) * 8
        else:
            raise TypeError("invalid entropy type\n\t"
                            "entropy must be of type bytes, int or string")

        LOGGER.debug(f"entropy: {entropy.hex()}")

        if entropy_size not in ENTROPY_SIZE_ALL:
            raise ValueError("invalid entropy size\n\t"
                             f"expected: {', '.join(str(v) for v in ENTROPY_SIZE_ALL)} bits\n\t"
                             f"obtained: {entropy_size} bits")

        return Seed(cls.__create_key, entropy)

    @classmethod
    def from_mnemonic(cls, mnemonic: Iterable[str] | str, correct_last_word: bool = False) -> 'Seed':
        if isinstance(mnemonic, str):
            mnemonic = mnemonic.split()
        elif not isinstance(mnemonic, Iterable):
            raise TypeError("invalid mnemonic type\n\t"
                            "mnemonic must be of type string or iterable of strings")
        else:
            mnemonic = tuple(mnemonic)

        LOGGER.debug(f"mnemonic: {' '.join(mnemonic)}")

        word_count = len(mnemonic)
        if word_count not in WORD_COUNT_ALL:
            raise ValueError("invalid mnemonic size\n\t"
                             f"expected: {', '.join(str(v) for v in WORD_COUNT_ALL)} words\n\t"
                             f"obtained: {word_count} words")

        seed = 0
        word = ""
        for i, word in enumerate(mnemonic):
            try:
                wid = wordlist.index(word)
            except ValueError as ve:
                raise ValueError(f"invalid mnemonic word\n\t{str(ve)}")

            seed = (seed << WORD_SIZE) | wid

        LOGGER.debug(f"seed: {hex(seed)[2:]}")

        seed_size = word_count * WORD_SIZE
        entropy_size = seed_size // ENTROPY_SIZE_DIV * ENTROPY_SIZE_DIV
        checksum_size = seed_size - entropy_size

        entropy = (seed >> checksum_size).to_bytes(entropy_size // 8, byteorder='big')
        checksum = seed & (2 ** checksum_size - 1)
        LOGGER.debug(f"entropy: {entropy.hex()}")
        LOGGER.debug(f"checksum: {bin(checksum)[2:].zfill(checksum_size)}")

        result = Seed(cls.__create_key, entropy)
        if result.checksum != checksum:
            if correct_last_word:
                LOGGER.info(f"last word modified from '{word}' to '{list(result.mnemonic)[-1]}' to match checksum")
            else:
                raise ValueError("invalid checksum\n\t"
                                 f"expected: {bin(result.checksum)[2:].zfill(checksum_size)}\n\t"
                                 f"obtained: {bin(checksum)[2:].zfill(checksum_size)}")

        return result

    @property
    def checksum(self) -> int:
        entropy_size = len(self.__entropy) * 8
        checksum_size = math.ceil(entropy_size / WORD_SIZE) * WORD_SIZE - entropy_size

        entropy_hash = hashlib.sha256(self.__entropy).digest()
        LOGGER.debug(f"entropy_hash: {entropy_hash.hex()}")

        checksum = entropy_hash[0] >> (8 - checksum_size)
        LOGGER.debug(f"checksum: {bin(checksum)[2:].zfill(checksum_size)}")

        return checksum

    @property
    def entropy(self) -> bytes:
        return self.__entropy

    @property
    def mnemonic(self) -> tuple[str]:
        entropy_size = len(self.__entropy) * 8
        checksum_size = math.ceil(entropy_size / WORD_SIZE) * WORD_SIZE - entropy_size

        seed = (int.from_bytes(self.__entropy, byteorder='big') << checksum_size) | self.checksum
        LOGGER.debug(f"seed: {hex(seed)[2:]}")

        word_count = (entropy_size + checksum_size) // WORD_SIZE
        mnemonic = []
        for i in range(word_count):
            wid = seed >> ((word_count - i - 1) * WORD_SIZE) & (2 ** WORD_SIZE - 1)
            word = str(wordlist[wid])

            LOGGER.debug(f"word {i + 1:2}: {wid:4} - {word}")
            mnemonic.append(word)

        return tuple(mnemonic)

    @property
    def passphrase(self):
        return self.__passphrase

    @passphrase.setter
    def passphrase(self, passphrase: str):
        self.__passphrase = str(passphrase)

    @property
    def rootseed(self) -> bytes:
        return hashlib.pbkdf2_hmac('sha512',
                                   bytes(" ".join(self.mnemonic), 'utf-8'),
                                   bytes('mnemonic' + self.__passphrase, 'utf-8'), 2048)
