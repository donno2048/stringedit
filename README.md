# stringedit

Replace strings in binary files.

## Installation

### From PyPI

```sh
pip3 install stringedit
```

### From GitHub

```sh
pip3 install git+https://github.com/donno2048/stringedit
```
## Usage

To run the string editing use `stringed` or `python3 -m stringedit`

```sh
$ stringed -h
usage: stringed [-h] [-n [number]] [-m {l,r,L}] filename

Replace strings in binary files

positional arguments:
  filename              input filename

optional arguments:
  -h, --help            show this help message and exit
  -n [number], --bytes [number]
                        print amy string of at least [number] characters (default 4)
  -m {l,r,L}, --method {l,r,L}
                        method used to widen replacement string if it's too long l - pad with
                        spaces from the left r - pad with spaces from the right L - leave
                        everything after the replacement as it was
```

You can also use the `stringpr` to print all the strings, similar to the `strings` linux command.

```sh
$ stringpr -h
usage: stringpr [-h] [-n [number]] [-t {o,d,x}] [-s <string>] filename

Print strings in binary files

positional arguments:
  filename              input filename

optional arguments:
  -h, --help            show this help message and exit
  -n [number], --bytes [number]
                        print amy string of at least [number] characters (default 4)
  -t {o,d,x}, --radix {o,d,x}
                        print the location of the string in base 8, 10 or 16
  -s <string>, --output-separator <string>
                        string used to separate strings in output
```

## Uses

- Could be used to create a modded version for a game by changing dialogues and such
- Could theoretically be used to "steal" someones binary by just replacing any info (e.g. license) with the attacker's - removes the need to decompile, change and then recompile the binary
- And more
