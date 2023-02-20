# Mnemonic FixSum

Splits a 24 words bip39 mnemonic into two 12 words bip39 mnemonics.
The resulting 12 words mnemonics are bip39 compliant and could be used for plausible deniability.
In order to rebuild the original mnemonic, take note of the split mnemonic and the encryption algorithm.

## Usage and Syntax
For production use, this tool is intended to run on an offline computer, with internet connection down.

```
 $ python mnemonic_split24.py -h
 usage: mnemonic_split24.py [-h] [-g] [-e ENCRYPTION]
 
 options:
   -h, --help            show this help message and exit
   -g, --generate        generate a new 24 words mnemonic (default = False)
   -e ENCRYPTION, --encryption ENCRYPTION
                         encrypt the original entropy with different algorithms (enhance original seed obfuscation)
                         supported algorithms are:
                         0) NONE: no encryption applied (DEFAULT)
                         1) NEGATIVE: invert all bits
                         2) REVERSAL: swap all bits
```

## Usage Examples

Generate mnemonic and split with no encryption

```
 $ python mnemonic_split24.py -g
 **********************
 ** mnemonic_split24 **
 **********************
 Splits a 24 words bip39 mnemonic into two 12 words bip39 mnemonics, useful for plausible deniability.
 
 generating a 24 words mnemonic:
 urge plastic snap bind enable link weather brush dish job drink napkin anchor now total twist lab liberty knee author parade super liar high
 
 Generating two 12 words mnemonics for plausible deniability.
 Please, take note of these mnemonics, together with the obfuscation algoritm, in order to rebuild the original 24 words mnemonic:
 nothing to do
 mnemonic l: urge plastic snap bind enable link weather brush dish job drink negative
 mnemonic r: identify defense oxygen upgrade sick amount jeans science ring assault submit grunt
```

Insert mnemonic and split with NEGATIVE encryption

```
 $ python mnemonic_split24.py -e 1
 **********************
 ** mnemonic_split24 **
 **********************
 Splits a 24 words bip39 mnemonic into two 12 words bip39 mnemonics, useful for plausible deniability.
 
 insert a valid 24 words bip39 mnemonic:
 mnemonic > hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length
 
 Generating two 12 words mnemonics for plausible deniability.
 Please, take note of these mnemonics, together with the encryption algoritm, in order to rebuild the original 24 words mnemonic:
 mnemonic l: nuclear seek feel romance swarm ship feel invest crucial broken essence trap
 mnemonic r: defense member meadow must guide despair treat ice drum flee erase all
```

Insert mnemonic and split with REVERSAL encryption

```
 $ python mnemonic_split24.py -e 2
 **********************
 ** mnemonic_split24 **
 **********************
 Splits a 24 words bip39 mnemonic into two 12 words bip39 mnemonics, useful for plausible deniability.
 
 insert a valid 24 words bip39 mnemonic:
 mnemonic > hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length
 
 Generating two 12 words mnemonics for plausible deniability.
 Please, take note of these mnemonics, together with the encryption algoritm, in order to rebuild the original 24 words mnemonic:
 mnemonic l: dinosaur open slide kit toast cradle maple crop hold tag fox sick
 mnemonic r: course option mobile plastic permit program debate end early profit junk coast
```
