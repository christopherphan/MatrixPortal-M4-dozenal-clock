# MatrixPortal-M4-dozenal-clock
Configure the MatrixPortal-M4 to display a digital clock with decimal and dozenal (base-12) time
A few months ago, I bought a
[MatrixPortal-M4](https://learn.adafruit.com/adafruit-matrixportal-m4) and LED matrix
display from Adafruit. My goal was to create some sort of digital dozenal (base-12) clock.

![Photo of the completed clock](clock_picture.jpg)

My starting point was [a project from Adafruit's web
site](https://learn.adafruit.com/network-connected-metro-rgb-matrix-clock) to build a
network-connected digital clock.

## Set-up

1. Follow [Adafruit's
instructions](https://learn.adafruit.com/network-connected-metro-rgb-matrix-clock/prep-the-matrixportal).
to build the Matrixportal-M4. (My code is designed to run on a 32 × 16 LED matrix display.)

2. Follow [Adafruit's
instructions](https://learn.adafruit.com/network-connected-metro-rgb-matrix-clock/install-circuitpython-2)
to install CircutPython on the MatrixPortal.

3. Copy the files in the directory `copy_to_board` of this repo onto the MatrixPortal.

## Dozenal time

### Dozenal numbers

Dozenal is another name for the base-12 number system, in contract to the decimal
(base-10) system that is typically used. One convention is to use the characters X and E
to represent digits for 10 and 11, respectively. (Later, we will discuss a different
convention that I actually used on the clock.)

| Decimal | Dozenal |
| ------: | ------: |
|       0 |       0 |
|       1 |       1 |
|       2 |       2 |
|     ... |     ... |
|       9 |       9 |
|      10 |       X |
|      11 |       E |
|      12 |      10 |
|      13 |      11 |
|      14 |      12 |
|     ... |     ... |
|      19 |      17 |
|      20 |      18 |
|      21 |      19 |
|      22 |      1X |
|      23 |      1E |
|      24 |      20 |
|      25 |      21 |
|     ... |     ... |
|     143 |      EE |
|     144 |     100 |
|     145 |     101 |
|     ... |     ... |

### Rationale for dozenal

In many ways, the dozenal superior to decimal. The number 12 = 2 × 2 × 3 has more divisors
than 10 = 2 × 5. (In fact, 12 is an example of a
   [Superior highly composite
   number](https://en.wikipedia.org/wiki/Superior_highly_composite_number).)
As a consequence, dozenal expansions of fractions are more likely to terminate than
decimal expansions.


| Decimal fraction | Decimal expansion | Dozenal expansion |
|:-----------------| :-----------------| :-----------------|
| 1/2              | 0.5               | 0;6               |
| 1/3              | 0.3333333333...   | 0;4               |
| 1/4              | 0.25              | 0;3               |
| 1/5              | 0.2               | 0;249724972...    |
| 1/6              | 0.1666666666...   | 0;2               |
| 1/7              | 0.1428571429...   | 0;186X35186...    |
| 1/8              | 0.125             | 0;16              |
| 1/9              | 0.1111111111...   | 0;14              |
| 1/10             | 0.1               | 0;124972497...    |
| 1/11             | 0.0909090909...   | 0;111111111...    |
| 1/12             | 0.0833333333...   | 0;1               |

(In this table, we use X to represent 10, E to represent 11, and ; as a radix separator.)

## Pitman notation

Above, I used the digit X to represent 10 and E to represent 11. Another common notation
is the set of Pitman digits, which resemble the digits 2 and 3, rotated
180°. These are in Unicode at codepoints [U+218A (TURNED DIGIT
TWO)](https://codepoints.net/U+218A) and [U+218B (TURNED
DIGIT THREE)](https://codepoints.net/U+218B). Font support remains very spotty, although
Google's [Noto Sans Symbols](https://fonts.google.com/noto/specimen/Noto+Sans+Symbols)
font has them.
