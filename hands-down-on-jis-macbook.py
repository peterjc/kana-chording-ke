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
"""Generate Karabiner Elements JSON for 'Hands Down Promethium' on JIS MacBook.

Karabiner Elements is a free open source keyboard remapping tool for macOS.
Hands Down Promethium is a modern keyboard layout optimised for English,
intended for split keyboards with the letter R and space both on thumb keys.

The Apple MacBook sold in Japan has a keyboard with a short spacebar (just
over three keys wide, underneath the Qwerty VBN keys), flanked on the by the
"eisuu" (switch to qwerty) and "kana" (switch to Japanese mode) keys.

This lets us remap the Japanese MacBook keyboard with two keys per thumb.
The left hand still uses the conventional home-keys (Qwerty ASDF), with
"eisuu" and space-bar as thumb keys. Due to the space-bar width we use a
"wide mod" and shift the right hand two columns further over (starting at
Qwerty L), with "kana" and right-command for the right thumb keys. Enter
becomes an easy horizontal pinkie move. This is enough for each hand to
have a three rows of five core block.

Without a sixth column for the right-hand as in the canonical Hands Down
Promethium layout, Q and Z were moved to the top right corner in favour of
hyphen and equals (which are in the right-hand's core 5x3 block instead).

This leaves a 2-2-3 central block (Qwerty YU, HJ, and BNM) into which the
punctuation typically on the right is transplanted (same row and order).
Hyphen and equals are in the right-hand's core 5x3 block, international3
(¥ and |) is moved to the centre block. The "ろ" key international1 for
underscore is also moved there.

The KE rules are deliberately defined not to be active in Japanese mode,
meaning Kana mode should still work, as will Romaji-Qwerty mode (although
you might want to type romaji using Hands Down?).

This was written and tested on the following:

* Apple MacBook Air, 13-inch, M3, 2024 - with Japanese Keyboard
* Apple macOS Sequoia 15.4.1
* Apple macOS keyboard layout set to "British - PC" (with Japanese input
  also setup, but using "ABC" as the romaji layout to match the keycaps).
* Karabiner Elements 15.3.9, with virtual keyboard type set to JIS (not
  ANSI or ISO) to reflect the physical keyboard and its keys.

Note compared that on the Japanese layout, brackets "("" and ")" are
on shift-8 and shift-9, unlike the USA or UK layouts using shift-9 and
shift-0. There are other signigicant differences in the punctuation,
including the placement of double quote and the @ sign (different between
Japanese, USA and UK layouts).
"""

import sys

script_version = "0.3"
layout_name = "Hands Down Promethium (2025 pico mod)"

