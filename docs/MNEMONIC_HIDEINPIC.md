# Mnemonic HideInPic

Uses steganography to hide a mnemonic in an image file.

Before to be written into the image, the mnemonic can be encrypted with the following algorithms:

| ALGORITHM      | DESCRIPTION                                                                              |
|----------------|------------------------------------------------------------------------------------------|
| NONE (DEFAULT) | No encryption                                                                            |
| NEGATIVE       | Each bit is switched, like in a negative                                                 |
| REVERSAL       | All bits are swapped, the less significant bit becomes the most significant and so on... |
| PASSWORD       | The mnemonic is encoded with a password                                                  |

The pixels to be modified can be selected reading the image in different directions:

| DIRECTION            | DESCRIPTION                            |
|----------------------|----------------------------------------|
| HORIZONTAL (DEFAULT) | from LEFT to RIGHT, from TOP to BOTTOM |
| VERTICAL             | from TOP to BOTTOM, from LEFT to RIGHT |
| REVERSE_HORIZONTAL   | from RIGHT to LEFT, from BOTTOM to TOP |
| REVERSE_VERTICAL     | from BOTTOM to TOP, from RIGHT to LEFT |

In order to rebuild the original mnemonic, take note of the encryption algorithm and direction.

## Usage and Syntax
For production use, this tool is intended to run on an offline computer, with internet connection down.

```
$ python mnemonic_hideinpic.py -h
usage: mnemonic_hideinpic.py [-h] [-g] [-e ENCRYPTION] [-d DIRECTION] -i INPUT_FILE -o OUTPUT_PATH

options:
  -h, --help            show this help message and exit
  -g, --generate        generate a new 24 words mnemonic (default = False)
  -e ENCRYPTION, --encryption ENCRYPTION
                        encrypt the mnemonic with different algorithms
                        supported algorithms are:
                        0) NONE (DEFAULT): no encryption applied
                        1) NEGATIVE: invert all bits
                        2) REVERSAL: swap all bits
                        3) PASSWORD: protect with a password
  -d DIRECTION, --direction DIRECTION
                        traverse the image in different directions
                        supported directions are:
                        0) HORIZONTAL (DEFAULT)
                        1) VERTICAL
                        2) REVERSE_HORIZONTAL
                        3) REVERSE_VERTICAL
  -i INPUT_FILE, --input-file INPUT_FILE
                        input image file
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        output image path
```

## Usage Examples

Generate a new mnemonic and hide it into a picture in HORIZONTAL direction with NONE encryption

```
$ python mnemonic_hideinpic.py -g -i ./tests/input/test_image.jpg -o ./tests/output/
************************
** mnemonic_hideinpic **
************************
Hide a mnemonic into an image with steganography.

generating a new 24 words mnemonic:
candy ancient remember pizza earth canal dragon ginger ocean nation debris wheel robust hood error brass coach defense gold reunion voice sting check mistake
```

Insert a mnemonic and hide it into a picture in VERTICAL direction with PASSWORD encryption

```
$ python mnemonic_hideinpic.py -e 3 -d 1 -i ./tests/input/test_image.jpg -o ./tests/output/
************************
** mnemonic_hideinpic **
************************
Hide a mnemonic into an image with steganography.

insert your mnemonic:
mnemonic > hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length

insert a password:
password > 
insert again.....:
password >
```
