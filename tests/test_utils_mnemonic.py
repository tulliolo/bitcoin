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
import json
import logging

from generator.entropy import BetterEntropy
from generator.seed import Seed
from utils import encryption
from utils.mnemonic import split, join

LOGGER = logging.getLogger(__name__)


def test_mnemonic_masking():
    with open("test_utils_mnemonic.json", "r") as file:
        data = json.load(file)

    failed = []
    sep = "\n\t"

    for gcount, group in enumerate(data):
        LOGGER.info(f"START TEST GROUP {gcount + 1}: {group.upper()}")
        if group == "static":
            for scount, sgroup in enumerate(['split', 'join']):
                LOGGER.info(f"START TEST SUBGROUP {gcount + 1}.{scount}: {group.upper()}.{sgroup.upper()}")
                for count, case in enumerate(data[group]):
                    transformation = encryption.Algorithm(case['transformation'])
                    LOGGER.info(f"START TEST CASE {gcount + 1}.{scount}.{count}: "
                                f"{group.upper()}.{sgroup.upper()}.{transformation.to_string().upper()}")

                    try:
                        if sgroup == "split":
                            mnemonic = case['mnemonic_o']
                            for count, obt_mnemonic in enumerate(tuple(split(mnemonic, transformation))):
                                exp_mnemonic = case[f'mnemonic_{count+1}']
                                assert " ".join(obt_mnemonic) == exp_mnemonic, \
                                    f"invalid mnemonic{sep}" \
                                    f"expected: '{exp_mnemonic}'{sep}" \
                                    f"obtained: '{' '.join(obt_mnemonic)}'"
                        else:
                            mnemonic = case['mnemonic_1'], case['mnemonic_2']
                            exp_mnemonic = case['mnemonic_o']
                            obt_mnemonic = join(*mnemonic, transformation)
                            assert " ".join(obt_mnemonic) == exp_mnemonic, \
                                f"invalid mnemonic{sep}" \
                                f"expected: '{exp_mnemonic}'{sep}" \
                                f"obtained: '{' '.join(obt_mnemonic)}'"
                    except Exception as e:
                        LOGGER.error(" | ".join(str(e).split(sep)))
                        failed.append(f"{gcount + 1}.{scount}.{count}")
                        raise e
                    finally:
                        LOGGER.info(f"STOP TEST CASE {gcount + 1}.{scount}.{count}: "
                                    f"{group.upper()}.{sgroup.upper()}.{transformation.to_string().upper()}")

        elif group == "dynamic" and data[group]:
            for count, transformation in enumerate(encryption.Algorithm):
                if transformation != encryption.Algorithm.PASSWORD:
                    LOGGER.info(f"START TEST CASE {gcount + 1}.{count}: {transformation.to_string().upper()}")
                    try:
                        exp_mnemonic = Seed.from_entropy(BetterEntropy.generate()).mnemonic
                        obt_mnemonic = split(exp_mnemonic, transformation)
                        obt_mnemonic = join(*obt_mnemonic, transformation)

                        assert obt_mnemonic == exp_mnemonic, \
                            f"invalid mnemonic{sep}" \
                            f"expected: '{' '.join(exp_mnemonic)}'{sep}" \
                            f"obtained: '{' '.join(obt_mnemonic)}'"

                    except Exception as e:
                        LOGGER.error(" | ".join(str(e).split(sep)))
                        failed.append(f"{gcount + 1}.{scount}.{count}")
                    finally:
                        LOGGER.info(f"STOP  TEST CASE {gcount + 1}.{count}: {transformation.to_string().upper()}")

            LOGGER.info(f"STOP  TEST GROUP {gcount + 1}: {group.upper()}\n\n")

        LOGGER.info(
            f"OVERALL RESULT: {'FAILED' if failed else 'SUCCESS'}"
        )
        if failed:
            LOGGER.info(f"TESTS FAILED: {', '.join(failed)}")


