# Hands Down Promethium on Japanese Apple Keyboard

## Concept

[Karabiner Elements](https://karabiner-elements.pqrs.org/) is a free open
source keyboard remapping tool for macOS. The [Hands Down Layout
variations](https://sites.google.com/alanreiser.com/handsdown) are a
family of alternatives to Qwerty, primarily designed for English.
[Hands Down Promethium](https://www.reddit.com/r/KeyboardLayouts/comments/1g66ivi/hands_down_promethium_snth_meets_hd_silverengram/)
released in late 2024 on *Reddit Keyboard Layouts* is intended for split
keyboards with the letter R and space on thumb keys.

The Apple MacBook sold in Japan has a keyboard with a short spacebar (just
over three keys wide, underneath the Qwerty VBN keys), flanked on the by
the "eisuu" (switch to qwerty) and "kana" (switch to Japanese mode) keys.

This lets us remap the Japanese MacBook keyboard into three rows of five
per hand with two keys per thumb:

* The left hand still uses the conventional home-keys (Qwerty ASDF), with
  "eisuu" and space-bar as thumb keys. We apply a "wide mod" to the bottom
  row, but with JIS and ANSI keyboards lacking the ISO key between
  left-shift and Z, we map left-shift to a letter instead.
* In order to have thumb-keys the right hand we must use a "wide mod" and
  move the home position *two* columns further right (starting at Qwerty L),
  with "kana" and right-command for the right thumb keys, and right-shift
  mapped to a letter. Enter becomes an easy horizontal pinkie move.

The canonical Hands Down Promethium layout places Q and Z far right in a
sixth column - but the Hands Down layouts are often used on ergonomic
split keyboards with only five columns for each hand, with Q and Z via
a layer or chording. Here they are moved to the top right corner in favour
of hyphen and equals (which are in the right-hand's core 5x3 block instead),
and placed far right on the navigation layer.

This leaves a 2-2-3 central block (Qwerty YU, HJ, and BNM) into which the
punctuation typically on the right is transplanted (same row and order).
This allows all the letter and punctuation keys to remain on the base
layer, allowing the keyboard to be used without layers or chording combos.

The KE rules are deliberately defined not to be active in Japanese mode,
meaning Kana mode should still work, as will Romaji-Qwerty mode (although
you might want to type romaji using Hands Down?).

## Core Layout

This is my personal variant of the top/bottom row inverted Hands Down
Promethium layout. Left 5 columns, thumbs are R and backspace:

1 | 2 | 3 | 4 | 5
--|---|---|---|--
V | P | G | M | X
S | N | T | H | K
B | F | D | L | J

Right 5 (or 6) columns, thumbs are shift and spacebar:

1 | 2 | 3 | 4 | 5 | 6
--|---|---|---|---|--
/ | . | ' | - | = | 
, | A | E | I | C | Q
; | U | O | Y | W | Z

As described above, here Q & Z are placed on the Apple keyboard's number row
between the zero and backspace.

## Chording Combos

Pressing two horizontally adjacent keys together by moving the hand inwards
(since these keys are normally pressed by the index finger), left hand for
open brackets/braces:

* `M` + `X` for `{` (Qwerty `R` and `T`)
* `H` + `K` for `(`
* `L` + `J` for `[`

Matching right hand combos for closing brackets/braces:

* `/` + `.` for `{` (Qwerty `I` and `O`)
* `,` + `A` for `(`
* `;` + `U` for `[`

etc...
