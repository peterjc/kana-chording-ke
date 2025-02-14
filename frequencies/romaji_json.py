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
"""Simple Qwerty letter counts using romaji mapping to JSON.

JSON format is for use with https://lucmazon.github.io/heatmap/ or locally
in the browser via https://github.com/lucmazon/heatmap/ (tested with Firefox).

This draws a keyboard layout using the counts for each English letter, which
can then be displayed on a Keyboard layout (e.g. Querty, or the heatmap author's
choice of the Bépo layout).
"""

katakana_counts: dict[str, int] = {}
with open("Tamaoka-and-Makioka-2004-Asahi-kana-usage.tsv") as handle:
    for line in handle:
        if line.startswith(("Katakana\t", "Total\n")):
            continue
        kanas, value = line.strip().split("\t")
        for k in kanas:
            # Splitting composites like シャ into two entries
            katakana_counts[k] = int(value)

assert katakana_counts["ッ"]

qwerty_counts = {}
with open("romaji.tsv") as handle:
    for line in handle:
        if line.startswith(("Katakana\t", "Total\n")):
            continue
        k, h, romaji = line.strip().split("\t")
        if k in katakana_counts:
            for letter in romaji:
                qwerty_counts[letter] = (
                    qwerty_counts.get(letter, 0) + katakana_counts[k]
                )

with open("romaji.json", "w") as handle:
    handle.write('{\n  "count": {\n')
    handle.write(
        ",\n".join(
            f'    "{letter}": {count}' for letter, count in qwerty_counts.items()
        )
    )
    handle.write("\n")
    handle.write("  },\n")
    handle.write('  "modifiers": [\n')
    handle.write('    "left shift", "left ctrl", "❖", "alt",\n')
    handle.write('    "altGr", "right ctrl", "right shift"\n')
    handle.write("  ]\n")
    handle.write("}\n")