# These are the keys are reported by Karabiner Elements (not JIS layout)
# excluding the function row, number row, backspace, enter key, globe/fn, and cursors.
jis_qwerty = (
    # Number row:
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "hyphen",
    "equal_sign",
    "international3",
    # Top row:
    "tab",
    "q",
    "w",
    "e",
    "r",
    "t",
    "y",
    "u",
    "i",
    "o",
    "p",
    "open_bracket",
    "close_bracket",
    # Home row:
    "left_control",  # ANSI/ISO has cap-locks here
    "a",
    "s",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "semicolon",
    "quote",
    "backslash",
    # Bottom row:
    "left_shift",
    "z",
    "x",
    "c",
    "v",
    "b",
    "n",
    "m",
    "comma",
    "period",
    "slash",
    "international1",
    "right_shift",
    # Thumb row:
    "caps_lock",
    "left_option",
    "left_command",
    "japanese_eisuu",
    "spacebar",
    "japanese_kana",
    "right_command",
)
# For both left and right, core is three rows of five, plus thumbs.
# The 2,2,3 key misc zone between the hands is being used for punctuation.
# Bottom row is left-shift, left-option, left-command, eisuu, spacebar,
# kana, right-command, (then globe/fn but cannot remap that, and cursors).
leave = "🔻"  # do not remap (transparent in Vial layer terminology)
hands_down = (
    # Number row:
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "international3",  # gives ` and ¬ in British PC layout
    "z",  # on right-hand pinkie sixth column in canonical HDP layout
    "q",  # on right-hand pinkie sixth column in canonical HDP layout
    # Top row:
    "🔻",  # i.e. tab
    "v",
    "p",
    "g",
    "m",
    "x",
    "open_bracket",  # misc zone, this is @ and ` on JIS`
    "close_bracket",  # misc zone, this is [ and { on JIS
    "slash",
    "period",
    "quote",
    "hyphen",
    "equal_sign",
    # Home row:
    "🔻",  # i.e. left-ctrl where ASNI/ISO has caps lock
    "s",
    "n",
    "t",
    "h",
    "k",
    "quote",  # misc zone, this is : and * on JIS
    "backslash",  # misc zone, this is ] and } on JIS
    "comma",
    "a",
    "e",
    "i",
    "c",
    # Bottom row:
    "b",
    "f",
    "d",
    "l",
    "j",
    "caps_lock",  # misc zone
    "international1",  # misc zone, this is _ on JIS (with and without shift)
    "international3",  # misc zone, this is ¥ and | on JIS
    "semicolon",
    "u",
    "o",
    "y",
    "w",
    # Thumb row:
    "left_shift",
    "🔻",  # i.e. left_option
    "🔻",  # i.e. left_command
    "r",
    "delete_or_backspace",
    "right_shift",
    "spacebar",
)
nav_variable = "navigation_layer"
nav_layer = (
    # Number row:
    "🔻",  # 1
    "🔻",  # 2
    "🔻",  # 3
    "🔻",  # 4
    "🔻",  # 5
    "🔻",  # 6
    "🔻",  # 7
    "🔻",  # 8
    "🔻",  # 9
    "🔻",  # 0
    "🔻",  # originally minus/equals in JIS
    "🔻",  # originally caret/tilde in JIS
    "🔻",  # originally yen/pipe in JIS
    # Top row:
    "🔻",  # tab
    "slash",
    "1",
    "2",
    "3",
    "equal_sign",
    "🔻",
    "🔻",
    "escape",
    "home",
    "up_arrow",
    "end",
    "delete_or_backspace",
    # Home row:
    "🔻",  # control
    "S(8)",  # *
    "4",
    "5",
    "6",
    "S(equal_sign)",
    "🔻",
    "🔻",
    "page_up",
    "left_arrow",
    "down_arrow",
    "right_arrow",
    "q",
    # Bottom row:
    "period",  # was shift on JIS
    "7",
    "8",
    "9",
    "hyphen",
    "🔻",
    "🔻",
    "🔻",
    "page_down",
    "A(left_arrow)",
    "return_or_enter",
    "A(right_arrow)",
    "z",
    # Thumb row:
    "🔻",
    "🔻",
    "🔻",
    "0",  # this is R in the base layer
    "🔻",
    "🔻",
    "🔻",
)
combos = {  # defined from JIS qwerty key names
    # Horizontal 2-key combos for brackets (open on left, close on right):
    ("r", "t"): "S(open_bracket)",  # {
    ("f", "g"): "S(9)",  # (
    ("c", "v"): "open_bracket",  # [
    ("i", "o"): "S(close_bracket)",  # }
    ("k", "l"): "S(0)",  # )
    ("comma", "period"): "close_bracket",  # ]
    # Vertical 2-key combos for Q & Z (outside base core):
    ("backslash", "right_shift"): "q",
    ("quote", "international1"): "z",
    # Horizontal 3-key combos:
    ("s", "d", "f"): "escape",
    ("z", "x", "c"): "tab",
    ("l", "semicolon", "quote"): "delete_or_backspace",
    ("period", "slash", "international1"): "return_or_enter",
    # Vertical 2-key combos (left-side near Qwerty location):
    ("g", "v"): "S(international1)",  # pipe
    ("japanese_eisuu", "c"): "S(international1)",  # pipe using thumb
    ("right_command", "comma"): "S(semicolon)",  # colon (like adj. thumb-shift)
    ("k", "comma"): "S(1)",  # exclamation-mark
    ("q", "a"): "international3",  # backtick (not exclamation-mark)
    ("w", "s"): "S(quote)",  # @-sign (often shift-2) in British layout)
    ("e", "d"): "S(3)",  # £-sign in British layout
    ("r", "f"): "S(4)",  # $-sign
    ("t", "g"): "S(5)",  # %-sign
    ("i", "k"): "S(6)",  # ^-sign
    ("o", "l"): "S(7)",  # &-sign
    ("p", "semicolon"): "non_us_pound",  # #-sign (often shift-3, mirrored from left)
    ("open_bracket", "quote"): "international1",  # backslash
    ("close_bracket", "backslash"): "S(backslash)",  # tilde
}

