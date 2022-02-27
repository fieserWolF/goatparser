# Goatparser

Goatparser parses C64 Goattracker source files.
As of now, this is a commandline-tool.
It might become a good starting point for own SID-player routines.
You could easily create your song in Goattracker and then export it to a new format of your choice.

It runs on 64 bit versions of Linux, MacOS, Windows and other systems supported by Python. 


# Why goatparser?

reason | description
---|---
open source | easy to modify and to improve, any useful contribution is highly welcome
portable | available on Linux, MacOS, Windows and any other system supported by Python3
simple | easy to use


# Usage

    goatparser v1.00 [10.07.2021] *** by fieserWolF
    usage: goatparser.py [-h] [-o OUTPUT_FILE] input_file

    This program parses C64 Goattracker source files.

    positional arguments:
      input_file            goattracker .sng input file

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT_FILE, --output OUTPUT_FILE
                            text output filename

    Example: ./goatparser.py song.sng


Have a good look in /doc.


# Author

* fieserWolF/Abyss-Connection - *code* - [https://github.com/fieserWolF](https://github.com/fieserWolF) [https://csdb.dk/scener/?id=3623](https://csdb.dk/scener/?id=3623)


# Getting Started

Clone the git-repository to your computer:
```
git clone https://github.com/fieserWolF/goatparser.git
```

Start the python script:
```
python3 goatparser.py --help
```



## Prerequisites

At least this is needed to run the script directly:

- python 3
- argparse

Normally, you would use pip like this:
```
pip3 install argparse
```

On my Debian GNU/Linux machine I use apt-get to install everything needed:
```
apt-get update
apt-get install python3 python3-argh
```
# Changelog

## Future plans

- maybe: implement other exports

Any help and support in any form is highly appreciated.

If you have a feature request, a bug report or if you want to offer help, please, contact me:

[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)


## Changes in 1.00

- initial release

# License

_goatparser program parses C64 Goattracker source files._

_Copyright (C) 2022 fieserWolF / Abyss-Connection_

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

See the [LICENSE](LICENSE) file for details.

For further questions, please contact me at
[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)

For Python3 and other used source licenses see file [LICENSE_OTHERS](LICENSE_OTHERS).


