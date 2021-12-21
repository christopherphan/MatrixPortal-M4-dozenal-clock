########################################################################################
# Dozenal clock LED sign, for Adafruit MatrixPortal-M4
#
# By Christopher Phan, cphan@chrisphan.com
# github: christopherphan
#
# MIT License
#
# Copyright (c) 2021 Christopher Phan, Ph.D.
#
# Loosely based on Metro Matrix Clock:
# https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Metro_Matrix_Clock
# Copyright (c) 2018 Adafruit Industries
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
import dozenal_circuit as doz
import weekdate as wd
import board

from adafruit_matrixportal.matrixportal import MatrixPortal

days_of_week = ["M", "Tu", "W", "Th", "F", "Sa", "Su"]


def datetext(ttuple):
    """
    Update the date line of the clock.
    """
    period = (
        ttuple[5] // 5
    )  # We update and change format of the date line every 5 seconds
    if period % 3 == 0:  # ISO month and date, e.g. 12-20 for 20th day of December
        return "{:02d}-{:02d}".format(ttuple[1], ttuple[2])
    elif period % 3 == 1:  # ISO week-date format, e.g., 2021-W51-1
        # See https://en.wikipedia.org/wiki/ISO_week_date
        current_wd = wd.iso_week_date(ttuple)
        return "W{:02d}-{}".format(current_wd[1], current_wd[2])
    else:  # Day of the week and date, e.g. M 20 for Monday the 20th
        return "{} {}".format(days_of_week[ttuple[6]], ttuple[2])


def callibrate_clock():
    """
    Reach out to the Adafruit servers and get the current time.
    Returns start_unixtime (the value of time.time()) and start_monotime (the value
        of time.monotonic_ns() // 10 ** 6).

    Requires secrets.py to be set up with WiFi network info as well as Adafruit IO
    service username and API key. See this page for more details:
        https://learn.adafruit.com/adafruit-matrixportal-m4/internet-connect
    """
    # Test all the characters in custom font.
    matrixportal.set_text("MTWFS")
    matrixportal.set_text("01234567", 1)
    matrixportal.set_text(
        "89 \u218a\u218b-;:", 2
    )  # U+218a and U+218b are dozenal digits
    try:
        matrixportal.get_local_time()
        matrixportal.set_text("ahu")
    except RuntimeError:
        matrixportal.set_text(":::::::")
        matrixportal.set_text(":::::::", 1)
        matrixportal.set_text(":::::::", 2)
    time.sleep(2)
    start_unixtime = time.time()
    start_monotime = time.monotonic_ns() // 10 ** 6
    return start_unixtime, start_monotime


matrixportal = MatrixPortal(
    status_neopixel=board.NEOPIXEL, debug=True, width=32, height=16
)

matrixportal.add_text((0, 2), "chris_6x5.bdf", 0x44FF44)  # Top line is decimal time
matrixportal.add_text((0, 7), "chris_6x5.bdf", 0x7733FF)  # Second line is dozenal time
matrixportal.add_text((0, 12), "chris_6x5.bdf", 0xFF3333)  # Third line is date

start_unixtime, start_monotime = callibrate_clock()
last_second = start_unixtime
current_offset = 0
last_doz = None
last_date_text = ""
ttuple = time.localtime(last_second)

while True:
    # CircuitPython time.time() only has integer precision, but we need
    # greater precision for the Dozenal clock (since each triciaHour is 25/12
    # seconds). We accomplish this by using both time.time() and
    # time.monotonic_ns().
    new_second = time.time()
    new_tick = time.monotonic_ns() // 10 ** 6
    update_all = False
    if new_second != last_second:
        current_offset = (new_second - start_unixtime) * 1000 - (
            new_tick - start_monotime
        )
        last_second = new_second
        if last_second % 2833 == 0:
            update_all = True
        ttuple = time.localtime(new_second)
        # Decimal time
        matrixportal.set_text(
            "{hours:02d}{colon}{minutes:02d}{colon}{seconds:02d}".format(
                hours=ttuple[3],
                minutes=ttuple[4],
                seconds=ttuple[5],
                colon=" " if new_second % 2 else ":",
            ),
            0,
        )
    new_date_text = datetext(ttuple)
    if new_date_text != last_date_text or update_all:
        last_date_text = new_date_text
        matrixportal.set_text(new_date_text, 2)
    precise_time = new_tick - start_monotime + start_unixtime * 1000 + current_offset
    new_doz = doz.dozenal_time(precise_time, 3)
    if last_doz is None or new_doz != last_doz or update_all:
        last_doz = new_doz
        # Dozenal format is xx;xxx in hours. The semicolon functions as a radix
        # seperator. It blinks (shown if triaciaHour is even).
        matrixportal.set_text(
            "{}{}{}".format(new_doz[0], " " if new_doz[2] else ";", new_doz[1]),
            1,
        )
    if new_second > start_unixtime + 4020:
        start_unixtime, start_monotime = callibrate_clock()
