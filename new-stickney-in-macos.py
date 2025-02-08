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

The small tsu "っ" (sokuon) is an exception, and does still get its own key in
the New Stickney layout due to its higher usage (double consanants in romaji
mode). That is the same as JIS, so a simple remapping. Likewise in romaji mode
we can remap to send `xtu` or `ltu` (or sent `x` or `l` if used as a prefix).

Third complication: Karabiner Elements can set the virtual keyboard to one of
ANSI, ISO, and JIS. Using ISO messes up the mappings using the `international1`
key (for "ろ") and `international3` (for "ー") keys, and assorted punctuation
keys (`equal_sign` for "へ", `backslash` for "む" and `close_bracket` for "゜").
*Running in JIS mode is required*.

https://karabiner-elements.pqrs.org/docs/manual/configuration/configure-keyboard-type/

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
    "っ❌❌❌❌❌❌、。・❌"  # bottom row (11 keys)
)
# Using option in kana mode gives "wide ASCII" versions of the QWERTY layout,
# https://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms_(Unicode_block)
# Except where it seems to trigger a shortcut of some kind (R, AS, ZXC).
# Note fixed ＂ and ＇ from smart quotes, also －, but others as typed.
# With these we can map the New Stickney number row to numbers and symbols.
#
jis_japanese_shift_option = (  # in kana mode!!!
    "！＂＃＄％＆＇（）０＝〜｜"  # number row (13 keys), smart quotes reverted
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
    "❌❌❌❌❌❌❌❌❌❌❌〜｜"  # number row unchanged (13 keys)
    "❌゜ひふ❌むえもみめ…『"  # top row (12 keys)
    "やそせへほれるりあま　』"  # home row (12 keys)
    "ゆゐ❌ゑ❌ろーをわ？❌"  # bottom row (11 keys)
)
# Here will map unused ❌ number row to the JIS option/fn
# and option/shift row of wide numbers and symbols, and
# for the five punctuation map to JIS kana mode usage.
# [Note this is New Stickney on JIS, on ANSI shows tilde top left,
# and moves the quotes to follow the curly and square brackets.]
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
# See https://karabiner-elements.pqrs.org/docs/help/troubleshooting/symbols-with-non-ansi-keyboard/
ke_key_names = {
    # Differ in JIS vs ANSI/ISO, see JIS_TO_ISO_ANSI_NAME
    "¥": "international3",
    "_": "international1",
    # QWERTYUIOP@[ on Japanese, ...P[] on ANSI and UK.
    "@": "open_bracket",  # Used for in ゛ JIS, but in NS only ellipsis with shift?
    "[": "close_bracket",  # Used for in ゜ JIS, but 「 in NS (and 『 with shift)
    # ASDFGHJKL;:] on Japanese, ...HJKL;' only on ANSI, ...HJKL;'# on UK
    "]": "backslash",  # Used for む in JIS, but 」in NS (and 』with shift)
    # "]": "non_us_pound",  # Used for む and with shift 」in JIS, but 」in NS (and 』with shift)
    # Same in JIS/ANSI/ISO
    "-": "hyphen",
    "^": "equal_sign",
    ";": "semicolon",
    ":": "quote",
    ",": "comma",
    ".": "period",
    "/": "slash",
    " ": "spacebar",
}

# What to simulate pressing in ISO/ANSI mode, because the key we wanted was JIS only:
ISO_ANSI_SPECIAL = {
    # shift+n -> "ろ" but international1 is JIS specific, so use alternative:
    "ろ": '{"key_code": "quote", "modifiers": ["shift"]}',
    # shift+w -> "゜" but brackets etc move between JIS and ISO/ANSI (shared with "「"):
    "゜": '{"key_code": "equal_sign"}',
    # shift+[ -> "「" but brackets etc move on JIS vs ISO/ANSI
    "「": '{"key_code": "equal_sign", "modifiers": ["shift"]}',
    # shift+] -> "」" but brackets etc move on JIS vs ISO/ANSI
    "」": '{"key_code": "open_bracket", "modifiers": ["shift"]}',
    # "『": '{"key_code": "open_bracket", "modifiers": ["shift", "option"]}',
    # shift+m -> "ー" using international3 is JIS specific, so use an alternative
    "ー": '{"key_code": "hyphen", "modifiers": ["option"]}',
    "＿": '{"key_code": "hyphen", "modifiers": ["shift", "option"]}',
    "￥": '{"key_code": "non_us_pound", "modifiers": ["option"]}',
    "｜": '{"key_code": "non_us_pound", "modifiers": ["shift", "option"]}',
    "〜": '{"key_code": "non_us_backslash", "modifiers": ["shift"]}',
}