#    for gcount, group in enumerate(data):
#        LOGGER.info(f"START TEST GROUP {gcount + 1}: {group.upper()}")
#        if group == "static":
#            for scount, sgroup in enumerate(['split', 'join']):
#                LOGGER.info(f"START TEST SUBGROUP {gcount + 1}.{scount}: {group.upper()}.{sgroup.upper()}")
#                for count, case in enumerate(data[group]):
#                    transformation = encryption.Algorithm(case['transformation'])
#                    LOGGER.info(f"START TEST CASE {gcount + 1}.{scount}.{count}: "
#                                f"{group.upper()}.{sgroup.upper()}.{transformation.to_string().upper()}")
#
#                    try:
#                        if sgroup == "split":
#                            mnemonic = case['mnemonic_o']
#                            exp_mnemonic = case['mnemonic_1'], case['mnemonic_2']
#                            obt_mnemonic = tuple(split(mnemonic, transformation))
#                            for ordinal in range(2):
#                                assert " ".join(obt_mnemonic[ordinal]) == exp_mnemonic[ordinal], \
#                                    f"invalid mnemonic {ordinal+1}{sep}" \
#                                    f"expected: '{exp_mnemonic[ordinal]}'{sep}" \
#                                    f"obtained: '{' '.join(obt_mnemonic[ordinal])}'"
#                        else:
#                            mnemonic = case['mnemonic_1'], case['mnemonic_2']
#                            exp_mnemonic = case['mnemonic_o']
#                            obt_mnemonic = join(*mnemonic, transformation)
#                            assert " ".join(obt_mnemonic) == exp_mnemonic, \
#                                f"invalid mnemonic{sep}" \
#                                f"expected: '{exp_mnemonic}'{sep}" \
#                                f"obtained: '{' '.join(obt_mnemonic[ordinal])}'"
#                    except Exception as e:
#                        LOGGER.error(" | ".join(str(e).split(sep)))
#                        failed.append(f"{gcount + 1}.{scount}.{count}")
#                        raise e
#                    finally:
#                        LOGGER.info(f"STOP TEST CASE {gcount + 1}.{scount}.{count}: "
#                                    f"{group.upper()}.{sgroup.upper()}.{transformation.to_string().upper()}")
#
#                LOGGER.info(f"STOP  TEST SUBGROUP {gcount + 1}.{scount}: {group.upper()}.{sgroup.upper()}")
#        elif group == "dynamic" and data[group]:
#            for count, transformation in enumerate(encryption.Algorithm):
#                LOGGER.info(f"START TEST CASE {gcount + 1}.{count}: {transformation.to_string().upper()}")
#                try:
#                    exp_mnemonic = tuple(Seed.from_entropy(BetterEntropy.generate()).mnemonic)
#                    print(exp_mnemonic)
#                    obt_mnemonic = tuple(split(exp_mnemonic, transformation))
#                    obt_mnemonic = join(*obt_mnemonic, transformation)
#
#                    assert obt_mnemonic == exp_mnemonic, \
#                        f"invalid mnemonic{sep}" \
#                        f"expected: '{' '.join(exp_mnemonic)}'{sep}" \
#                        f"obtained: '{' '.join(obt_mnemonic)}'"
#
#                except Exception as e:
#                    LOGGER.error(" | ".join(str(e).split(sep)))
#                    failed.append(f"{gcount + 1}.{scount}.{count}")
#                    raise  e
#                finally:
#                    LOGGER.info(f"STOP  TEST CASE {gcount + 1}.{count}: {transformation.to_string().upper()}")
#
#        LOGGER.info(f"STOP  TEST GROUP {gcount + 1}: {group.upper()}\n\n")
#
#    LOGGER.info(
#        f"OVERALL RESULT: {'FAILED' if failed else 'SUCCESS'}"
#    )
#    if failed:
#        LOGGER.info(f"TESTS FAILED: {', '.join(failed)}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')
    test_mnemonic_masking()
