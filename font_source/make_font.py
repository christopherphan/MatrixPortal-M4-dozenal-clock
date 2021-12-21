from collections.abc import Sequence
from typing import NamedTuple
import unicodedata as ud
import json


def to_picture_row(k: int) -> str:
    outstr = bin(k)[2:]
    outstr = f"{outstr:>8}"
    outstr = outstr.replace("1", "#").replace("0", " ")
    return outstr


def to_picture(bitmap: Sequence[int]) -> list[str]:
    return [to_picture_row(k) for k in bitmap]


def to_bitmap_row(k: str) -> int:
    u = f"{k:<8}".replace(" ", "0").replace("#", "1")
    return int(u, 2)


def to_bitmap(pic: Sequence[str]) -> list[int]:
    return [to_bitmap_row(k) for k in pic]


def show_hex(list_: Sequence[int]) -> list[str]:
    return [f"{k:02x}" for k in list_]


def rotate_picture(pic: Sequence[str]) -> list[str]:
    return [k[::-1] for k in pic[::-1]]


def rotate_bitmap(bitmap: Sequence[int]) -> list[int]:
    return to_bitmap(rotate_picture(to_picture(bitmap)))


def left_trim_pic(pic: Sequence[str]) -> list[str]:
    trim_amt = min([k.find("#") for k in pic])
    return [f"{k[trim_amt:]:<8}" for k in pic]


def rotate_and_trim_bitmap(bitmap: Sequence[int]) -> list[int]:
    return to_bitmap(left_trim_pic(rotate_picture(to_picture(bitmap))))


def show_bitmap(bitmap: Sequence[int]) -> None:
    print("\n".join(to_picture(bitmap)))


front_matter = """STARTFONT 2.1
FONT -ChrisPhan-6by5-Medium-R-Normal--6-60-75-75-P-40-ISO10646-1
SIZE 5 75 75
FONTBOUNDINGBOX 6 5 0 -1
STARTPROPERTIES 2
FONT_ASCENT 5
FONT_DESCENT 0
ENDPROPERTIES"""


class Character(NamedTuple):
    bitmap: list[int]
    char_desc: str
    encoding: int
    width: int

    @property
    def code(self) -> str:
        char_info: str = f"STARTCHAR {self.char_desc}\nENCODING {self.encoding}\n"
        char_info += "SWIDTH 1000 0\n"
        char_info += f"DWIDTH {self.width + 1} 0\n"
        char_info += f"BBX {self.width + 1} 5 0 0\n"
        char_info += "BITMAP\n"
        char_info += "\n".join(show_hex(self.bitmap)).upper()
        char_info += "\nENDCHAR"
        return char_info


def describe(x: str) -> str:
    x = x[0]
    return f"U+{ord(x):04x} ".upper() + ud.name(x)


char_data: dict[str, Character] = {}

with open("characters.txt", "rt") as infile:
    current_bitmap: list[int] = []
    char_desc: str = ""
    encoding: int = 0
    width: int = 0
    current_char: str = ""
    for idx, line in enumerate(infile):
        if idx % 7 == 0:
            current_bitmap = []
            print(line[:-1], end=", ")
            if line[:2].upper() == "U+":
                encoding = int(line[2:6], 16)
                current_char = chr(encoding)
            else:
                current_char = line[0]
                encoding = ord(current_char)
            char_desc = describe(current_char)
            print(char_desc)
        elif idx % 7 == 6:
            width = line.count("-")
            char_data[current_char] = Character(
                current_bitmap, char_desc, encoding, width
            )
        else:
            current_bitmap.append(to_bitmap_row(line[:-1]))

to_rotate = {"\N{TURNED DIGIT TWO}": "2", "\N{TURNED DIGIT THREE}": "3"}
for k in to_rotate:
    char_data[k] = Character(
        rotate_and_trim_bitmap(char_data[to_rotate[k]].bitmap),
        describe(k),
        ord(k),
        char_data[to_rotate[k]].width,
    )

with open("chris_6x5.bdf", "wt") as outfile:
    outfile.write(
        front_matter
        + f"\nCHARS {len(char_data)}\n"
        + "\n".join([char_data[k].code for k in char_data])
        + "\nENDFONT"
    )


with open("chris_6x5.json", "wt") as outfile:
    json.dump({char_data[k].encoding: char_data[k].bitmap for k in char_data}, outfile)
