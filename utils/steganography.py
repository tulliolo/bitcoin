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
import math
import operator

from PIL import Image

from utils import encryption

LOGGER = logging.getLogger(__name__)


def __get_modified_pixels(image: Image, message: bytes, direction: encryption.Direction):
    image_size = operator.mul(*image.size)  # pixels
    message_size = len(message) * 3  # pixels

    if image_size < message_size:
        raise ValueError("invalid size\n\t"
                         "message is too long for this image")

    # encode message
    for i, value in enumerate(message):
        for j in range(3):
            ordinal = 3 * i + j
            coordinates, pixel = __get_pixel(image, direction, ordinal)
            yield coordinates, pixel, \
                tuple(
                    (pixel[k] & (2 ** 8 - 2)) | ((value >> (7 - ((ordinal % 3) * 3 + k))) & 1)
                    if (ordinal % 3) * 3 + k < 8 else
                    (pixel[k] & (2 ** 8 - 2)) | 1 if i < (len(message) - 1) else
                    pixel[k] & (2 ** 8 - 2)
                    for k in range(3)
                )


def __get_pixel(image: Image, direction: encryption.Direction, ordinal: int):
    image_size = operator.mul(*image.size)  # pixels
    image_width = image.size[0]  # pixels
    image_height = image.size[1]  # pixels

    index = \
        ordinal if direction == encryption.Direction.HORIZONTAL else \
            ((ordinal * image_width) + (ordinal // image_height)) % image_size if direction == encryption.Direction.VERTICAL else \
                (image_size - ordinal - 1) % image_size if direction == encryption.Direction.REVERSE_HORIZONTAL else \
                    (((image_size - ordinal - 1) * image_width) +
                     (image_size - ordinal - 1) // image_height) % image_size

    coordinates = (index % image_width, index // image_width)
    return coordinates, image.getpixel(coordinates)


def encode(
        message: str | bytes,
        image: Image,
        algorithm: encryption.Algorithm = encryption.Algorithm.NONE,
        direction: encryption.Direction = encryption.Direction.DEFAULT,
        password: str = None
) -> Image:
    if algorithm == encryption.Algorithm.PASSWORD and not password:
        raise ValueError("password cannot be empty")

    if isinstance(message, str):
        message = bytes(message, 'utf-8')

    message = encryption.encrypt(message, algorithm, password)
    omage = image.copy()

    LOGGER.debug(f"modifying pixels in {direction.to_string()} order")
    LOGGER.debug("coordinates, original pixel -> modified pixel")
    for coordinates, opixel, mpixel in __get_modified_pixels(image, message, direction):
        LOGGER.debug(f"{coordinates}, {opixel} -> {mpixel}")
        omage.putpixel(coordinates, mpixel)

    return omage


def decode(
        image: Image,
        algorithm: encryption.Algorithm = encryption.Algorithm.NONE,
        direction: encryption.Direction = encryption.Direction.HORIZONTAL,
        password: str = None
) -> bytes:
    if algorithm == encryption.Algorithm.PASSWORD and not password:
        raise ValueError("password cannot be empty")

    image_size = operator.mul(*image.size)  # pixels
    i = 0
    goon = True
    message = 0
    message_size = 0
    LOGGER.debug("coordinates -> pixel")
    while goon and i < image_size - 1:
        coordinates, pixel = __get_pixel(image, direction, i)
        LOGGER.debug(f"{coordinates} -> {pixel}")

        for j in range(3):
            message, message_size, goon = ((message << 1) | (pixel[j] & 1), message_size + 1, True) \
                if (i % 3) * 3 + j < 8 else (message, message_size, True) \
                    if (pixel[j] & 1) else (message, message_size, False)

        i += 1

    if goon:
        LOGGER.warning("cannot find an hidden message")
        message = 0
    else:
        LOGGER.debug(f"found an encrypted {message_size} bytes length message")
        message = message.to_bytes(math.ceil(message_size / 8), byteorder='big')
        message = encryption.decrypt(message, algorithm, password)
        LOGGER.debug(f"decrypted message: {message}")

    return message
