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
"""Generate Karabiner Elements JSON for flick-input like kana chording.

The general pattern is we bind each row of the 5-column extended gojūon to a
single letter, generally the first letter of the standard romaji. We include
binding for maru and ten-ten modified characters. Thus in addition to binding
h to the ha-row (はひふへほ) we bind p for the pa-row (ぱぴぷぺぽ), and b for the
ba-row (ばびぶべぼ).

For example, k is mapped to the ka-row (かきくけこ):

* k alone → ka for か,
* k+left → ki for き,
* k+up → ku for く,
* k+right → ke for け,
* k+down → ko for こ.

This is the standard Japanese vowel order a/i/u/e/o clockwise, matching the
iOS flick-input. You can use the Japanese mode kanji support to select words
in katakana, or enable shift for katakana. In that mode, K alone → KA giving
カ, and so on.

On macOS both la/li/lu/le/lo and xa/xi/xu/xe/xo give the small vowels
(ぁぃぅぇぉ), but here only l is bound to them, and x is instead used for
small ya/yu/yo (ゃゅょ).

Currently there is no binding for small tsu っ, available in macOS romaji
as xtsu, xsu, ltsu and lsu. This is normally done by a double consanant,
thus kka or xtsu ka would both give っか.

Following iOS flick-input, the W key mappings includes ん rather than the
unused wu. However, our mapping sticks to gojūo layout and rather than
mapping w+right to the long sound character (ー) we have the legacy wye and wyi
romaji (ゑゐ) used in some names:

* w alone → wa for わ,
* w+left → wyi for ゐ,
* w+up → nn for ん,
* w+right → wye for ゑ,
* w+down → wo for を.

In comparison, iOS flick-input uses:

* w alone → wa for わ,
* w+left → wo for を (rather than with down),
* w+up → nn for ん,
* w+right → - for ー,
* w+down unused (as on final row of their grid)

We do copy their punction mapping bound to comma, but move long sound
character (ー) here to the down modifier:

* `,` alone → `,` for `、` (Japanese comma),
* `,`+`left` → `.` for `。`  (Japanese full stop),
* `,`+`up` → `!` for `！` (Japanese exclamation mark),
* `,`+`right` → `?` for `？` (Japanese question mark),
* `,`+`down` → `-` for `ー` (unused on iOS as on final row of their grid)

"""

import sys

output_name = "cursor-chording-flick-input.json"
title = "Kana chording with cursor keys"
romaji_description = (
    "Romanji mode chording: row key like r plus cursors sends ra/ri/ru/er/ro"
)
romaji_numpad_description = (
    "Romanji mode chording: NumPad key like 3 plus cursors sends ra/ri/ru/er/ro"
)
vowel_modifiers = {
    "i": "left_arrow",
    "u": "up_arrow",
    "e": "right_arrow",
    "o": "down_arrow",
    "a": None,  # last as a workaround (KE rule order ought not to matter)
}
rows = {
    "": "あいうえお",
    # Using l for little here (small vowels), and x for small ya/yu/yo:
    "l": "ぁぃぅぇぉ",  # chiisai a -> la
    "k": "かきくけこ",
    "g": "がぎぐげご",  # ten-ten ka -> ga
    "s": "さしすせそ",
    "z": "ざじずぜぞ",  # ten-ten sa -> za
    "t": "たちつてと",
    # TODO: "・・っ・・" for small っ via xtsu/xtu or ltsu/lsu
    "d": "だぢづでど",  # ten-ten ta -> da
    "n": "なにぬねの",
    "h": "はひふへほ",
    "b": "ばびぶべぼ",  # ten-ten ha -> ba
    "p": "ぱぴぷぺぽ",  # maru ha -> pa
    "m": "まみむめも",
    # Follow iOS flick input placement of Japanese open/close quotes
    "y": "や「ゆ」よ",
    # Using x here for small ya/yu/yo as next to y in alphabet,
    # and binding the small a/i/u/e/o to l for little:
    "xy": "ゃ・ゅ・ょ",  # chiisai ya -> xya
    "r": "らりるれろ",
    # Follow iOS flick-input and typical charts with ん in place of wu,
    # Note wi/we must be entered as wyi/wye:
    "w": "わゐんゑを",
    # Not only vu gives a single kana (thus using a list)
    "v": ["ゔぁ", "ゔぃ", "ゔ", "ゔぇ", "ゔぉ"],
    # Punctuation
    ",": "、。！？ー",
}
# Could infer the blank exceptions from "・" entries in above dict?
exceptions = {
    "xta": None,  # there is no small た
    "xti": None,  # there is no small ち
    "xte": None,  # there is no small て
    "xto": None,  # there is no small と
    "yi": '{"key_code": "open_bracket"}',  # historical, not used (large), using for open quote
    "ye": '{"key_code": "close_bracket"}',  # historical, not used (large), using for close quote
    "xyi": None,  # historical, not used (small)
    "xye": None,  # historical, not used (small)
    # wi is historical, only used in names now
    "wi": '{"key_code": "w"}, {"key_code": "y"}, {"key_code": "i"}',
    # "wu" is historical and not used, instead w+up mapped to "ん"
    "wu": '{"key_code": "n"}, {"key_code": "n"}',
    # we is historical, only used in names now
    "we": '{"key_code": "w"}, {"key_code": "y"}, {"key_code": "e"}',
    # punctuation
    ",a": '{"key_code": "comma"}',
    ",i": '{"key_code": "period"}',
    ",u": '{"key_code": "1", "modifiers": ["shift"]}',  # for "!"
    ",e": '{"key_code": "slash", "modifiers": ["shift"]}',  # for "?""
    ",o": '{"key_code": "hyphen"}',
}


