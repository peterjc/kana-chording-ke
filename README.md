# Kana-Chording-KE : Flick-input like Japanese keyboard chording

## Concept

By keyboard chording we mean pressing multiple keys at once to generate
characters. This idea has been applied to Japanese kana which are laided out
on a 5×10 grid (the gojūon, 五十音, "Fifty Sounds"), starting with the five
vowels (`a`, `i`, `u`, `e`, `o`, or `あ`, `い`, `う`, `え`, `お`), followed by
the `ka`-row (`ka`, `ki`, `ku`, `ke`, `ko`, or `か`, `き`, `く`, `け`, `こ`),
then the `sa`-row, etc. We can address any of the matrix positions with a
consonant row (`a`, `ka`, `sa`, `ta`, `na`, `ha`, `ma`, `ya`, `ra`, `wa`) and
vowel column. Thus combining `ha` and `i` gives `hi`, `は`＋`い`→`ひ`).

| あぁ　 | いぃ　 | うぅ　 | えぇ　 | おぉ　 |
|-------|-------|-------|-------|-------|
| かが　 | きぎ　 | くぐ　 | けげ　 | こご　 |
| さざ　 | しじ　 | すず　 | せぜ　 | そぞ　 |
| ただ　 | ちぢ 　| つづ　 | てで　 | とど　 |
| な　　 | に　　 | ぬ　　 | ね　　 | の　　 |
| はばぱ | ひびぴ | ふぶぷ | へべぺ | ほぼぽ |
| ま　　 | み　　 | む　　 | め　　 | も　　 |
| ら　　 | り 　　| る　　 | れ　　 | ろ　　 |
| やゃ　 |  　　　| ゆゅ　 |  　　　| よょ　 |
| わ　　 |　　　  | ん　　 | 　　　 | を　　 |

Plus っ (xtu), ゔ (vu), ヵ (xka), and ヶ (xke).

This is a software based project inspired by:

