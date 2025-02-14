This is a proof-of-principle implementation of the [New Stickney Japanese keyboard
layout](https://esrille.github.io/ibus-hiragana/en/layouts.html#new_stickney) on
on macOS via Karabiner Elements, which has been tested with the default Apple IME
in "Japanese - Kana" mode.

This should work on any Qwerty layout keyboard, but has been tested on an Apple
MacBook Japanese keyboard, and a GB ISO external keyboard. ANSI keyboards should
work but there may be some minor issues with the punctuation keys.

# Installation

The rule has not yet been added to https://ke-complex-modifications.pqrs.org/
so for now save [new-stickney-in-macos.json](https://github.com/peterjc/kana-chording-ke/raw/refs/heads/main/new-stickney-in-macos.json) to `~/.config/karabiner/assets/complex_modifications/`

# Implementation

Python script `cursor-chording-flick-input.py` generates the verbose JSON file
`cursor-chording-flick-input.json` which you can import into Karabiner Elements.
The rules are conditional on being in "Japanese - Kana" input mode, so they do not
alter the normal ABC (Qwerty) usage, nor currently "Japanese - Romaji" input.

The rule for using the spacebar as a central sticky-shift key (where you can press
it once and the next character is shifted, or hold it down like a traditional shift)
has been created separately from the kana-remapping rules as this is something the
user may wish to experiment with (e.g. using this as a shift in ordinary mode?).