# Sanity-check layout:
assert len(jis_qwerty) == len(hands_down) == len(nav_layer) == 4 * 13 + 7, (
    f"{len(jis_qwerty)} vs {len(hands_down)} vs {len(nav_layer)} vs {4 * 13 + 7}"
)
before = set(jis_qwerty)
before.update(["delete_or_backspace"])  # added
after = {
    jis_key if hd_key == leave else hd_key
    for hd_key, jis_key in zip(hands_down, jis_qwerty)
}
after.update(
    [
        "japanese_eisuu",
        "japanese_kana",
        "right_command",
    ]  # lost
)
assert before == after, f"{before.difference(after)} vs {after.difference(before)})"

output_name = "hands-down-on-jis-macbook.json"
title = f"{layout_name} on Japanese MacBook (KE script version {script_version})"
rules_description = f"{layout_name} on JIS layout in non-Japanese input mode"

# Only active on Laptop's built-in keyboard (via is_built_in_keyboard).
#
# Want to exclude "input_source_id": "com.apple.inputmethod.Kotoeri.KanaTyping.Japanese"
# and "input_source_id": "com.apple.inputmethod.Kotoeri.RomajiTyping.Japanese", but
# allow "input_source_id": "com.apple.keylayout.ABC", "com.apple.keylayout.British-PC",
# etc - so making this conditional on not "language": "jp" instead.
#
# Note while this assume the Karabiner Elements virtual device is in JIS mode (like the
# physical keyboard), this allows the user to run any keyboard layout in non-Japanese
# mode (and macOS lets you set the romaji layout separately so that can still follow
# the JIS punctuation layout and keycaps).
input_source_conditions = [
    '{"identifiers": [{ "is_built_in_keyboard": true }], "type": "device_if"}',
    '{"input_sources": [{ "language": "ja" }], "type": "input_source_unless"}',
    '{"keyboard_types": ["jis"], "type": "keyboard_type_if"}',
]


def make_to_key(key):
    if key.startswith("S(") and key.endswith(")"):
        # Just shifted
        key = key[2:-1]
        return f'[{{"key_code": "{key}", "modifiers": ["left_shift"]}}]'
    elif key.startswith("A(") and key.endswith(")"):
        # Just alt aka option
        key = key[2:-1]
        return f'[{{"key_code": "{key}", "modifiers": ["left_option"]}}]'
    else:
        # No modifiers
        return f'[{{"key_code": "{key}"}}]'


def make_tap_hold(mod, key):
    """Rule to make a modifier act as a letter when tapped.

    Based on https://karabiner-elements.pqrs.org/docs/json/complex-modifications-manipulator-definition/to-if-held-down/#more-advanced-example

    Intended to be used with left and right shift which are mapped to
    letter keys, but I keep finding my fingers using left shift. Also
    my current corne split keyboard layout has the bottom left and
    right keys as shift when held.
    """
    return f"""\
                {{
                    "from": {{
                        "key_code": "{mod}",
                        "modifiers": {{ "optional": ["any"] }}
                    }},
                    "parameters": {{
                        "basic.to_delayed_action_delay_milliseconds": 150,
                        "basic.to_if_held_down_threshold_milliseconds": 150
                    }},
                    "to_delayed_action": {{ "to_if_canceled": [{{ "key_code": "{key}" }}] }},
                    "to_if_alone": [
                        {{
                            "halt": true,
                            "key_code": "{key}"
                        }}
                    ],
                    "to_if_held_down": [{{ "key_code": "{mod}" }}],
                    "conditions": [
                        {",\n                        ".join(input_source_conditions)}
                    ],
                    "type": "basic",
                    "description": "Get {key} when tap {mod}, remains {mod} if held"
                }}"""


