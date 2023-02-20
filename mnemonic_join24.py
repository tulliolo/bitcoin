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
import argparse
import sys

from utils import encryption, mnemonic


def __print_header():
    print(
        "*********************\n"
        "** mnemonic_join24 **\n"
        "*********************\n"
        "Rebuild the original 24 words bip39 mnemonic, from two 12 words mnemonics used for plausible deniability.\n"
    )


def __mnemonic_join24(args=None):
    if args is None:
        args = sys.argv[1:]
        
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Rebuild the original 24 words bip39 mnemonic, "
                    "from two 12 words mnemonics used for plausible deniability."
    )
    parser.add_argument(
        "-d", "--decryption", action="store", default="0",
        help="Decrypt the original entropy with different algorithms.\n"
             "N.B.: the algorithm must be the same previously used to encrypt!"
             "Supported algorithms are:\n"
             "0) NONE: no decryption needed (DEFAULT)\n"
             "1) NEGATIVE: invert all bits\n"
             "2) REVERSAL: swap all bits")
    options = parser.parse_args(args)

    __print_header()

    try:
        if not options.decryption.isnumeric() or not int(options.decryption) in range(3):
            raise ValueError("invalid decryption algorithm:\n\t"
                             "expected: 0-2\n\t"
                             f"obtained: '{options.decryption}'")

        print("insert the first 12 words bip39 mnemonic:")
        mnemonic_l = input("mnemonic l > ").strip().split()
        print("insert the second 12 words bip39 mnemonic:")
        mnemonic_r = input("mnemonic r > ").strip().split()

        print(
            "\nGenerating the original 24 words mnemonic:\n"
            f"{' '.join(mnemonic.join(mnemonic_l, mnemonic_r, encryption.Algorithm(int(options.decryption))))}"
        )

    except Exception as e:
        print(e)
        exit(-1)


if __name__ == "__main__":
    __mnemonic_join24()