* [KanaCord](https://github.com/maccody/KanaChord) which was a hardware project
  building a physical 30 key chording kana keyboard with internal software.
  This was a split keyboard where the left hand had 2 rows of 6 keys containing
  maru (`ﾟ`, handakuten), ten-ten (`ﾞ`, dakuten), and a small key (labelled `大`),
  making 3 modifiers, and the main consonants (9 keys). On the right were 3 rows
  of 6 keys, containing the vowels (5 keys), `ん`, space, assorted punctuation,
  and a hiragana/katakana toggle. The core idea is the (almost) 50 main kana
  are typed by pressing the appropriate two keys together.

* The 12-key iOS Japanese flick keyboard for touch screens, which lays out 10
  keys for each row (`a`, `ka`, ..., `wa`) plus context dependent size toggle,
  maru, or ten-ten modifier, and a core punctuation key. Here each key can be
  tapped giving the labelled character from the `a`-column, flicked left
  (`i`-column), up (`u`-column), right (`e`-column), or down (`o`-column).

This project combines these ideas whereby any of the ASCII keys representing
a row (like `k` for `ka`, `ki`, `ku`, `ke`, `ko`) can be pressed alone or in
combination with one of four modifier keys (initially the four cursor keys)
giving the five different vowel combinations.

## Implementation

We are using the very capable macOS keyboard modifying software [Karabiner
Elements](https://karabiner-elements.pqrs.org/) to do this on macOS. KE has
its own rather verbose [JSON configuration
language](https://karabiner-elements.pqrs.org/docs/json/) which can be used
to define complex reboard remappings, including multiple keys at once which
we need for chording. Creating over 100 JSON rules for all the kana had to
be scripted, for which I am using Python.

The [KanaCord](https://github.com/maccody/KanaChord) uses operating system
specific keyboard expressions to enter the [hex code for individual unicode
for each kana](http://www.i18nguy.com/unicode/hiragana.html). For example,
け (ke) is unicode 3051 in hex.

For macOS, once in "*Unicode Hex Input*" mode, press-and-hold the option key
(aka alt), then type `3`, `0`, `5`, `1`, and release the option key. The top
number row or the number pad can be used. This will insert unicode hex character
3051, け (ke). The same trick works for emoji too, usually eight digits, and
can be done from KE. Unfortunately, using "Unicode Hex Input" mode has the
significant drawback that you won't get access to the OS' kanji support. In
this mode hiragana and katanana would both work by directly sending the
unicode hex for each character.

If instead we use "*Japanese - Romaji*" mode, we must map the desired kana to
any of the supported romaji aliases, and send that key sequence. Thus if
the user presses `right+k` wanting `け` we map this to sending `k` then `e`,
and let the OS turn this into the kana or kanji as more is typed. We can
also support `shift+right+k` sending upper case `K` then `E` which can be
configured in the macOS Japanese settings to be treated automatically as
the katakana `ケ`. In this mode to enter coffee we would want to simulate
pressing `K` `O` `-` `H` `I` `-` giving `コーヒー` as you typed. Here is
a great [introduction to typing in romaji
mode](https://www.tofugu.com/japanese/how-to-type-in-japanese/) which
covers this and more.

Alternatively, in "*Japanese - Kana*" mode, we must map the desired kana to
the physical key on the macOS Japanese keyboard, and send that keycode. In
KE these are labelled by the English letter or symbol on that key (these
keyboards have a full QWERTY layout with USA like punctuation placement).
Thus if the user presses `right+k` wanting `け` this corresponds to the
semi-colon key `:` so we send that. When `right+g` is pressed for `げ`,
we must also send the ten-ten key `@` (and likewise for maru modifications
follow the base kana with the maru key `[`). In this mode the shift key
gives the small form of the vowels `a`/`i`/`u`/`e`/`o`, `tsu` or
`ya`/`yu`/`yo`, and toggles the `わ` key to `を` (key zero). For katakana,
in this mode to enter coffee we would want to simulate pressing `b` `¥`
`v` `¥` giving `コーヒー` via the language support. There are explict keys
for `◌゙` (adding ten-ten or dakuten) and `◌゚ ` (adding maru or handakuten).

## Physical Keyboards

### Full querty

The initial mapping is based on the flick-input on iOS using the cursor keys.
Thus `k` alone gives ka (`か`), while `left+k` gives ki (`き`), `right+k` gives
ke (`け`), etc. This can be used with the QWERTY layout on a Japanese keyboard,
or anything similar with "Roman" letter like any English layout, or the French
AZERTY for example.

For example, `n+left` (→`に`), `h+down` (→`ほ`), `w+up` (→`ん`), `g+down` (→`ご`)
would type `にほんご` which should offer the kanji `日本語` (meaning Japanese
language). That is four chords (three and a single character if you prefer),
compared to at least seven keys in Romaji mode (either `nihongo` or `nihonngo`
works).

For an example with ten-ten and maru modifiers, the Japanese word for grammar
is `ぶんぽう` or `文法`. This can be entered as `b+up` (→`ぶ`), `w+up` (→`ん`),
`p+down` (→`ぽ`), `a+up` (→`う`), four chords for four characters.

For a katakana example, `コーヒー` (meaning coffee) in romaji mode using shift to
indicate katakana explicitly, would be `shift+h+down` (→`コ`), `-` (→`ー`),
`shift+h+left` (→`ヒ`), `-` (→`ー`). That is four chords (two and two single
keys if you prefer), compared to six keys with shift in Romaji mode (`KO-HI-`).

This may prove popular with Japanese learners, as no new key locations need be
learnt, only a couple of corner cases like `up+w`→`ん` to match the iOS flick
layout. However, with the right hand on the cursors to mimic the flick action,
the left hand must cover at least the 10 keys `a`, `k`, `s`, `t`, `n`, `m`,
`y`, `r`, and `w` (plus optionally the 5 ten-ten and maru modified forms using
`g`, `z`, `d`, `b` and `p`, and 2 small forms using `l` and `x`) which on
QWERTY layouts are split between the left and right halves of the keyboard
making it impractical. An alternative mapping taking only keys from the left
hand side would be easier physically, but harder to memorise.

### 12 key grid

Instead my initial plan is to use a custom keyboard mapping on a supplementary
small macro keyboard with at least 12 keys, mimicking the iOS flick-input with
its core four rows of three (additional controls either side not shown):

| あ | か | さ |
|----|----|----|
| た | な | は |
| ま | や | ら |
| 大 | わ | 、 |

How to handle the context dependent ten-ten, maru, or small form kana modifier
(shown here as `大`) remains to be decided (three modifier keys woud be
simplest), while for the punctuation button the English comma makes sense:

| `a` | `k` | `s` |
|-----|-----|-----|
| `t` | `n` | `h` |
| `m` | `y` | `r` |
| `?` | `w` | `,` |

The earlier example using core hiragana remains the same:  `n+left` (→`に`),
`h+down` (→`ほ`), `w+up` (→`ん`), `g+down` (→`ご`) would type `にほんご` which
should offer the kanji `日本語` (meaning Japanese language).

Words with ten-ten and maru modifiers like `ぶんぽう` (`文法`) would require
some kind of shift/modifier. As would small characters.

For a katakana example, `コーヒー` (meaning coffee) assuming we don't have
access to the hypen key `-`, we can use an iOS flick-input inspired chord 
`comma+down` (→`ー`). Thus four chords `shift+h+down` (→`コ`), `comma+down`
(→`ー`),　`shift+h+left` (→`ヒ`), `comma+down` (→`ー`) for four characters.
(Perhaps we should make both `comma+down` and `shift+comma+down` → `ー`
since this will often be used with romaji-shift mode?)

Additional keys would be needed for kanji selection, proably at least escape to
cancel, space to cycle the suggestions, and enter to accept. Perhaps for the
right hand?

### 15 key grid

A variation of this idea would be to use a custom layout on a macro keyboard of
at least 15 keys to replicate the Gboard [Godan
キーボード](https://support.google.com/ime/japanese/answer/2700298) flick-keyboard
which has separate keys for the five vowels (`a`, `i`, `u`, `e`, `o`) as the
left-most column, and the nine consonant rows (`k`, `s`, `t`, `n`, `m`,
`y`, `r`, and `w`) as the central and right-most columns. These are shown as
upper case Roman letters (with additional controls either side not shown):

| `A` | `K` | `H` |
|-----|-----|-----|
| `I` | `S` | `M` |
| `U` | `T` | `Y` |
| `E` | `N` | `R` |
| `O` | `小` | `W` |

Again the `?` here is a placeholder for a context dependent modifier.

My understanding is to type `日本語` would need seven keys, just like Romaji
mode: `N` `I` (→`に`) `H` `O` (→`ほ`) `N` (→`ん`) `G` `O` (→`ご`).

In this approach the flick actions left used for ten-ten (like `H` to `B`),
right for maru (`H` to `P`), down for the numbers (telephone keypad layout),
and up for corner cases. This is also used in ABC mode to access the rest
of the alphabet, meaning in principle this might replace a physical QWERTY
keyboard rather than just supplementing one - although you'd still need
cursor controls, escape, enter, etc. The middle key in the final row is
context dependant for toggling the modifiers (redundant?) or size:

| ・<br>・ `A` ・<br>`1` | `Q`<br>・ `K` `G`<br>`2` | `F`<br>`P` `H` `B`<br>`3`   |
|:---------------------:|:------------------------:|:---------------------------:|
| ・<br>・ `I` ・<br>`4` | `J`<br>・ `S` `Z`<br>`5` | `L`<br>・ `M` `ー`<br>`6`    |
| ・<br>・ `U` ・<br>`7` | `C`<br>・ `T` `D`<br>`8` | `X`<br>・ `Y` ・<br>`9`      |
| ・<br>・ `E` ・<br>・  | ・<br>・ `N` ・<br>`0`    | `？`<br>`.` `R` `！`<br>`、` |
| ・<br>・ `O` ・<br>・  | ◌゙` &nbsp; ◌゚ <br>大 ⇔ 小  | `V`<br>・ `W` ・<br>・       |

I don't see how this might be used with macOS "Japanese - Kana" mode, unless
when a consonant is pressed we wait for the vowel before sending anything to
the keyboard? However, it seems a natural fit to the "Japanese - Romaji" mode.

In this layout, for typing Japanese the only flick actions (here chording of some
sort) would be for the ten-ten and maru modifiers - leaving the second hand mostly
idle, perhaps mainly handling the kanji selection? Rather it seems logical to split
the layout as per the intended thumb split - one hand gets the five vowels, and
the other the nine consonants - taking us back to the KanaChord keyboard approach.

## License

MIT License
