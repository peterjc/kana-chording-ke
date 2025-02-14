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

Then open Karabiner Elements, select "Complex Modifications" from the left hand
column, and click "Add predefined rule", which should show a screen like this
(sorted alphabetically):

![Screenshot 2025-02-14 at 12 23 40](https://github.com/user-attachments/assets/4c99e2a4-c04d-404c-b267-3ea29417b688)

Find "New Stickney Japanese Kana Layout in macOS" and click "Enable All".

If not already installed, add "Japanese - Kana" mode.

Switch to "Japanese - Kana" mode and start typing!

# Implementation

Python script `cursor-chording-flick-input.py` generates the verbose JSON file
`cursor-chording-flick-input.json` which you can import into Karabiner Elements.
The rules are conditional on being in "Japanese - Kana" input mode, so they do not
alter the normal ABC (Qwerty) usage, nor currently "Japanese - Romaji" input.

Many of the kana on the JIS layout are on what are punctuation keys in Qwerty
layouts, and some of these keys differ between the ANSI/ISO/JIS physical keyboards.
Also, the New Stickney layout leaves the number row and symbols to the underlying
locale. This means some of the re-mapping rules are ANSI/IOS/JIS mode specific
(Karabiner Elements has a notational mode for their virtual keyboard device).

The rule for using the spacebar as a central sticky-shift key (where you can press
it once and the next character is shifted, or hold it down like a traditional shift)
has been created separately from the kana-remapping rules as this is something the
user may wish to experiment with (e.g. using this as a shift in ordinary mode?).


