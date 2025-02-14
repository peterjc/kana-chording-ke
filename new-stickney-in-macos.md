This is a proof-of-principle implementation of the [New Stickney Japanese keyboard
layout](https://esrille.github.io/ibus-hiragana/en/layouts.html#new_stickney) on
on macOS via Karabiner Elements, which has been tested with the default Apple IME
in "Japanese - Kana" mode.

Python script `cursor-chording-flick-input.py` generates the verbose JSON file
`cursor-chording-flick-input.json` which you can import into Karabiner Elements.
The rules are conditional on being in "Japanese - Kana" input mode, so do not
alter the normal ABC (Qwerty) usage, nor currently "Japanese - Romaji" input.

This should work on any Qwerty layout keyboard, but has been tested on an Apple
MacBook Japanese keyboard, and a GB ISO external keyboard. ANSI keyboards should
work but there may be some minor issues with the punctuation keys.
