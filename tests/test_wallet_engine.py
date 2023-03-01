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

from wallet import engine, version

LOGGER = logging.getLogger(__name__)


def test_wallet_engine():
    with open("test_wallet_engine.json", "r") as file:
        data = json.load(file)

        failed = []
        gcount = 1
        tcount = 0

        LOGGER.info(f"START TEST {gcount}: VECTOR")
        for scount, test in enumerate(data["vector"]):
            LOGGER.info(f"START TEST {gcount}.{scount}")
            try:
                master = engine.Node.from_seed(
                    bytes.fromhex(test["seed"]),
                    version.NetworkId.MAINNET, version.AddressType.P2SH
                )
                LOGGER.info(f"master prvkey = {master.xprvkey}")
                LOGGER.info(f"master pubkey = {master.xpubkey}")

                for count, case in enumerate(test["flow"]):
                    LOGGER.info(f"START TEST {gcount}.{scount}.{count}")
                    try:
                        path = case["path"]
                        xprvkey = case["prvkey"]
                        xpupkey = case["pubkey"]
                        if path == "m":
                            assert master.xprvkey == xprvkey, \
                                "prvkey mismatch!\n\t" \
                                f"expected: {master.xprvkey}\n\t" \
                                f"obtained: {xprvkey}"

                            assert master.xpubkey == xpupkey, \
                                "pubkey mismatch!\n\t" \
                                f"expected: {master.xpubkey}\n\t" \
                                f"obtained: {xpupkey}"

                    except Exception as e:
                        msg = ' | '.join(str(e).split("\n\t"))
                        LOGGER.error(msg)
                        failed.append(f"{gcount}.{scount}.{count}")
                    finally:
                        tcount += 1
                        LOGGER.info(f"STOP  TEST {gcount}.{scount}.{count}")

            except Exception as e:
                msg = ' | '.join(str(e).split("\n\t"))
                LOGGER.error(msg)
                failed.append(f"{gcount}.{scount}")
                tcount += 1
            finally:
                LOGGER.info(f"STOP  TEST {gcount}.{scount}")
        LOGGER.info(f"STOP  TEST {gcount}: VECTOR\n")
        gcount += 1

        LOGGER.info("***********")
        LOGGER.info("** RECAP **")
        LOGGER.info("***********")
        LOGGER.info(f"TOTAL TESTS: {tcount}")
        LOGGER.info(f"OK TESTS: {(tcount - len(failed)):2}/{tcount}")
        LOGGER.info(f"KO TESTS: {len(failed):2}/{tcount}\n")

        if failed:
            LOGGER.error(f"FAILED TESTS: {', '.join(failed)}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')
    test_wallet_engine()
