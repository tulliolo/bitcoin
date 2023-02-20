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

from PIL import Image

from generator.entropy import BetterEntropy
from generator.seed import Seed
from utils import encryption, steganography

FILE_NAME = "test_image.jpg"
INPUT_PATH = "./input/"
OUTPUT_PATH = "./output/"

PASSWORD = "password"

LOGGER = logging.getLogger(__name__)


def test_steganography():
    input_file = INPUT_PATH + FILE_NAME
    input_file_name = FILE_NAME.split(".")[0]
    with Image.open(input_file, mode='r') as input_image:
        LOGGER.info(f"opened {'x'.join([str(val) for val in input_image.size])} image '{input_file}'")

        message = ' '.join(Seed.from_entropy(BetterEntropy.generate()).mnemonic)
        LOGGER.info(f"generated message '{message}'")

        failed = []
        for i, algorithm in enumerate(encryption.Algorithm):
            for j, direction in enumerate(encryption.Direction):
                LOGGER.info(f"START TEST {i+1}.{j}: {algorithm.to_string().upper()}.{direction.to_string().upper()}")
                try:
                    output_image = steganography.encode(message, input_image, algorithm, direction, PASSWORD)
                    output_file = \
                        OUTPUT_PATH + input_file_name + '_' + \
                        algorithm.to_string() + '_' + direction.to_string() + '.png'
                    output_image.save(output_file)
                    LOGGER.info(f"saved encoded "
                                f"{'x'.join([str(val) for val in output_image.size])} image '{output_file}'")

                    with Image.open(output_file, mode='r') as output_image:
                        LOGGER.info(f"opened encoded {'x'.join([str(val) for val in output_image.size])} "
                                    f"image '{output_file}'")
                        hidden_message = \
                            steganography.decode(output_image, algorithm, direction, PASSWORD).decode('utf-8')
                        LOGGER.info(f"decoded hidden message in '{output_file}': '{hidden_message}'")
                        assert message == hidden_message, "message doesn't match!\n\t" \
                                                          f"expected: {message}\n\t" \
                                                          f"obtained: {hidden_message}"
                except Exception as e:
                    LOGGER.error(e)
                    failed.append(f"{i+1}.{j}")
                finally:
                    LOGGER.info(
                        f"STOP  TEST {i+1}.{j}: {algorithm.to_string().upper()}.{direction.to_string().upper()}")

        num_tests = len(encryption.Algorithm) * len(encryption.Direction)
        LOGGER.info(f"TESTS OK: {num_tests - len(failed):2}/{num_tests:2}")
        LOGGER.info(f"TESTS KO: {len(failed):2}/{num_tests:2}")
        if len(failed):
            LOGGER.info(f"TESTS FAILED: {','.join(failed)}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')
    test_steganography()
