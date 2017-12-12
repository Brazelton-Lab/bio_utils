#! /usr/bin/env python

"""Test bio_utils' binary_guesser

Copyright:

    test_binary_guesser.py test bio_utils' binary_guesser
    Copyright (C) 2015  William Brazelton, Alex Hyer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from bio_utils.verifiers import binary_guesser
from bio_utils.verifiers import FormatError
from tempfile import NamedTemporaryFile

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Production'
__version__ = '2.0.0'


def test_binary_guesser():
    """Test bio_utils' binary_guesser with binary and text data"""

    # Store data
    binary_data = b'\x8e\xd2\x837U\xbc\\!H\xc8\xb1O\xac\x9e\xbf\xd4b\x82\xc9' \
                  b'\xd7\xaa\xb9\x16Uo5m\r\x00\x1e\xdd\x978\x00Rj\xe2Ng\xc3' \
                  b'=\xe6N}\x92\xf0(+\xa3\x99\\w\xe0\xa6\xb4\xa4\xc2\x90\x81' \
                  b'\xc4@\x10\x0f_\xdf\xdeo\r\xdc\xcd<\x7fq\x87\xb4\n\xcd' \
                  b'\xd2\r=\xfb\x84\xfb\xa5\xc0\x9e\xb4wl6j\xa9\xae\xe5\xc1' \
                  b'\xfb^\\L\xc8\x0b\xd1fU\xd1\xdd]\x06\x19\xf7\xc6\x90?x' \
                  b'\x06\x8ab\x0b\x14\xa4\x00z\x83\xe8\x90\x16@U\xba~\xbb' \
                  b'\xcf\x90\xb2\xdb>^A\xd1\xd45\xd7\xbc\x99\xf26\xf4\xa0' \
                  b'\x8f-\x04)\xf9[\x7f\xca\x81\xcd\x04\xefd\x9ci\xe8lH' \
                  b'\xce\xb8\xe6R\xe4#\xb5\x16\x97a\xd2\xda2\x1d\x9d\xb1#1 ' \
                  b'\xe1u\x04g2\xe4\xf0B\xa6\xcd\x00q\x9d=N\x1f\xf1%\xa6' \
                  b'\x89\xc2\xb4j\xeb\x90\x07>kJ\xefi\xd2tp\xb0\xf1\xb7' \
                  b'\xbb\xc8\xa8cZ\x0c\x88\xe2\x08\x0b\x05\xddS\x86\xa4s' \
                  b'\x1ck\x90\xa3\t(\x03n\xe8S\x8a\x03\xe3*\xb4\x02\x06%' \
                  b'\xfe2.?&\x13\x94\xea7\xd1\xb9\xef\xe1\x94Y\xbd58\xf4Y' \
                  b'\x13\xe9r\x90\x84\x0e{\xe2\x98\x12\xff\xf4f\x87J\xfc:' \
                  b'\xd7\xd9\xc6\xbf\xd3IU\xf5\\\xa1\xb0\xad\x04#\x9c\x0c' \
                  b'\x1d\x90\xbb\x93\xee\xbb\r\xa7\x96\t\x8b\xc1\x91\xecl' \
                  b'\xe1\x0f~3@\xa7\x98\re\x9b\x8fy\xb8U\x18\x04z\xe8\rT?' \
                  b'\xed\xb0\n\xf7*\xc8\xce\xb5N8\xaeh\x06\x84\'\xdd6SI' \
                  b'\xd6\xf9\xbdz\xd3\xab\xe3\xd9\xb3*BBd\xc0\x9d\xd6\x8a' \
                  b'\xb1\xe8\xc4\xb9\xacw|>\x80y\x86\xfcM!\x1b\xc9\xff\x93' \
                  b'\x8d\xb5\x89IL\x93J\x88\x0b\xe5\'\xbd\x13\xa9\xd5\xa0' \
                  b'\xe9Rs\xce,\x8e%\xdbQ\x85##I\x93\x04\xec\x98V\x8d\x9b' \
                  b'\xd9B9?z\'>Aq\x10`&\x0e\xa1\xb2\x94\x0c}"QI\x82\xf5.O' \
                  b'\x9a:uu|\xdd\x86^\xfd\x0bu\xbf05\xea\\e\xc7\\\xbe\xd9' \
                  b'\x98\x0fFo9\xb1\n`\xe9\x8ccg\n\x13\xcb\x1b!\xb2\xcdt|' \
                  b'\xc7!\xfawn3\xf0p\xb1n\xb6^\xe1;S\xa0\xf3y.\x8e\x83{' \
                  b'\x9f\x03\xa1\xfe\x8b\xae\xd4\xfa\xafh\xefP\x8c\xa0\xc1' \
                  b'\x8dWW\x85\xa0\xfeT\xa8\xa3\xe1\x85\x11G\x0f5\x83\xec' \
                  b'\xebvJ\x1a(\xbdk\x8c\xbbf\x81\x1d\xc0\x91[\x1c\x9d\xa4' \
                  b'\x0c\x81\xfe\x94-\xd9\xa0\xd3\x0c\xe0~\r\x8eZ\xc91>\xac' \
                  b'\x935\x94H\xfeN\x02\t\xe5\xb15X3\xcb3n\xec\x82\xbcl\x05' \
                  b'\xa7\x07X\xc6\x1a`\x1b\xd3\x85\x0c<c\x81K$\xb9#\x12h' \
                  b'\xa9gN\xce\x8f:\x0e\xe1r\xf2K\xc1\x05\xa5J6\x12\xf8\xd7' \
                  b'\xce\xcb@\xea\xb3\x0c]\x89\xe3\x9b)\xcd\x11\x06\x9bH4\n' \
                  b'\xad\xbd\xdb\x80U\r\x9e\xf6h$;Gov\xb3\x03\x88a\x81.MA' \
                  b'\x99\xc2\xc2Q\x1c=3c#)\xfb\xc1\x10f<xI\xef\xb2\xdcP' \
                  b'\xd9P\x1d\xc68\xec#-\xbd\xf2\x8c\x16a\xaa\x1a\xb6qb\x15' \
                  b'\xa8\xcct\xb8e\xc9\xbb\xd6S\x01 U\xcfw\xbd\xc0\xab\xb3l' \
                  b'\x1d\xd2\xa6k\x04\x06G_\x0e\x9bjam\xb4\xc4-\xcf\xad\x07c' \
                  b'\xf9"N\x8c\xe3r.\x0cq\xe2\x8c\x99\xd5\xa9\xfc\xbevRW7' \
                  b'\x17y\xfd\xbf\x9bq\t\x92\x1d\xc9\x19E\xd5\xedJ\xea9\xa4' \
                  b'\xd26~\xcc\x12\x9b\x12\xc4\x96(\xbe\xd7\x05-\xc9\x9f\x02' \
                  b'\xe2\x08f\xaf\'J\x0c\xb1\xcd\xa6\x80k)s\xa8\xbe\x15\x9d' \
                  b'\r}P2\xa1u\r~T\xedq\xa1X3o\x0b\xcb\x9dN\x8dAME\xe9\xcb\n' \
                  b'\xc6 ,\n\xa3\xba\x9a\x15\xc5-\xbaW\x89y?\xe3\x16 T!\xf0' \
                  b'\xf5\xfd\xa3Ks3\xb7\xe9F#\xdd\xebQ\xa9+#\xf9WG\x05\x93' \
                  b'\x93\x9a\x127\xf7d\xf2\x1cx\x9a2\x0fB\xber*\xc4\x90\xf8' \
                  b'\x07\xd7#\xf4\xff\xc0\xdcF\xd7<d\xb0\xdb\xcf\xa1\x1e' \
                  b'\xd2\x98\xde\xd1=u\xa6\xc4\x81\xf0\x04#x\xb6\xde\x0e\xbe' \
                  b'\xc6\x1b:\x10\x8f\xdf\xa3\x99E\xa2\xc2W\xde\xa7\x03\xe6x' \
                  b'\xc3\x07\x9d\xf1\x01$\x1d\xa1L\xad\xe8bnI\x14\xe7\xc1,'

    text_data = 'BGwrYz3oUOoys8NJQN0Ju43r28l/bdXne8YbOZWiPMMoZFyxp9Qmc4NK6k' \
                'Bs/DA2ZougW3RVZGAs\n3RRPLU78oRpTH3jzSViqj0jEtpMIwpOofhDjyP' \
                '8bM7/bHWIa9XruomgdnOxkttqMc/Mxj6ZcODlv\nGADtY86z+/VdfO9lDj' \
                'nwYmkkvjPN3qxpy6LIx9ZPMKpwCzTheidJR95u6gG+1ofA5HYaLIReujUn' \
                '\ntvtZKu49pmiEuz5tT0VWRPHR/7q2Eg5u7SZAhlWtOW+G/P7QkLFButy8' \
                'sArJwCBtEl6DH7B+L570\nZxfBaF1yaFU7VmZNL3e6MIq2Lgkk6TU3Ezvy' \
                'LMB1ZLt8Zpst4tL814fMmJ6QazUaafG73YQkmoVg\nGdbemZBu3CLxJ3iX' \
                'i9NPZxDionF9yNAt7gdiGqrVC3lRJIgSF1wn5/jqsdv8OhBI98DWOOYGmv' \
                'EJ\nM+DztfOx4KQpA4TSunCRK/2H6POolGN1gOXbteUZY4cA2FreVW15QG' \
                '/an30epRiKH/cgeNdEuIIe\niFsWt62tFTxXaQZZbc/p/hwUJ7iSMeYpq7' \
                'WgYmJQmkdHggKFFZniuI5VyE1YHqVu1bZEhLaI3XSJ\npGF9dvGRCamzGO' \
                'xLnz7TsjbVM45maSPXGJVw5OgZrZhqPdZNKgplblL8xvg//lRF582cYQFy' \
                'yM8X\nOGqN83/QKo02FwEdqGg6DD5zzbLys4K/HjYguARUHLMBziFCvq2x' \
                '9z31pSJUUCaBVit0Z4S4cCiK\narptw/91PnBJCdchBk0T62Kt4E41ClWV' \
                'OUWZcLKWVhW689HLrvO4YCBi+qZDtTJFK1cmahAh9xZj\n1KmfvZzM6QFB' \
                'RTtH2qzvEsgiA6lu9u1HS8ohHFxEYDJ32XKoNSQtarfOpjw/sA3kUaBi5a' \
                '1Josah\nXDyGoXSXdtVq2wdZLLf7uuwbTUZae6j+bl5R7dYTkKzhsaVmpU' \
                'zkrCHjl7XB+9YfpNwiCYPIfZSQ\nNluAEf2OeGozMipZ47fh9PMvWHri3g' \
                '8pA/7B9Nn8K3mSmEDLBBZgkcKynR6rtSgzj2hIX0qS0/iX\nihk5ZjvZiu' \
                'tqPiix6j+SSl59jk2WERh1IVHHWtBJUknbTlV3reTL+aWZHfkUioA0RSRi' \
                'cwBTY6ou\nnypnq8l4mPTWUCZReDz7N5OEGWquroD8Fv4+IB5EviVI6Xrj' \
                'Yil8m0rIjtbmwgFK0kSvkTEUI0DD\nCH3TY/+tXgLWA6scXG46T9+deuM0' \
                'F7H/+4iRfnLV1LMV8J+roIFcg3VPX1yBW4wryXNdERVNhbTk\nI/9c17pC' \
                '8fWqhv8kLBvcZcbzn6XDkKWXcQ6VOwiopYw/b6HaPDR7zSeBhNoPPJEw5q' \
                'q6ZSs2eA==\n'

    binary_handle = NamedTemporaryFile(mode='wb+')
    binary_handle.write(binary_data)
    binary_handle.seek(0)

    binary_guesser(binary_handle)
    assert binary_handle.tell() == 0

    text_handle = NamedTemporaryFile(mode='wt+')
    text_handle.write(text_data)
    text_handle.seek(256)

    try:
        binary_guesser(text_handle, num_bytes=128)
    except FormatError as error:
        assert error.message == '{0} is probably not a binary ' \
                                'file'.format(text_handle.name)
    assert text_handle.tell() == 256
