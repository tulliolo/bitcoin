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
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
import copy
import json
import logging
import math
from collections.abc import Iterable

from generator.entropy import Entropy
from generator.seed import Seed, ENTROPY_SIZE_ALL, WORD_SIZE, ENTROPY_SIZE_MIN
from generator.wordlist import wordlist

LOGGER = logging.getLogger(__name__)

CHECKSUM_SIZE_MIN = math.ceil(ENTROPY_SIZE_MIN / WORD_SIZE) * WORD_SIZE - ENTROPY_SIZE_MIN


def __invalidate_mnemonic(mnemonic: Iterable[str] | str) -> Iterable[str]:
    result = copy.deepcopy(mnemonic)
    result = result.split() if isinstance(result, str) else result

    last_wid = wordlist.index(result[-1])
    last_wid = \
        last_wid & (2 ** WORD_SIZE - 2 ** CHECKSUM_SIZE_MIN) | \
        (2 ** CHECKSUM_SIZE_MIN - 1 - (last_wid & (2 ** CHECKSUM_SIZE_MIN - 1)))

    result[-1] = wordlist[last_wid]

    return result


def test_mnemonic():
    with open('test_generator.json', 'r') as file:
        data = json.load(file)

    sep = "\n\t"
    group = 1
    failed = []

    LOGGER.info(f"START STATIC TESTS\n")
    for count, case in enumerate(data['vector']):
        entropy = case['entropy']
        mnemonic = case['mnemonic']
        rootseed = case['rootseed']

        for subcount in range(3):
            try:
                LOGGER.info(f"START TEST {group}.{count}.{subcount}")
                seed = \
                    Seed.from_entropy(entropy) if subcount == 0 else \
                        Seed.from_mnemonic(mnemonic) if subcount == 1 else \
                            Seed.from_mnemonic(__invalidate_mnemonic(mnemonic), True)
                seed.passphrase = "TREZOR"

                mnemonic_exp = mnemonic if isinstance(mnemonic, str) else " ".join(mnemonic)
                mnemonic_obt = " ".join(seed.mnemonic)
                assert mnemonic_obt == mnemonic_exp, f"invalid mnemonic{sep}" \
                                                     f"expected: '{mnemonic_exp}'{sep}" \
                                                     f"obtained: '{mnemonic_obt}'"

                rootseed_obt = seed.rootseed.hex()
                assert rootseed_obt == rootseed, f"invalid rootseed{sep}" \
                                                 f"expected: {rootseed}{sep}" \
                                                 f"obtained: {rootseed_obt}"

            except Exception as e:
                LOGGER.error(" | ".join(str(e).split(sep)))
                failed.append(f"{group}.{count}.{subcount}")
                raise e
            finally:
                LOGGER.info(f"STOP  TEST {group}.{count}.{subcount}\n")

    LOGGER.info("STOP  STATIC TESTS\n\n")

    group += 1

    LOGGER.info("START RANDOM TESTS\n")
    for count, size in enumerate(ENTROPY_SIZE_ALL):

        try:
            LOGGER.info(f"START TEST {group}.{count}")
            entropy = Entropy.generate(size)
            seed = Seed.from_entropy(entropy)

            LOGGER.info(f"mnemonic: '{' '.join(seed.mnemonic)}'")
            LOGGER.info(f"rootseed: '{seed.rootseed.hex()}'")
        except Exception as e:
            LOGGER.error(" | ".join(str(e).split(sep)))
            failed.append(f"{group}.{count}")
        finally:
            LOGGER.info(f"STOP  TEST {group}.{count}\n")

    LOGGER.info("STOP  RANDOM TESTS\n\n")

    group += 1

    LOGGER.info("START ERROR  TESTS")
    for count, test in enumerate(data['error']):
        error = test['error']

        try:
            LOGGER.info(f"START TEST {group}.{count}")

            seed = Seed.from_entropy(test['entropy']) if 'entropy' in test else Seed.from_mnemonic(test['mnemonic'])

            assert False, "failed to generate error"
        except Exception as e:
            LOGGER.error(" | ".join(str(e).split(sep)))

            try:
                assert error == str(e).split(sep)[0], f"invalid error{sep}" \
                                                      f"expected: '{error}'{sep}" \
                                                      f"obtained: '{str(e).split(sep)[0]}'"
            except AssertionError as ae:
                LOGGER.error(" | ".join(str(ae).split(sep)))
                failed.append(f"{group}.{count}")
        finally:
            LOGGER.info(f"STOP TEST {group}.{count}\n")

    LOGGER.info("STOP  ERROR  TESTS\n\n")

    LOGGER.info(
        f"OVERALL RESULT: {'FAILED' if failed else 'SUCCESS'}"
    )
    if failed:
        LOGGER.info(f"TESTS FAILED: {', '.join(failed)}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')
    test_mnemonic()
