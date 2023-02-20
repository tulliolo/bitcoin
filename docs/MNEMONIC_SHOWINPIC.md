# Mnemonic ShowInPic

Uses steganography to reveal a mnemonic hidden in an image file by the [Mnemonic HideInPic](MNEMONIC_HIDEINPIC.md) tool.

After being extracted from the image, the mnemonic can be decrypted with the following algorithms:

| ALGORITHM      | DESCRIPTION                                                                              |
|----------------|------------------------------------------------------------------------------------------|
| NONE (DEFAULT) | No decryption                                                                            |
| NEGATIVE       | Each bit is switched, like in a negative                                                 |
| REVERSAL       | All bits are swapped, the less significant bit becomes the most significant and so on... |
| PASSWORD       | The mnemonic is decoded with a password                                                  |

The pixels to be processed can be selected reading the image in different directions:

| DIRECTION            | DESCRIPTION                            |
|----------------------|----------------------------------------|
| HORIZONTAL (DEFAULT) | from LEFT to RIGHT, from TOP to BOTTOM |
| VERTICAL             | from TOP to BOTTOM, from LEFT to RIGHT |
| REVERSE_HORIZONTAL   | from RIGHT to LEFT, from BOTTOM to TOP |
| REVERSE_VERTICAL     | from BOTTOM to TOP, from RIGHT to LEFT |

## Usage and Syntax
For production use, this tool is intended to run on an offline computer, with internet connection down.

```
$ python mnemonic_showinpic.py -h
usage: mnemonic_showinpic.py [-h] [-e ENCRYPTION] [-d DIRECTION] -i INPUT_FILE

Show a mnemonic hidden in an image with steganography.

options:
  -h, --help            show this help message and exit
  -e ENCRYPTION, --encryption ENCRYPTION
                        decrypt the mnemonic with different algorithms
                        supported algorithms are:
                        0) NONE (DEFAULT): no decryption applied
                        1) NEGATIVE: invert all bits
                        2) REVERSAL: swap all bits
                        3) PASSWORD: decrypt with a password
  -d DIRECTION, --direction DIRECTION
                        traverse the image in different directions
                        supported directions are:
                        0) HORIZONTAL (DEFAULT)
                        1) VERTICAL
                        2) REVERSE_HORIZONTAL
                        3) REVERSE_VERTICAL
  -i INPUT_FILE, --input-file INPUT_FILE
                        input image file
```

## Usage Examples

Reveal a mnemonic hidden in a picture in HORIZONTAL direction with NONE encryption

```
$ python mnemonic_showinpic.py -i ./tests/output/test_image_00.png 
************************
** mnemonic_showinpic **
************************
Show a mnemonic hidden in an image with steganography.

nothing to do

found message in picture:
candy ancient remember pizza earth canal dragon ginger ocean nation debris wheel robust hood error brass coach defense gold reunion voice sting check mistake
```

Reveal a mnemonic hidden in a picture in VERTICAL direction with PASSWORD encryption

```
$ python mnemonic_showinpic.py -e 3 -d 1 -i ./tests/output/test_image_31.png 
************************
** mnemonic_showinpic **
************************
Show a mnemonic hidden in an image with steganography.


insert a password:
password > 
insert again.....:
password > 

found message in picture:
hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length
```
