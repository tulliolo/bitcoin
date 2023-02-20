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
import logging
from collections.abc import Iterable

from generator.seed import Seed
from utils import encryption

WORD_COUNT_BASE = 12
WORD_COUNT_JOIN = 2 * WORD_COUNT_BASE

LOGGER = logging.getLogger(__name__)


def split(
        mnemonic: Iterable[str] | str,
        algorithm: encryption.Algorithm = encryption.Algorithm.NONE
) -> Iterable[Iterable[str]]:
    mnemonic = mnemonic.split() if isinstance(mnemonic, str) else tuple(mnemonic)
    word_count = len(mnemonic)

    if word_count != WORD_COUNT_JOIN:
        raise ValueError("invalid word count\n\t"
                         f"expected: {WORD_COUNT_JOIN}"
                         f"obtained: {word_count}")

    if algorithm == encryption.Algorithm.PASSWORD:
        raise ValueError("invalid algorithm\n\t"
                         f"expected: {', '.join([a.to_string() for a in encryption.Algorithm if a != encryption.Algorithm.PASSWORD])}\n\t "
                         f"obtained: {encryption.Algorithm.PASSWORD.to_string()}")

    entropy = encryption.encrypt(Seed.from_mnemonic(mnemonic).entropy, algorithm)
    entropy_size = len(entropy) * 8

    LOGGER.debug(f"original entropy: {entropy.hex().zfill(2 * entropy_size // 8)}")

    entropy = int.from_bytes(entropy, byteorder='big')
    entropy_size //= 2
    entropy_split = (
        entropy >> entropy_size,
        entropy & (2 ** entropy_size - 1)
    )

    for count, value in enumerate(entropy_split):
        LOGGER.debug(f"entropy_{'r' if count else 'l'}: {hex(value)[2:].zfill(entropy_size // 8)}")
        yield Seed.from_entropy(value.to_bytes(entropy_size // 8, byteorder='big')).mnemonic


def join(
        mnemonic_1: Iterable[str] | str,
        mnemonic_2: Iterable[str] | str,
        algorithm: encryption.Algorithm = encryption.Algorithm.NONE
) -> Iterable[str]:
    if algorithm == encryption.Algorithm.PASSWORD:
        raise ValueError("invalid algorithm\n\t"
                         f"expected: {', '.join([a.to_string() for a in encryption.Algorithm if a != encryption.Algorithm.PASSWORD])}\n\t "
                         f"obtained: {encryption.Algorithm.PASSWORD.to_string()}")

    entropy_joint = 0
    entropy_joint_size = 0
    for count, mnemonic in enumerate((mnemonic_1, mnemonic_2)):
        mnemonic = mnemonic.split() if isinstance(mnemonic, str) else list(mnemonic)

        word_count = len(mnemonic)
        if word_count != WORD_COUNT_BASE:
            raise ValueError("invalid word count\n\t"
                             f"expected: {WORD_COUNT_BASE}\n\t"
                             f"obtained: {word_count}")

        entropy = Seed.from_mnemonic(mnemonic).entropy
        entropy_joint = (entropy_joint << len(entropy) * 8) | int.from_bytes(entropy, byteorder='big')
        entropy_joint_size += len(entropy)

        LOGGER.debug(f"original entropy {count}: {entropy.hex().zfill(len(entropy) * 2)}")

    entropy_joint = encryption.encrypt(entropy_joint.to_bytes(entropy_joint_size, byteorder='big'), algorithm)

    LOGGER.debug(f"joint entropy: {entropy_joint.hex().zfill(2 * entropy_joint_size)}")

    return Seed.from_entropy(entropy_joint).mnemonic
