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
import os.path
import getpass

from PIL import Image

from generator.entropy import BetterEntropy
from generator.seed import Seed
from utils import encryption, steganography


def __print_header():
    print(
        "************************\n"
        "** mnemonic_hideinpic **\n"
        "************************\n"
        "Hide a mnemonic into an image with steganography.\n"
    )


def __mnemonic_hideinpic(args=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Hide a mnemonic into an image with steganography."
    )
    parser.add_argument(
        "-g", "--generate", action="store_true", default=False,
        help="generate a new 24 words mnemonic (default = False)"
    )
    parser.add_argument(
        "-e", "--encryption", action="store", default="0",
        help="encrypt the mnemonic with different algorithms (default = NONE)\n"
             "supported algorithms are:\n"
             "0) NONE: no encryption applied (DEFAULT)\n"
             "1) NEGATIVE: invert all bits\n"
             "2) REVERSAL: swap all bits\n"
             "3) PASSWORD: protect with a password")
    parser.add_argument(
        "-d", "--direction", action="store", default="0",
        help="traverse the image in different directions\n"
             "supported directions are:\n"
             "0) HORIZONTAL (DEFAULT)\n"
             "1) VERTICAL\n"
             "2) REVERSE_HORIZONTAL\n"
             "3) REVERSE_VERTICAL")
    parser.add_argument(
        "-i", "--input-file", action="store", required=True,
        help="input image file"
    )
    parser.add_argument(
        "-o", "--output-path", action="store", required=True,
        help="output image path"
    )
    options = parser.parse_args(args)

    __print_header()

    try:
        if not os.path.isdir(options.output_path):
            raise ValueError(f"invalid output path '{options.output_path}'")

        if not (options.encryption.isnumeric() and int(options.encryption) in range(len(encryption.Algorithm))):
            raise ValueError(f"invalid encryption\n\t"
                             f"expected: 0-{len(encryption.Algorithm)}\n\t"
                             f"obtained: {options.encryption}")

        if not (options.direction.isnumeric() and int(options.direction) in range(len(encryption.Direction))):
            raise ValueError(f"invalid direction\n\t"
                             f"expected: 0-{len(encryption.Direction)}\n\t"
                             f"obtained: {options.direction}")

        if options.generate:
            mnemonic = ' '.join(Seed.from_entropy(BetterEntropy.generate()).mnemonic)
            print("generating a new 24 words mnemonic:")
            print(mnemonic)
        else:
            print("insert your mnemonic:")
            mnemonic = ' '.join(Seed.from_mnemonic(input("mnemonic > ")).mnemonic)

        algorithm = encryption.Algorithm(int(options.encryption))
        direction = encryption.Direction(int(options.direction))
        password = None
        if algorithm == encryption.Algorithm.PASSWORD:
            print("\ninsert a password:")
            password = getpass.getpass(prompt='password > ')
            print("insert again.....:")
            if password != getpass.getpass(prompt='password > '):
                raise ValueError("password did not match!")

        with Image.open(options.input_file, mode='r') as input_image:
            input_image_name = options.input_file.split('/')[-1].split('.')[0]

            output_file = options.output_path + "/" + input_image_name + "_" + \
                          options.encryption + options.direction + ".png"

            output_image = steganography.encode(mnemonic, input_image, algorithm, direction, password)
            output_image.save(output_file)

    except Exception as e:
        print(e)
        print()
        parser.print_usage()
        exit(-1)


if __name__ == "__main__":
    __mnemonic_hideinpic()