def build_layer(layer_map, layer_var):
    yield f"""\
        {{
            "from": {{ "apple_vendor_top_case_key_code": "keyboard_fn" }},
            "to": [
                {{
                    "set_variable": {{
                        "name": "{nav_variable}",
                        "value": 1
                    }}
                }}
            ],
            "to_after_key_up": [
                {{
                    "set_variable": {{
                        "name": "{nav_variable}",
                        "value": 0
                    }}
                }}
            ],
            "to_if_alone": [{{ "apple_vendor_top_case_key_code": "keyboard_fn" }}],
            "type": "basic",
            "description": "Hold globe/fn key for navigation layer"
        }}
"""
    for hd_key, jis_key in zip(layer_map, jis_qwerty):
        if hd_key == leave or hd_key == jis_key:
            continue
        yield f"""\
                {{
                    "type": "basic",
                    "from": {{"key_code": "{jis_key}", "modifiers": {{"optional": ["any"]}}}},
                    "to": {make_to_key(hd_key)},
                    "conditions": [{{"name": "{layer_var}", "type": "variable_if", "value": 1}}],
                    "description": "Get {hd_key} when press {jis_key} on navigation layer"
                }}
"""


def build_hands_down_to_jis_qwerty_map():
    for combo_keys, key in combos.items():
        combo = ", ".join(f'{{"key_code": "{_}"}}' for _ in combo_keys)
        yield f"""\
                {{
                    "type": "basic",
                    "from": {{
                        "simultaneous": [{combo}]
                    }},
                    "to": {make_to_key(key)},
                    "parameters": {{
                        "basic.simultaneous_threshold_milliseconds": {50 if len(combo_keys) < 3 else 100}
                    }},
                    "conditions": [
                        {",\n                        ".join(input_source_conditions)}
                    ],
                    "description": "Get {key} when press combo {", ".join(combo_keys)}"
                }}
"""
    for hd_key, jis_key in zip(hands_down, jis_qwerty):
        if hd_key == leave or hd_key == jis_key:
            continue
        if hd_key == "quote" and jis_key == "p":
            # Extra rule so shift+quote gives double-quote as in USA
            # layout (Hands Down Promethium expectation) rather than
            # @ as per the British layout I have macOS set to.
            yield f"""\
                {{
                    "type": "basic",
                    "from": {{"key_code": "{jis_key}", "modifiers": {{"mandatory": ["shift"], "optional": ["any"]}}}},
                    "to": [{{"key_code": "2", "modifiers": ["left_shift"]}}],
                    "conditions": [
                        {{"input_sources": [{{ "input_source_id": "com.apple.keylayout.British" }}], "type": "input_source_if"}},
                        {",\n                        ".join(input_source_conditions)}
                    ],
                    "description": "Get shift+2 for double-quote on British layout when press shift+{jis_key}"
                }}
"""
        if jis_key in ("left_shift", "right_shift"):
            yield make_tap_hold(jis_key, hd_key)
        else:
            yield f"""\
                {{
                    "type": "basic",
                    "from": {{"key_code": "{jis_key}", "modifiers": {{"optional": ["any"]}}}},
                    "to": [{{"key_code": "{hd_key}"}}],
                    "conditions": [
                        {",\n                        ".join(input_source_conditions)}
                    ],
                    "description": "Get {hd_key} when press {jis_key}"
                }}
"""


nav_rules = list(build_layer(nav_layer, nav_variable))
hands_down_rules = list(build_hands_down_to_jis_qwerty_map())

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
"""
    )
    handle.write(
        f"""\
        {{
            "description": "{rules_description} : Navigation layer",
            "manipulators": [
"""
        + ",\n".join(_.rstrip() for _ in nav_rules)
        + """\n
            ]
        },
"""
    )
    handle.write(
        f"""\
        {{
            "description": "{rules_description} : Core mappings",
            "manipulators": [
"""
        + ",\n".join(_.rstrip() for _ in hands_down_rules)
        + """\n
            ]
        }
"""
    )
    # Finish the rule set
    handle.write("""\
    ]
}
""")

sys.stderr.write(f"Generated {len(hands_down_rules)} sub-rules in {output_name}\n\n")
sys.stderr.write("Try running this to add the rules to Karabiner Elements:\n\n")
sys.stderr.write(
    f"cp {output_name} ~/.config/karabiner/assets/complex_modifications/\n\n"
)
sys.stderr.write("Then open 'Karabiner Elements', select 'Complex Modifications',\n")
sys.stderr.write("click 'Add predefined rule', scroll down to find the new\n")
sys.stderr.write(f"'{title}'\n")
sys.stderr.write("block. Click enable all.")
