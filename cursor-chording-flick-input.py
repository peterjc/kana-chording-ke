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
ゃ・ゅ・ょ　ャ・ュ・ュ　xy+ or ly+ for small ya/yu/yo
らりるれろ　ラリルレロ　r+
わゐ・ゑを　ワヰ・ヱヲ　w+ - with wa/wyi/(vu)/wye/wo for the obsolete ones
・・ゔ・・　・・ヴ・・　v+
・・ん・・　・・ン・・　nn
・・ー・・　・・ー・・　used minus - so no need to map this
```

"""

import sys

output_name = "cursor-chording-flick-input-romaji-mode.json"
vowel_modifiers = {
    "i": "left_arrow",
    "u": "up_arrow",
    "e": "right_arrow",
    "o": "down_arrow",
    "a": None,  # last as a workaround (KE rule order ought not to matter)
}
rows = [
    "",  #  a row:  あいうえお
    "l",  # small:  ぁぃぅぇぉ (using l for little here, and x for small ya/yu/yo)
    "k",  # ka row: かきくけこ
    "g",  # ga row: がぎぐげご
    "s",  # sa row: さしすせそ
    "z",  # za row: ざじずぜぞ
    "t",  # ta row: たちつてと
    #  "xt" small:  ・・っ・・ (just small tsu っ aka xtsu aka xtu etc).
    "d",  # da row: だぢづでど
    "n",  # na row: なにぬねの
    "h",  # ha row: はひふへほ
    "b",  # ba row: ばびぶべぼ
    "p",  # pa row: ぱぴぷぺぽ
    "m",  # ma row: まみむめも
    "y",  # ya row: や・ゆ・よ
    "xy",  # small: ゃ・ゅ・ょ (using x here, and l for small a/i/u/e/o)
    "r",  # ra row: らりるれろ
    "w",  # wa row: わ・ん・を (including ん in place of wu)
    "v",  # va row: ・・ゔ・・ (only mapping vu, others don't give single kana)
]
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
    "va": None,  # not used as double kana, just vu for ゔ/ヴ
    "vi": None,  # not used as double kana, just vu for ゔ/ヴ
    "ve": None,  # not used as double kana, just vu for ゔ/ヴ
    "vo": None,  # not used as double kana, just vu for ゔ/ヴ
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
    "manipulators": [
        {{"conditions": [
                {{"input_sources": [{{"language": "^ja$" }}],
                    "type": "input_source_if"
                }}
            ],
            "from": {{"modifiers": {{"optional": ["any"] }},
                "simultaneous": [
                    {{"key_code": "{key}" }}
                ]
            }},
            "parameters": {{"basic.simultaneous_threshold_milliseconds": {threshold} }},
            "to": [ {out_list} ],
            "type": "basic"
        }}
    ]
}}
"""
    )


rules = []
# a -> あ, a+left -> い, etc
for vowel, modifier in vowel_modifiers.items():
    rules.append(romaji_simple_mapping("a", modifier, vowel))

for prefix in rows:
    for suffix, modifier in vowel_modifiers.items():
        romaji = prefix + suffix
        romaji = exceptions.get(romaji, romaji)  # apply exception
        if not romaji:
            continue  # skip the historical entries "yi" and "ye" etc
        # binding the first letter only (small ya/yu/yo special case)
        rules.append(romaji_simple_mapping(prefix[:1], modifier, romaji))

with open(output_name, "w") as handle:
    # This does not nicely indent.
    # Should the keyboard stay as ISO?
    handle.write(
        """\
{
  "title": "Kana chording with cursor keys (Romaji Mode)",
  "maintainers": [
    "peterjc"
  ],
  "author": "Peter J. A. Cock",
  "homepage": "https://github.com/peterjc/kana-chording-ke",
  "repo": "https://github.com/peterjc/kana-chording-ke",
  "rules": [
"""
        + ",\n".join(_.strip() for _ in rules)
        + """\
    ]
}"""
    )

sys.stderr.write(f"Generated {len(rules)} rules in {output_name}\n")
sys.stderr.write(
    "Try moving that under ~/.config/karabiner/assets/complex_modifications/\n"
)
