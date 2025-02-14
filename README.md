This repository is a holding point for assorted keyboard layout experiments
focused on Japanese text entry, and in particular the possibilities offered
by keyboard chording. Currently this is focused on in-software keyboard
modification on macOS using the free open source software [Karabiner
Elements](https://karabiner-elements.pqrs.org/), but many of the ideas could
equally be done with a programmable keyboard.

# Projects

Currently there are two main sub-projects:

* [Flick-input like Japanese keyboard chording using cursor
  keys](cursor-chording-flick-input.md) where for example the `k` or `か`
  (ka) key alone gives か, but in combination with `←`, `↑`, `↓`, or `→`
  gives き, く, け, or こ (ki, ku, ke, ko) mimicking the touch-screen iOS
  12-key flick input.

* [New Stickney Japanese keyboard layout](new-stickney-in-macos.md) where
  for example Qwerty `q` with the standard JIS layout gives `た`, but is
  remapped to `f` in order to give `け` as per the New Stickney layout.
  The standard JIS kana layout uses four rows of keys (including the
  numberpad; small kana are typed using shift), while New Stickney is more
  ergonomic using only three rows (small kana are typed using the `゛`
  post-modifier).

# Japanese character entry

There are at least three ways to enter Japanese hiragana or katakana (and
in some cases kanji) on computers which I have tested on macOS:

1. There are operating system specific keyboard expressions to enter the hex
   code of an individual unicde symbol which can be used for kana or even kanji.
   See [hex codes for kana in unicode](http://www.i18nguy.com/unicode/hiragana.html).
   For macOS, once in "*Unicode Hex Input*" mode, to enter け (ke), press-and-hold
   the option key (aka alt), then type `3`, `0`, `5`, `1`, and release the option
   key. The top number row or the number pad can be used. The same trick works for
   emoji too, usually eight digits, and can be done from KE. Unfortunately, using
   "Unicode Hex Input" mode has the significant drawback that you won't get access
   to the OS IME for kanji support.

2. If instead we use "*Japanese - Romaji*" mode, we must map the desired kana to
   any of the supported romaji aliases, and send that key sequence. Thus for `け`
   we send `k` then `e`. We can send upper case `K` then `E` which can be
   configured in the macOS Japanese settings to be treated automatically as
   the katakana `ケ`. In this mode to enter coffee we would want to simulate
   pressing `K` `O` `-` `H` `I` `-` giving `コーヒー` as you typed. Here is
   a great [introduction to typing in romaji
   mode](https://www.tofugu.com/japanese/how-to-type-in-japanese/) which
   covers this and more.

3. Alternatively, in "*Japanese - Kana*" mode, we must map the desired kana to
   the physical key on the macOS Japanese keyboard JIS layout, and send that
   keycode. In the default JIS layout `け` corresponds to the ANSI Qwerty semi-colon
   key `:` so we send that. For `げ`, we must also send the `◌゙` (ten-ten or
   dakuten) as the `@` key. Likewise `◌゚ ` (adding maru or handakuten) is on the
   `[` key. In this mode the shift key gives the small form of the vowels
   `a`/`i`/`u`/`e`/`o`, `tsu` or `ya`/`yu`/`yo`, and toggles the `わ` key to
   `を` (key zero).

Note Karabiner Elements rules can be conditional on the current input mode.
