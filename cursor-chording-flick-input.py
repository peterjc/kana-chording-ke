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
"""Generate Karabina Elements JSON for flick-input like kana chording."""

vowels = "aiueo"  # used as suffix for default romaji mapping
modifiers = [None, "left_arrow", "up_arrow", "right_arrow", "down_arrow"]
assert len(vowels) == len(modifiers)


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


for modifier, suffix in zip(modifiers, vowels):
    print(romaji_simple_mapping("h", modifier, "h" + suffix))
