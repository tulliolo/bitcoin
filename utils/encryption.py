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
import base64
import enum
import hashlib
import logging
from collections.abc import Iterator

from cryptography.fernet import Fernet

LOGGER = logging.getLogger(__name__)


class Algorithm(enum.Enum):
    NONE = 0
    NEGATIVE = 1
    REVERSAL = 2
    PASSWORD = 3

    def to_string(self) -> str:
        return \
            "none" if self == Algorithm.NONE else \
                "negative" if self == Algorithm.NEGATIVE else \
                    "reversal" if self == Algorithm.REVERSAL else \
                        "password"


class Direction(enum.Enum):
    HORIZONTAL = DEFAULT = 0
    VERTICAL = 1
    REVERSE_HORIZONTAL = 2
    REVERSE_VERTICAL = 3

    def to_string(self) -> str:
        return \
            "horizontal" if self == Direction.HORIZONTAL else \
                "vertical" if self == Direction.VERTICAL else \
                    "reverse_horizontal" if self == Direction.REVERSE_HORIZONTAL else \
                        "reverse_vertical"


def encrypt(message: str | bytes, algorithm: Algorithm, password: str | None = None) -> bytes:
    if isinstance(message, str):
        message = bytes(message, 'utf-8')

    LOGGER.debug(f"cipher algorithm: {algorithm.to_string()}")
    LOGGER.debug(f"original message: {str(message)}")
    if algorithm == Algorithm.NONE:
        LOGGER.warning("nothing to do")
    elif algorithm == Algorithm.NEGATIVE:
        message = __do_negative(message)
    elif algorithm == Algorithm.REVERSAL:
        message = __do_reversal(message)
    else:
        if not password:
            raise ValueError("password cannot be empty")

        key = base64.urlsafe_b64encode(hashlib.sha256(bytes(password, 'utf-8')).digest())
        f = Fernet(key)
        message = f.encrypt(message)

    LOGGER.debug(f"cipher message:   {str(message)}")
    return message


def decrypt(message: str | bytes, algorithm: Algorithm, password: str | None = None) -> bytes:
    if isinstance(message, str):
        message = bytes(message, 'utf-8')

    LOGGER.debug(f"decipher algorithm: {algorithm.to_string()}")
    LOGGER.debug(f"cipher message: {str(message)}")
    if algorithm == Algorithm.NONE:
        LOGGER.warning("nothing to do")
    elif algorithm == Algorithm.NEGATIVE:
        message = __do_negative(message)
    elif algorithm == Algorithm.REVERSAL:
        message = __do_reversal(message)
    else:
        if not password:
            raise ValueError("password cannot be empty")

        key = base64.urlsafe_b64encode(hashlib.sha256(bytes(password, 'utf-8')).digest())
        f = Fernet(key)
        message = f.decrypt(message)

    LOGGER.debug(f"original message: {str(message)}")
    return message


def __do_negative(message: bytes) -> bytes:
    message_size = len(message) * 8
    message = int.from_bytes(message, byteorder='big')
    return ((1 << message_size) - message - 1).to_bytes(message_size // 8, byteorder='big')


def __do_reversal(message: bytes) -> bytes:
    message_size = len(message) * 8
    return int(
        bin(
            int.from_bytes(message, byteorder='big')
        )[2:].zfill(message_size)[::-1],
        2
    ).to_bytes(message_size // 8, byteorder='big')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')

    message = "ciao"
    for a in Algorithm:
        cmessage = encrypt(message, a, "password")
        decrypt(cmessage, a, "password")
