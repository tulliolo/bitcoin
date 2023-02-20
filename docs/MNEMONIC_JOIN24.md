# Mnemonic FixSum

Joins the two 12 words bip39 mnemonics created by the [Mnemonic Split24](MNEMONIC_JOIN24.md) tool into the original 24 words bip39 mnemonic.

## Usage and Syntax
For production use, this tool is intended to run on an offline computer, with internet connection down.

```
 $ python mnemonic_join24.py -h
 usage: mnemonic_join24.py [-h] [-d DECRYPTION]
 
 options:
   -h, --help            show this help message and exit
   -d DECRYPTION, --decryption DECRYPTION
                         Decrypt the original entropy with different algorithms.
                         N.B.: the algorithm must be the same previously used to encrypt!Supported algorithms are:
                         0) NONE: no decryption needed (DEFAULT)
                         1) NEGATIVE: invert all bits
                         2) REVERSAL: swap all bits
```

## Usage Examples

Rebuild mnemonic with no decryption

```
 $ python mnemonic_join24.py
 *********************
 ** mnemonic_join24 **
 *********************
 Rebuild the original 24 words bip39 mnemonic, from two 12 words mnemonics used for plausible deniability.
 
 insert the first 12 words bip39 mnemonic:
 mnemonic l > urge plastic snap bind enable link weather brush dish job drink negative
 insert the second 12 words bip39 mnemonic:
 mnemonic r > identify defense oxygen upgrade sick amount jeans science ring assault submit grunt
 nothing to do
 
 Generating the original 24 words mnemonic:
 urge plastic snap bind enable link weather brush dish job drink napkin anchor now total twist lab liberty knee author parade super liar high
```

Rebuild mnemonic with NEGATIVE decryption

```
 $ python mnemonic_join24.py -d 1
 *********************
 ** mnemonic_join24 **
 *********************
 Rebuild the original 24 words bip39 mnemonic, from two 12 words mnemonics used for plausible deniability.
 
 insert the first 12 words bip39 mnemonic:
 mnemonic l > nuclear seek feel romance swarm ship feel invest crucial broken essence trap
 insert the second 12 words bip39 mnemonic:
 mnemonic r > defense member meadow must guide despair treat ice drum flee erase all
 
 Generating the original 24 words mnemonic:
 hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length
```

Rebuild mnemonic with REVERSAL decryption

```
 $ python mnemonic_join24.py -d 2
 *********************
 ** mnemonic_join24 **
 *********************
 Rebuild the original 24 words bip39 mnemonic, from two 12 words mnemonics used for plausible deniability.
 
 insert the first 12 words bip39 mnemonic:
 mnemonic l > dinosaur open slide kit toast cradle maple crop hold tag fox sick
 insert the second 12 words bip39 mnemonic:
 mnemonic r > course option mobile plastic permit program debate end early profit junk coast
 
 Generating the original 24 words mnemonic:
 hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length
```
