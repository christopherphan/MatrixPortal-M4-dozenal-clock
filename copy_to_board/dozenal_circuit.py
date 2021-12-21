########################################################################################
# Dozenal module for CircuitPython, for Dozenel clock LED sign
#
# By Christopher Phan, cphan@chrisphan.com
# github: christopherphan
#
# MIT License
#
# Copyright (c) 2021 Christopher Phan, Ph.D.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
########################################################################################

import time

dozdict = {k: str(k) for k in range(10)}
# Pitman digits, which are in Unicode:
dozdict[10] = chr(8586)  # Called TURNED DIGIT TWO, this represents 10 in Dozenal
dozdict[11] = chr(8587)  # Called TURNED DIGIT THREE, this represents 11 in Dozenal


def to_doz(x, minlen=0):
    """Convert an integer into a string with dozenal represenation, using the Pitman
        digits.

    :param x: The integer to be represented in dozenal.
    :type x: int
    :param minlen: The minumum length of the output, defaults to 0. Must be between
        0 and 4, inclusively.
    :type minlen: int, optional
    :return: A string with x in dozenal (base-12), using the Pitman digits (Unicode
        code-points U+218A and U+218B for 10 and 11, respectively).
    :rtype: str
    """
    doz_str = ""
    quot = x
    rem = 0
    while quot > 0 or len(doz_str) < minlen:
        quot, rem = divmod(quot, 12)
        doz_str = dozdict[rem] + doz_str

    return doz_str


def dozenal_time(milliseconds, precision=3):
    """Converts Unix time in milliseconds to the local time in hours in dozenal.

    :param milliseconds: The number of miliseconds since 1970-01-01T00:00 UTC.
    :type milliseconds: int
    :param precision: The position in dozenal places of the time in hours. Must be
        an integer between 0 and 4, inclusive. The default is 3.
    :type precision: int
    :raises ValueError: Raised if precision is not an integer between 0 and 4,
        inclusive.
    :return: the whole part of the hour in Dozenal, the fractional part of the hour
        in Dozenal, and a boolean indicating if the semicolon Humphrey point should be
        illuminated or not.
    :rtype: Tuple[str, str, bool]

    """
    if precision not in [0, 1, 2, 3, 4]:
        raise ValueError("precision must be an integer between 0 and 4")
    local_hour = time.localtime(milliseconds // 1000)[3]
    current_time = (milliseconds * 144 // 25000) % (
        12 ** 4
    )  # Every tim (quadciaHour, or 12 ** -4 hours) is 25/144 seconds.
    display_time = (
        (current_time // 12 ** (4 - precision)) % 12 ** precision
        if precision != 4
        else current_time
    )
    flash = bool((current_time // 12) % 2)  # this is so the Humphrey point can flash
    return to_doz(local_hour, 2), to_doz(display_time, precision), flash
