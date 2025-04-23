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
"""Generate Karabiner Elements JSON for Hands Down layout on a JIS MacBook.

The Apple MacBook sold in Japan has a JIS based keyboard layout which has a
quite different bottom row compared to Apple's ANSI/US or ISO/European layouts).
In particular, the spacebar is shorter - just over three keys wide and found
underneath the Qwerty VBN keys. It is flanked on the by the "eisuu" (switch to
qwerty) and "kana" (switch to Japanese mode) keys. This is important as it
offers a way to use this bottom row for thumb keys, like the letter "R" as
used on the left-thumb in many of the "Hands Down" alternative layouts.

This allows us to remap the letter keys while still using the same home row
(although we will use a "wide mod" and shift the hands further apart), while
using (left-command), "eisuu" and spacebar for the left thumb, and "kana",
right-command (and globe/fn?) for the right thumb keys. The number row is
deliberately not altered.

The specific layout I am using is a personal variant of "Hands Down Promethium"
(top/bottom inverted, minor letters moved about) with the punctuation placement
partly based on "Enthium" (top/bottom inverted, unmirrored).

The KE rules are deliberately defined not to be active in Japanese mode,
meaning Kana mode should still work, as will Romaji-Qwerty mode (although
you might want to type romaji using Hands Down?).

This assumes the Karabiner Elements virtual device will be in JIS mode
(important for punctuation to work as expected - but not done yet!).
"""

import sys

script_version = "0.0"

# These are the keys are reported by Karabiner Elements (not JIS layout)
# excluding the function row, number row, enter key, globe/fn, and cursors.
jis_qwerty = (
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
    "left_control",
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
# For both left and right, core is three rows of five, plus thumbs
# We have a 2 (or 3?) dead zone between the two hands (for punctuation? Q, Z?)
# Bottom row is left-shift, left-option, left-command, eisuu, spacebar,
# kana, right-command, (then globe/fn but cannot remap that, and cursors).
hands_down = (
    # Top row:
    "v",
    "p",
    "g",
    "m",
    "x",
    "❌",
    "❌",
    # "❌",
    "slash",
    "period",
    "quote",
    "hyphen",
    "equal_sign",
    "delete_or_backspace",
    # Home row:
    "s",
    "n",
    "t",
    "h",
    "k",
    "❌",
    "❌",
    # "❌",
    "comma",
    "a",
    "e",
    "i",
    "c",
    "q",
    # Bottom row:
    "b",
    "f",
    "d",
    "l",
    "j",
    "❌",
    "❌",
    # "❌",
    "semicolon",
    "u",
    "o",
    "y",
    "w",
    "z",
    # Thumb row:
    "left_control",
    "🔻",  # i.e. left_option
    "🔻",  # i.e. left_command
    "r",
    "delete_or_backspace",
    "spacebar",
    "left_shift",
)
unused = "❌"  # map to no-op
leave = "🔻"  # do not remap (transparent in Vial layer terminology)

assert len(jis_qwerty) == len(hands_down) == 3 * 13 + 7, (
    f"{len(jis_qwerty)} vs {len(hands_down)} vs {3 * 13 + 7}"
)

output_name = "hands-down-on-jis-macbook.json"
title = f"Hands Down Promethium (inverted personal variant) on Japanese MacBook (KE rules version {script_version})"
rules_description = (
    "Hands Down Promethium variant on JIS layout in non-Japanese input mode"
)

# Want to exclude "input_source_id": "com.apple.inputmethod.Kotoeri.KanaTyping.Japanese"
# and "input_source_id": "com.apple.inputmethod.Kotoeri.RomajiTyping.Japanese",
# allow "input_source_id": "com.apple.keylayout.ABC", or "language": "en"?
# Can we cope with ANSI/ISO/JIS for the punctuation? Initially require JIS
input_source_condition = '"conditions": [{"input_sources": [{ "input_source_id": "com.apple.keylayout.ABC" }], "type": "input_source_if"}, {"keyboard_types": ["jis"], "type": "keyboard_type_if"}]'


def build_hands_down_to_jis_qwerty_map():
    for hd_key, jis_key in zip(hands_down, jis_qwerty):
        if hd_key == leave:
            continue
        if hd_key == unused:
            hd_key = "delete_or_backspace"  # placeholder
        yield f"""\
                {{
                    "type": "basic",
                    "from": {{"key_code": "{jis_key}", "modifiers": {{"optional": ["any"]}}}},
                    "to": [{{"key_code": "{hd_key}"}}],
                    {input_source_condition},
                    "description": "Get {hd_key} when press {jis_key}"
                }}
"""


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
sys.stderr.write(f"'{title}' block. Click enable (or enable all).")
