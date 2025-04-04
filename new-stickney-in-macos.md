This is a proof-of-principle implementation of the [New Stickney Japanese keyboard
layout](https://esrille.github.io/ibus-hiragana/en/layouts.html#new_stickney)
([version 17](https://github.com/esrille/new-stickney)) on macOS via Karabiner
Elements, which has been tested with the default Apple IME in "Japanese - Kana"
mode.

This should work on any Qwerty layout keyboard, but has been tested on an Apple
MacBook Japanese keyboard, and a GB ISO external keyboard. ANSI keyboards should
work but there may be some minor issues with the punctuation keys.

It should also work on a 30 key reduced Qwerty layout - as shown here as a matrix
with the Qwerty key, base kana, and shifted kana. Left hand:

|     1    |   2    |     3    |     4   |     5    |
|--------:|---------:|--------:|--------:|---------:|
| `Q` → `け❌` | `W` → `く゜` | `E` → `すひ` | `R` → `さふ` | `T` → `つ❌` |
| `A` → `はや` | `S` → `かそ` | `D` → `しせ` | `F` → `たへ` | `G` → `てほ` |
| `Z` → `よゆ` | `X` → `きゐ` | `C` → `こ❌` | `V` → `とゑ` | `B` → `ち❌` |

Right hand:

|     6   |     7   |     8    |     9   |    0    |
|--------:|--------:|---------:|--------:|--------:|
| `Y` → `ぬむ` | `U` → `おえ` | `I` → `のも` | `O` → `にみ` | `P` → `ねめ` |
| `H` → `られ` | `J` → `うる` | `K` → `いり` | `L` → `゛あ` | `;` → `なま` |
| `N` → `っろ` | `M` → `んー` | `,` → `、を` | `.` → `。わ` | `/` → `・？` |

Four of the shifted keys are currently unused (shown as `❌`). The layout also
follows romaji mode in mapping `[` and `]` to `「` and `」` for quotation
(keys off to the right - their location depends on ANSI vs ISO vs JIS
keyboard type).

# Installation

The rule has not yet been added to https://ke-complex-modifications.pqrs.org/
so for now save [new-stickney-in-macos.json](https://github.com/peterjc/kana-chording-ke/raw/refs/heads/main/new-stickney-in-macos.json) to `~/.config/karabiner/assets/complex_modifications/`

Then open Karabiner Elements, select "Complex Modifications" from the left hand
column, and click "Add predefined rule", which should show a screen like this
(sorted alphabetically):

![Screenshot 2025-02-14 at 12 23 40](https://github.com/user-attachments/assets/4c99e2a4-c04d-404c-b267-3ea29417b688)

Find "New Stickney Japanese Kana Layout in macOS" and click "Enable" on the
"Core Mappings" and *one* of the spacebar as central-shift rules (see below).

If not already installed, add "Japanese - Kana" mode.

Switch to "Japanese - Kana" mode and start typing!

# Spacebar

Two alternative rules are provided for using the spacebar as a central shift:

* "Space is sticky left-shift" - You can press it once and the next character is
   shifted, or hold it down like a traditional shift. This aims to follow the New
   Stickney behaviour as documented for the (Linux) Hiragana IME.
* "Hold space (alone) for left-shift" - You can still tap the spacebar to act as
  space, or use shift-space, both of which are useful with the default macOS IME.

Note currently the Qwerty quote (ANSI/ISO) or colon (JIS) is assigned to `変換`
in New Stickney, but here currently just acts as space.

# Implementation

This works detecting by remapping keys like `q` so that rather than the IME
turning this into た as per the JIS layout, Karabiner elements replaces it with
`f` to that the IME turns this into け as per the New Stickney layout.

Python script [cursor-chording-flick-input.py](cursor-chording-flick-input.py)
generates the verbose JSON file
[cursor-chording-flick-input.json](cursor-chording-flick-input.json) which you can
import into Karabiner Elements.

The rules are conditional on being in "Japanese - Kana" input mode, so they do not
alter the normal ABC (Qwerty) usage, nor currently "Japanese - Romaji" input.

Many of the kana on the JIS layout are on what are punctuation keys in Qwerty
layouts, and some of these keys differ between the ANSI/ISO/JIS physical keyboards.
Also, the New Stickney layout leaves the number row and symbols to the underlying
locale. This means some of the re-mapping rules are ANSI/IOS/JIS mode specific
(Karabiner Elements has a notational mode for their virtual keyboard device).

The standard JIS layout uses the shift key to enter enter "ぁぃぅぇぉゃゅょ" (small
vowel sounds). In this layout you type the corresponding large character from
"あいうえおやゆよ" and then press `゛` (Qwerty letter `L`).  This is done in KE with
a variable to track which vowel is wanted and sending backspace and the shifted key.

The New Stickney layout leaves the top number/symbol row largely unchanged.
However, they are used as a fourth row of kana in the JIS layout. These keys are
therefore remapped to option (alt) equivalents giving wide versions of the expected
characters. We could map to the numberpad keys instead which seems to give narrow
number characters.

# Limitations

New Stickney maps `[` and `]` to `「` and `」` for quotation, and that works -
with the caveat that which keys should be used is only specified for ANSI/JIS
(which differ) and not ISO (which could follow the placement of either). With
shift (where Qwerty would give `{` and `}`), these should be `『` and `』`. As
far as I am aware, in macOS "Japanese - Kana" input mode we can only type one of
these (`『` using shift+option).