def romaji_simple_mapping(
    in_key: str,
    modifier: str,
    out_keys: str,
    source_map=None,
    threshold: int = 100,
) -> str:
    """Generate Karabina Elements JSON to map key+modifier to given romaji key sequence.

    Using the following mappings for macOS 「Japanese - Romaji」 mode:

    * `は` from `h` alone to `ha`
    * `ひ` from `h` + `left_arrow` to `hi`
    * `ひ` from `h` + `up_arrow` to `hu` or `fu`
    * `へ` from `h` + `right_arrow` to `he`
    * `ほ` from `h` + `down_arrow` to `ho`
    """
    # Used these in per mapping descriptions:
    # vowel = next(k for (k, v) in vowel_modifiers.items() if v == modifier)
    # kana = rows["" if prefix == "a" else prefix]["aiueo".index(vowel)]
    return (
        f"""\
                {{
                    "type": "basic",
                    "conditions": [
                        {{
                            "input_sources": [
                                {{
                                    "input_source_id": "Romaji",
                                    "language": "ja"
                                }}
                            ],
                            "type": "input_source_if"
                        }}
                    ],
                    "from": {{
                        "modifiers": {{"optional": ["any"] }},
                        "simultaneous": [
                            {{"key_code": "{in_key}" }},
                            {{"key_code": "{modifier}" }}
                        ],
                        "simultaneous_options": {{"key_down_order": "insensitive" }}
                    }},
                    "parameters": {{"basic.simultaneous_threshold_milliseconds": {threshold} }},
                    "to": [ {out_keys} ]
                }}
"""
        if modifier
        else f"""\
                {{
                    "type": "basic",
                    "conditions": [
                        {{
                            "input_sources": [{{"language": "^ja$" }}],
                            "type": "input_source_if"
                        }}
                    ],
                    "from": {{
                        "modifiers": {{"optional": ["any"] }},
                        "simultaneous": [
                            {{"key_code": "{in_key}" }}
                        ]
                    }},
                    "parameters": {{"basic.simultaneous_threshold_milliseconds": {threshold} }},
                    "to": [ {out_keys} ]
                }}
"""
    )


rules = []
numpad_rules = []
numpad_map = {
    "a": "keypad_7",  # Top left
    "k": "keypad_8",
    "s": "keypad_9",
    "t": "keypad_4",
    "n": "keypad_5",
    "h": "keypad_6",
    "m": "keypad_1",
    "y": "keypad_2",
    "r": "keypad_3",
    "w": "keypad_0",  # Might use larger key for ten-ten/maru/chiisai?
    "comma": "keypad_period",
}

# Mappings for extended gojūon table including ba and pa as well as ha,
# plus comma bindings based on iOS flick-input
for prefix in rows:
    for suffix, modifier in vowel_modifiers.items():
        romaji = prefix + suffix

        if not prefix:
            # binding a/i/u/e/o to a
            key = "a"
        elif prefix == ",":
            # needs a name as the key code
            key = "comma"
        else:
            # binding the first letter only (small ya/yu/yo special case)
            key = prefix[:1]

        try:
            romaji_out_keys = exceptions[romaji]
        except KeyError:
            romaji_out_keys = ", ".join(('{"key_code": "' + _ + '"}') for _ in romaji)
        if not romaji_out_keys:
            # skip the historical entries yi/ye and small versions etc
            # Might be better to map this to a no-op, otherwise macOS
            # sees y and left, or y and right, x and left, x and right
            continue

        rules.append(romaji_simple_mapping(key, modifier, romaji_out_keys))
        if key in numpad_map:
            # With only ~12 keys, can't give ten-ten (gzdb), maru forms (p)
            # nor small forms (x) with their own keys
            numpad_rules.append(
                romaji_simple_mapping(numpad_map[key], modifier, romaji_out_keys)
            )

with open(output_name, "w") as handle:
    # This does not nicely indent.
    # Should the keyboard stay as ISO?
    handle.write(
        f"""\
{{
    "title": "{title}",
    "maintainers": [
        "peterjc"
    ],
    "author": "Peter J. A. Cock",
    "homepage": "https://github.com/peterjc/kana-chording-ke",
    "repo": "https://github.com/peterjc/kana-chording-ke",
    "rules": [
        {{
            "description": "{romaji_description}",
            "manipulators": [
"""
        + ",\n".join(_.rstrip() for _ in rules)
        + f"""\
            ]
        }},
        {{
            "description": "{romaji_numpad_description}",
            "manipulators": [
"""
        + ",\n".join(_.rstrip() for _ in numpad_rules)
        + """\
            ]
        }
    ]
}
"""
    )

sys.stderr.write(f"Generated {len(rules)} sub-rules in {output_name}\n")
sys.stderr.write("Try running this to add to Karabiner Elements:\n\n")
sys.stderr.write(
    f"cp {output_name} ~/.config/karabiner/assets/complex_modifications/\n\n"
)
sys.stderr.write("Then open 'Karabiner Elements', select 'Complex Modifications',\n")
sys.stderr.write("click 'Add predefined rule', scroll down to find the new\n")
sys.stderr.write(f"'{title}' block with entries\n")
sys.stderr.write(f"'{romaji_description}' etc.\n")
sys.stderr.write("Click enable individually (or enable all).")