kana_conditions = '"conditions": [{"input_sources": [{ "input_source_id": "com.apple.inputmethod.Kotoeri.KanaTyping.Japanese" }], "type": "input_source_if"}]'
kana_JIS_conditions = '"conditions": [{"input_sources": [{ "input_source_id": "com.apple.inputmethod.Kotoeri.KanaTyping.Japanese" }], "type": "input_source_if"}, {"keyboard_types": ["jis"], "type": "keyboard_type_if"}]'
kana_not_JIS_conditions = '"conditions": [{"input_sources": [{ "input_source_id": "com.apple.inputmethod.Kotoeri.KanaTyping.Japanese" }], "type": "input_source_if"}, {"keyboard_types": ["ansi", "iso"], "type": "keyboard_type_if"}]'

# Compared to ANSI and ISO, JIS has an extra ろ key bottom right.
# Compared to ANSI, JIS has an extra ￥ key top right (between equal_sign and backspace),
# Compared to ANSI, ISO has an extra \ key bottom left (between left-sift and Z).
# Will do some matching up (far left ISO -> far right JIS, same row)
ISO_MAPPINGS = {
    # This is the # sign between ' and enter on a UK keyboard. The JIS enter key
    # is the shape here is the same as JIS keyboards so will ise this for "」"
    "non_us_pound": "」",
    # This is the slash/broken-pipe bottom left between left-shift and Z on
    # a UK keyboard, also known as the ISO key. Map to JIS ろ key bottom.
    "non_us_backslash": "＿",
    # This is the top left back-tick and pipe on a UK keyboard. There is a key
    # here on both JIS (New Stickney uses it for あ/A) and ANSI keyboards (where
    # New Stickney uses it for ellipsis/tilde). My Japanese MacBook has no key
    # here (but has dedicated switching keys). In JIS Kana mode, it gives §±
    # which is useless. Treat like JIS top right ￥ and pipe.
    "grave_accent_and_tilde": "￥",
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


def _to_key_code_and_mods(kana: str) -> tuple[str, str]:
    """Helper function before look at JIS vs ISO/ANSI."""
    # No mods needed in JIS jana:
    index = jis_japanese_normal.find(kana)
    if index >= 0:
        return jis_qwerty[index], ""
    # Shift needed in JIS kana
    index = jis_japanese_shift.find(kana)
    if index >= 0:
        return jis_qwerty[index], '"modifiers": ["shift"]'
    # fn+option in JIS kana (wide numbers)
    index = jis_japanese_fn_option.find(kana)
    if index >= 0:
        return jis_qwerty[index], '"modifiers": ["fn", "option"]'
    # Shift+option in JIS kana (punctuation)
    index = jis_japanese_shift_option.find(kana)
    if index >= 0:
        return jis_qwerty[index], '"modifiers": ["shift", "option"]'
    raise KeyError(kana)


def to_key_using_jis_kana_mode(kana: str) -> str:
    """Build KE to-event keycode string to type given character in ISO/ANSI kana mode."""
    if kana == unused:
        return no_op_to_action
    try:
        key_code, modifiers = _to_key_code_and_mods(kana)
        key_name = ke_key_name(key_code)
        if modifiers:
            return f'{{"key_code": "{key_name}", {modifiers}}}'
        else:
            return f'{{"key_code": "{key_name}"}}'
    except KeyError:
        # Fall back of last resort - used to disable wyi, wye
        return no_jis[kana]


_ = to_key_using_jis_kana_mode("０")
assert _ == '{"key_code": "0", "modifiers": ["fn", "option"]}', _
_ = to_key_using_jis_kana_mode("、")
assert _ == '{"key_code": "comma", "modifiers": ["shift"]}', _
_ = to_key_using_jis_kana_mode("を")
assert _ == '{"key_code": "0", "modifiers": ["shift"]}', _
_ = to_key_using_jis_kana_mode("え")
assert _ == '{"key_code": "5"}', _
_ = to_key_using_jis_kana_mode("＆")  # wide &
assert _ == '{"key_code": "6", "modifiers": ["shift", "option"]}', _
_ = to_key_using_jis_kana_mode("＇")  # wide '
assert _ == '{"key_code": "7", "modifiers": ["shift", "option"]}', _
_ = to_key_using_jis_kana_mode("（")  # wide (
assert _ == '{"key_code": "8", "modifiers": ["shift", "option"]}', _
_ = to_key_using_jis_kana_mode("）")  # wide )
assert _ == '{"key_code": "9", "modifiers": ["shift", "option"]}', _
_ = to_key_using_jis_kana_mode("む")
assert _ == ('{"key_code": "backslash"}'), _
_ = to_key_using_jis_kana_mode("゜")
assert _ == '{"key_code": "close_bracket"}', _
_ = to_key_using_jis_kana_mode("へ")
assert _ == '{"key_code": "equal_sign"}', _
_ = to_key_using_jis_kana_mode("ろ")
assert _ == '{"key_code": "international1"}', _
_ = to_key_using_jis_kana_mode("ー")
assert _ == '{"key_code": "international3"}', _
del _

# Problems seen when Karabiner Elements Virtual Decive in ISO mode (use JIS):
# shift+6 should give &, getting  etc.
# shift+7 should give ', getting ＆ etc.
# shift+w should give maru ゜ (aka "close_bracket"), getting mu む
# shift+f should give he へ (aka "equal_sign"), but getting maru　゜
# shift+y should give mu む (aka "backslash"), but getting he へ
# shift+n should give ro ろ (aka "international1"), getting nothing
# shift+m should give onbiki ー (aka "international3"), getting nothing


def build_stickney_to_jis_kana_map():
    for key_name, kana in ISO_MAPPINGS.items():
        # These are "extra" keys on ISO keyboards not on JIS
        to_rule = to_key_using_jis_kana_mode(kana)
        print(f"Mapping ISO {key_name} to {kana} using {to_rule}")
        yield f"""\
                {{
                    "type": "basic",
                    "from": {{"key_code": "{key_name}"}},
                    "to": [{to_rule}],
                    {kana_JIS_conditions if kana in ISO_ANSI_SPECIAL else kana_conditions},
                    "description": "ISO {key_name} to {kana}"
                }}
        """
        if kana in ISO_ANSI_SPECIAL:
            assert kana not in no_jis, kana
            # Need a second version for ISO/JIS
            to_rule = ISO_ANSI_SPECIAL[kana]
            print(f"Mapping ISO {key_name} to {kana} using ISO {to_rule}")
            yield f"""\
                {{
                    "type": "basic",
                    "from": {{"key_code": "{key_name}"}},
                    "to": [{to_rule}],
                    {kana_JIS_conditions if kana in ISO_ANSI_SPECIAL else kana_conditions},
                    "description": "ISO {key_name} to {kana}"
                }}
            """
        # And with shift...
        kana = new_stickney_shift[new_stickney_normal.index(kana)]
        to_rule = to_key_using_jis_kana_mode(kana)
        print(f"Mapping ISO shift+{key_name} to {kana} using {to_rule}")
        yield f"""\
                {{
                    "type": "basic",
                    "from": {{"key_code": "{key_name}", "modifiers": {{ "mandatory": ["shift"] }} }},
                    "to": [{to_rule}],
                    {kana_JIS_conditions if kana in ISO_ANSI_SPECIAL else kana_conditions},
                    "description": "ISO {key_name} to {kana}"
                }}
        """
        if kana in ISO_ANSI_SPECIAL:
            assert kana not in no_jis, kana
            # Need a second version for ISO/JIS
            to_rule = ISO_ANSI_SPECIAL[kana]
            print(f"Mapping ISO shift+{key_name} to {kana} using ISO {to_rule}")
            yield f"""\
                {{
                    "type": "basic",
                    "from": {{"key_code": "{key_name}", "modifiers": {{ "mandatory": ["shift"] }} }},
                    "to": [{to_rule}],
                    {kana_JIS_conditions if kana in ISO_ANSI_SPECIAL else kana_conditions},
                    "description": "ISO {key_name} to {kana}"
                }}
            """
    # return
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

            if kana == "ろ":
                assert (
                    from_rule
                    == '{"key_code": "n", "modifiers": { "mandatory": ["shift"] } }'
                ), from_rule
            elif kana == "』":
                assert (
                    from_rule
                    == '{"key_code": "backslash", "modifiers": { "mandatory": ["shift"] } }'
                )
                assert to_rule == no_op_to_action, to_rule

            # Usually universal, but could be JIS specific:
            yield f"""\
                {{
                    "type": "basic",
                    "from": {from_rule},
                    "to": [{to_rule}],
                    {kana_JIS_conditions if kana in ISO_ANSI_SPECIAL else kana_conditions},
                    "description": "{qwerty_name} to {kana}"
                }}
"""
            if kana in ISO_ANSI_SPECIAL:
                assert kana not in no_jis, kana
                # Need a second version for ISO/JIS
                to_rule = ISO_ANSI_SPECIAL[kana]
                yield f"""\
                {{
                    "type": "basic",
                    "from": {from_rule},
                    "to": [{to_rule}],
                    {kana_not_JIS_conditions},
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
"""
    )

    if romaji_rules:
        handle.write(
            f"""\
        {{
            "description": "{romaji_rules_description}",
            "manipulators": [
"""
            + ",\n".join(_.rstrip() for _ in romaji_rules)
            + """\n
            ]
        },
"""
        )
    handle.write(
        f"""\
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
