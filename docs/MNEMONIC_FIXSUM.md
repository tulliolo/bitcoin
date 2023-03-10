# Mnemonic FixSum

Modifies a mnemonic 'manually' generated, e.g. by rolling dices.
In particular, the last word will be modified to match the checksum, to make the resulting mnemonic bip39 compliant.

## Usage and Syntax
For production use, this tool is intended to run on an offline computer, with internet connection down.

```
 Usage: python mnemonic_fixsum.py
```

## Usage Examples

```
 $ python3 mnemonic_fixsum.py 
 *********************
 ** mnemonic_fixsum **
 *********************
 Insert a 'candidate' mnemonic, e.g. generated by dices.
 The tool will modify the last word, matching a valid bip39 checksum.
 
 insert a candidate bip39 mnemonic:
 mnemonic > letter advice cage absurd amount doctor acoustic avoid letter advice cage about
 
 a valid bip39 mnemonic is:
 letter advice cage absurd amount doctor acoustic avoid letter advice cage above
```
