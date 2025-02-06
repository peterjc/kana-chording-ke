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
"""Generate Karabina Elements JSON for using New Stickney kana layout on macOS.

There is built in support for both kana and romaji Japanese input on macOS. The
goal of these Karabiner Elements rules is to use a New Stickney kana layout and
have Karabiner Elements remap the keypresses in in Japanese input mode.

* https://esrille.github.io/ibus-hiragana/layouts.html#new_stickney
* https://esrille.github.io/ibus-hiragana/en/layouts.html#new_stickney

For example, the Qwery key `a` is the kana "た" (ta) in the JIS kana layout, but
"け" (ke) in the New Stickney layout. We must therefore remap the Qwerty key "a"
to the two key presses `k` `e` in romaji mode, or `shift`+`;` (i.e. ":") if in
kana mode reflecting the JIS kana layout.

First complication: The numbers/symbols row is part of the JIS kana layout, but
for New Stickney it is implicitly left as numbers/sybmols. In romaji mode we
need do nothing, but in kana mode unless stopped those keys would give JIS kana.
Therefore we map these to option modifier versions which in macOS kana mode
gives wide versions of the ASCII numbers and symbols.

Second complication: The New Stickney layout's handling of small kana (sutegana
or Kogaki moji) via the ten-ten key AFTER the kana. This is not supported by the
macOS IME. We need a complex (fragile?) dead-key like set of rules, perhaps
sending backspace(s) and then the small kana equivalent.

The small tsu "っ" is an exception, and does still get its own key in the New
Stickney layout due to its higher usage (double consanants in romaji mode). That
is the same as JIS, so a simple remapping. Likewise in romaji mode we can remap
to send `xtu` or `ltu` (or sent `x` or `l` if used as a prefix).

Open questions:

* The "変換" key (conversion or wide space - on the USA single-quote key, or JIS
layout colon): Does it have a macOS Kana entry mode equivalent?
* Center shift: Need to remap the space bar to shift (if held)?
* Other special mode keys: Leave them alone as per macOS kana entry?
"""

import sys

unused = "❌"  # wanted something double-width
daku = "がぎぐげござじずぜぞだぢづでどばびぶべぼ"
handaku = "ぱぴぷぺぽ"
kogaki = "ぁぃぅぇぉゃゅょ"  # excluding small tsu "っ" and no small ka or ke "ヵヶ"


# As typed on Japanese Apple MacBook keyboard
jis_qwerty = (
    "1234567890-^¥"  # number row (13 keys)
    "qwertyuiop@["  # top row (12 keys)
    "asdfghjkl;:]"  # home row (12 keys)
    "zxcvbnm,./_"  # bottom row (11 keys)
)
jis_qwerty_shifted = (
    "!\"#$%&'()0=~|"  # number row (13 keys)
    "QWERTYUIOP`{"  # top row (12 keys)
    "ASDFGHJKL+*}"  # home row (12 keys)
    "ZXCVBNM<>?_"  # bottom row (11 keys)
)
# Nothing critical here, except perhaps euro sign:
# The top left slash "⁄" is wider than ASCII "/"?
jis_qwerty_option_shifted = (
    "⁄€‹›ﬁﬂ‡°·‚—±|"  # number row (13 keys)
    "Œ„´‰ˇÁ¨ˆØ∏”’"  # top row (12 keys)
    "ÅÍÎÏ˝ÓÔÒÚÆ»"  # home row (12 keys)
    "¸˛Ç◊ı˜Â¯˘¿`"  # bottom row (11 keys)
)

jis_japanese_normal = (
    "ぬふあうえおやゆよわほへー"  # number row (13 keys)
    "たていすかんなにらせ゛゜"  # top row (12 keys)
    "ちとしはきくまのりれけむ"  # home row (12 keys)
    "つさそひこみもねるめろ"  # bottom row (11 keys)
)
jis_japanese_shift = (
    "❌❌ぁぅぇぉゃゅょを❌❌❌"  # number row
    "❌❌ぃ❌❌❌❌❌❌❌❌「"  # top row (12 keys)
    "❌❌❌❌❌❌❌❌❌❌❌」"  # home row (12 keys)
    "っ❌❌❌❌❌❌❌、。・"  # bottom row (11 keys)
)
# Using option in kana mode gives "wide ASCII" versions of the QWERTY layout,
# https://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms_(Unicode_block)
# Except where it seems to trigger a shortcut of some kind (R, AS, ZXC).
# Note fixed ＂ and ＇ from smart quotes, also －, but others as typed.
# With these we can map the New Stickney number row to numbers and symbols.
#
jis_japanese_shift_option = (
    "！＂＃＄％＆＇（）０＝〜｜"  # number row (13 keys)
    "ＱＷＥ❌ＴＹＵＩＯＰ｀｛"  # top row (12 keys)
    "❌❌ＤＦＧＨＪＫＬ＋＊｝"  # home row (12 keys)
    "❌❌❌ＶＢＮＭ＜＞？＿"  # bottom row (11 keys)
)
jis_japanese_fn_option = (
    "１２３４５６７８９０－＾￥"  # number row (13 keys)
    "ｑｗｅｒｔｙｕｉｏｐ＠［"  # top row (12 keys)
    "ａｓｄｆｇｈｊｋｌ；：］"  # home row (12 keys)
    "ｚｘｃｖｂｎｍ、。・＿"  # bottom row (11 keys)
)

