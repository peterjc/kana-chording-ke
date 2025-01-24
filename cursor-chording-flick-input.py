#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2025 Peter J. A. Cock
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
"""Generate Karabina Elements JSON for flick-input like kana chording.

```
あいうえお　アイウエオ	aiueo
ぁぃぅぇぉ　ァィゥェォ　x+ or l+ for small vowels
かきくけこ　カキクケコ	k+
がぎぐげご　ガギグゲゴ	g+
さしすせそ　サシスセソ	s+ - can use si or shi for し
ざじずぜじ　ザジズゼゾ　z+ - can use zi or ji  for じ
たちつてと　タチツテト　t+ - can use ti or chi for ち
・・っ・・　・・ッ・・　did this with xtsu, xtu, xtsu or ltu
だぢづでど　ダヂヅデド　d+
なにぬねの　ナニヌネノ　n+
はひふへほ　ハヒフヘホ　h+ - can use hu for fu for ふ
ばびぶべぼ　バビブベボ　b+
ぱぴぷぺぽ　パピプペポ　p+
まみむめも　マミムメモ　m+
や・ゆ・よ　ヤ・ユ・ヨ　y+
ゃ・ゅ・ょ　ャ・ュ・ュ　xy+
らりるれろ　ラリルレロ　r+
わゐ・ゑを　ワヰ・ヱヲ　w+ - with wa/wyi/(vu)/wye/wo for the obsolete ones
・・ゔ・・　・・ヴ・・　v+
・・ん・・　・・ン・・　nn
・・ー・・　・・ー・・　used minus - so no need to map this
```

"""

rows = [
    "x",  # small vowels - could use prefix l instead.
    "k",
    "g",
    "s",
    "z",
    "t",
    "xt",  # just for small tsu aka xtsu aka xtu etc.
    "d",
    "n",
    "h",
    "b",
    "p",
    "m",
    "y",
    "xy",  # small ya, yu, yo
    "r",
    "w",  # including ん in place of wu
    "v",
]
vowels = "aiueo"  # used as suffix for default romaji mapping
modifiers = [None, "left_arrow", "up_arrow", "right_arrow", "down_arrow"]
assert len(vowels) == len(modifiers)
exceptions = {
    "si": "shi",  # use typical romaji for kana し although "si" works anyway
    "zi": "ji",  # use typical romaji for kana じ although "zi" works anyway
    "ti": "chi",  # use typical romaji for kana ち although "ti" works anyway
    "xta": None,  # there is no small た
    "xti": None,  # there is no small ち
    "xtu": "xtsu",  # use more logical code for small っ
    "xte": None,  # there is no small て
    "xto": None,  # there is no small と
    "hu": "fu",  # use typical romaji for kana ふ although "hu" works anyway
    "yi": None,  # historical, not used (large)
    "ye": None,  # historical, not used (large)
    "xyi": None,  # historical, not used (small)
    "xye": None,  # historical, not used (small)
    "wi": "wyi",  # historical, only used in names now
    "wu": "nn",  # "wu" is historical and not used, instead w+up mapped to "ん"
    "we": "wye",  # historical, only used in names now
    "va": None,  # not used as a single kana, just vu for ゔ/ヴ
    "vi": None,  # not used as a single kana, just vu for ゔ/ヴ
    "ve": None,  # not used as a single kana, just vu for ゔ/ヴ
    "vo": None,  # not used as a single kana, just vu for ゔ/ヴ
}


def romaji_simple_mapping(
    key: str, modifier: str, out_keys: str, threshold: int = 100
) -> str:
    """Generate Karabina Elements JSON to map key+modifier to given romaji key sequence.

    Using the following mappings for macOS Japanese - Romaji mode:

    * `は` from `h` alone to `ha`
    * `ひ` from `h` + `left_arrow` to `hi`
    * `ひ` from `h` + `up_arrow` to `hu` or `fu`
    * `へ` from `h` + `right_arrow` to `he`
    * `ほ` from `h` + `down_arrow` to `ho`
    """
    out_list = ", ".join(('{"key_code": "' + _ + '"}') for _ in out_keys)
    return (
        f"""\
{{"description": "Romanji mode: {key}+{modifier} sends {out_keys}",
    "enabled": false,
    "manipulators": [
        {{"conditions": [
                {{"input_sources": [{{"language": "^ja$" }}],
                    "type": "input_source_if"
                }}
            ],
            "from": {{"modifiers": {{"optional": ["any"] }},
                "simultaneous": [
                    {{"key_code": "{key}" }},
                    {{"key_code": "{modifier}" }}
                ],
                "simultaneous_options": {{"key_down_order": "insensitive" }}
            }},
            "parameters": {{"basic.simultaneous_threshold_milliseconds": {threshold} }},
            "to": [ {out_list} ],
            "type": "basic"
        }}
    ]
}}
"""
        if modifier
        else f"""\
{{"description": "Romanji mode: {key} alone sends {out_keys}",
    "enabled": false,
    "manipulators": [
        {{"conditions": [
                {{"input_sources": [{{"language": "^ja$" }}],
                    "type": "input_source_if"
                }}
            ],
            "from": {{"modifiers": {{"optional": ["any"] }},
                "simultaneous": [
                    {{"key_code": "{key}" }},
                ],
            }},
            "parameters": {{"basic.simultaneous_threshold_milliseconds": {threshold} }},
            "to": [ {out_list} ],
            "type": "basic"
        }}
    ]
}}
"""
    )


# a -> あ, a+left -> い, etc
for modifier, vowel in zip(modifiers, vowels):
    print(romaji_simple_mapping("a", modifier, vowel))

for prefix in rows:
    for modifier, suffix in zip(modifiers, vowels):
        romaji = prefix + suffix
        romaji = exceptions.get(romaji, romaji)  # apply exception
        if not romaji:
            continue  # skip the historical entries "yi" and "ye"
        print(romaji_simple_mapping(prefix, modifier, romaji))