assert len(jis_qwerty) == len(jis_qwerty_shifted) == len(jis_qwerty_option_shifted)
assert len(jis_qwerty) == len(jis_japanese_normal) == len(jis_japanese_shift)
assert len(jis_qwerty) == len(jis_japanese_shift_option)

# These are as laid out on JIS keyboard, not USA (punctuation keys move)
# The "wide space" on the home row is actually the 変換 key
# (which should give a wide space when there is nothing to convert)
# The ❌ are not explicitly redefined, assuming follow JIS punctuation
# and QWERTY for the number row...
new_stickney_normal = (
    "❌❌❌❌❌❌❌❌❌❌❌❌￥"  # number row unchanged (13 keys)
    "けくすさつぬおのにね❌「"  # top row (12 keys)
    "はかしたてらうい゛な　」"  # home row includes ten-ten (12 keys)
    "よきことちっん、。・❌"  # bottom row (11 keys)
)
# Not sure there is a full-width Japanese three-dot ellipsis?
# I don't know how to type this or the double-quotes either.
new_stickney_shift = (
    "❌❌❌❌❌❌❌❌❌❌❌〜❌"  # number row unchanged (13 keys)
    "❌゜ひふ❌むえもみめ…『"  # top row (12 keys)
    "やそせへほれるりあま　』"  # home row (12 keys)
    "ゆゐ❌ゑ❌ろーをわ？❌"  # bottom row (11 keys)
)
# Here will map unused ❌ number row to the JIS option/fn
# and option/shift row of wide numbers and symbols, and
# for the five punctuation map to JIS kana mode usage.
new_stickney_normal = (
    "１２３４５６７８９０－＾￥"  # number row unchanged (13 keys)
    "けくすさつぬおのにね❌「"  # top row (12 keys)
    "はかしたてらうい゛な　」"  # home row includes ten-ten (12 keys)
    "よきことちっん、。・＿"  # bottom row (11 keys)
)
new_stickney_shift = (
    "！＂＃＄％＆＇（）－＝〜｜"  # wide symbols via option+shift (13 keys)
    "❌゜ひふ❌むえもみめ…『"  # top row (12 keys)
    "やそせへほれるりあま　』"  # home row (12 keys)
    "ゆゐ❌ゑ❌ろーをわ？＿"  # bottom row (11 keys)
)

assert len(new_stickney_normal) == len(new_stickney_shift)
assert len(new_stickney_normal) == len(new_stickney_shift) == len(jis_qwerty)

# no_op_to_action = '{"halt": true}'  # not valid
no_op_to_action = '{"set_variable": { "name": "kogaki", "value": ""}}'
no_jis = {
    "ゐ": no_op_to_action,  # Obsolete (wyi in romaji)
    "ゑ": no_op_to_action,  # Obsolete (wye in romaji)
    "　": '{"key_code": "spacebar"}',  # Use plain space to get wide space
    "…": no_op_to_action,  # How to enter in macOS kana mode?
    "『": no_op_to_action,  # How to enter in macOS kana mode?
    "』": no_op_to_action,  # How to enter in macOS kana mode?
}


output_name = "new-stickney-in-macos.json"
title = "New Stickney Japanese Kana Layout in macOS"
kana_rules_description = "New Stickney to JIS layout in Japanese Kana input mode"
romaji_rules_description = "New Stickney to JIS layout in Japanese Romaji input mode"


# JIS so rather different from USA ASCI layout:
ke_key_names = {
    "-": "hyphen",
    "^": "equal_sign",
    "¥": "international3",
    "@": "open_bracket",
    "[": "close_bracket",  # really!
    ";": "semicolon",
    ":": "quote",
    "]": "backslash",
    ",": "comma",
    ".": "period",
    "/": "slash",
    "_": "international1",
    " ": "spacebar",
}


def ke_key_name(character: str) -> str:
    return ke_key_names.get(character, character)


def from_key_using_ns_layout(kana: str) -> str:
    """Build KE from_key rule for a New Stickney character."""
    # Is this an un-shifted key on the NS layout:
    index = new_stickney_normal.find(kana)
    if index >= 0:
        return f'{{"key_code": "{ke_key_name(jis_qwerty[index])}"}}'
    # Should be a shifted-key on the NS layout:
    index = new_stickney_shift.find(kana)
    if index >= 0:
        return f'{{"key_code": "{ke_key_name(jis_qwerty[index])}", "modifiers": ["shift"]}}'


def to_key_using_jis_kana_mode(kana: str) -> str:
    """Build KE to-event keycode string to type given character in JIS kana mode."""
    if kana == unused:
        return no_op_to_action
    # No mods needed in JIS jana:
    index = jis_japanese_normal.find(kana)
    if index >= 0:
        return f'{{"key_code": "{ke_key_name(jis_qwerty[index])}"}}'
    # Shift needed in JIS kana
    index = jis_japanese_shift.find(kana)
    if index >= 0:
        return f'{{"key_code": "{ke_key_name(jis_qwerty[index])}", "modifiers": ["shift"]}}'
    # fn+option in JIS kana (wide numbers)
    index = jis_japanese_fn_option.find(kana)
    if index >= 0:
        return f'{{"key_code": "{ke_key_name(jis_qwerty[index])}", "modifiers": ["fn", "option"]}}'
    # Shift+option in JIS kana (punctuation)
    index = jis_japanese_shift_option.find(kana)
    if index >= 0:
        return f'{{"key_code": "{ke_key_name(jis_qwerty[index])}", "modifiers": ["shift", "option"]}}'
    # Fall back of last resort - used to disable wyi, wye
    return no_jis[kana]


assert (
    to_key_using_jis_kana_mode("０")
    == '{"key_code": "0", "modifiers": ["fn", "option"]}'
)


def build_stickney_to_jis_kana_map():
    for from_index, from_qwerty in enumerate(jis_qwerty):
        from_qwerty = ke_key_name(from_qwerty)
        for from_shift, kana, from_rule, qwerty_name in (
            (
                False,
                new_stickney_normal[from_index],
                f'{{"key_code": "{from_qwerty}"}}',
                from_qwerty,
            ),
            (
                True,
                new_stickney_shift[from_index],
                f'{{"key_code": "{from_qwerty}", "modifiers": {{ "mandatory": ["shift"] }} }}',
                "shift-" + from_qwerty,
            ),
        ):
            to_rule = to_key_using_jis_kana_mode(kana)
            if kana == unused:
                assert to_rule == no_op_to_action, f"{kana=} {from_rule=} {to_rule=}"

            # use jis_qwerty_shifted not from_qwerty.upper()
            # print(f"Kana '{kana}' : New Stickney {from_rule} -> {to_rule}")
            yield f"""\
                {{
                    "type": "basic",
                    "from": {from_rule},
                    "to": [{to_rule}],
                    "description": "{qwerty_name} to {kana}"
                }}
"""


romaji_rules = []
kana_rules = list(build_stickney_to_jis_kana_map())

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
            "description": "{romaji_rules_description}",
            "manipulators": [
"""
        + ",\n".join(_.rstrip() for _ in romaji_rules)
        + f"""\n
            ]
        }},
        {{
            "description": "{kana_rules_description}",
            "manipulators": [
"""
        + ",\n".join(_.rstrip() for _ in kana_rules)
        + """\n
            ]
        }
    ]
}
"""
    )

sys.stderr.write(f"Generated {len(romaji_rules)} romaji mode and {len(kana_rules)}")
sys.stderr.write(f" kana mode sub-rules in {output_name}\n\n")
sys.stderr.write("Try running this to add the rules to Karabiner Elements:\n\n")
sys.stderr.write(
    f"cp {output_name} ~/.config/karabiner/assets/complex_modifications/\n\n"
)
sys.stderr.write("Then open 'Karabiner Elements', select 'Complex Modifications',\n")
sys.stderr.write("click 'Add predefined rule', scroll down to find the new\n")
sys.stderr.write(f"'{title}' block with two\n")
sys.stderr.write("rule groups. Click enable (or enable all).")
