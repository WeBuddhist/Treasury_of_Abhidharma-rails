# Brief — root-text transclusion map for ཆོས་མངོན་རྒྱ་མཚོའི་སྙིང་པོ།, one part

You map where a Tibetan commentary quotes, glosses or cites its root text, for ONE part of the file (your part id
and line range are given in your task).

**About this commentary.** *ཆོས་མངོན་པའི་མཛོད་ཀྱི་རྣམ་པར་བཤད་པ་ཆོས་མངོན་རྒྱ་མཚོའི་སྙིང་པོ།* is a full verse-by-verse
commentary on Vasubandhu's Abhidharmakośa: it usually quotes a root verse (often as a block of its own, after an opener
such as `དང་པོ་ནི།`) and then explains it (`… ཞེས་པ་ནི།`, `… ཞེས་སོ།`, `… ཞེས་གསུངས་`, `… ཞེས་པ་ནས་ … ཞེས་པའི་བར་`, `ཅེས་
པའི་དོན་ནི`). Root coverage is expected to be nearly complete, and most quoted verses are in the ≥ 6-syllable seeds — but
check each seed and read for short lemmas and paraphrases too. It also quotes other works: the autocommentary
(`རང་འགྲེལ་ལས།`), sūtras (`མདོ་ལས།`), the Abhidharmasamuccaya (`ཀུན་བཏུས`), Indian commentators (`རྒྱལ་སྲས`, `གང་སྤེལ`,
`ཡ་ཤོ་མི་ཏྲ`), Mi bskyod rdo rje and others.

**Chapter keying.** Body blocks are `^1-N-k` inside commentary chapter N (`######## … ^1-2-3-4-2-2-N-0`), which explains
root chapter N (`## གནས་N་པ… ^N-0`, verses `^N-V`). The frame before chapter 1 (blocks `^1-1 … ^1-66`) explains the
treatise's title, the translator's homage and the Kośa's opening (root front matter `^I-1 … ^I-3` and ch.1 verses
1-1 … ~1-3): the root's Sanskrit/Tibetan title and translator's homage MAY be rows here (`^I-*`) where the commentary
quotes them. The zones `^I-1` and `^II-k` at the very top are the commentator's own title and homage: give them NO rows.
Root chapter colophons are `^N-a` (e.g. `^1-a`): give one to the block that carries the commentary's own chapter
closing (`… གནས་N་པ … ཞེས་བྱ་བ་སྟེ། …` or similar), as kind `lemma`. The root's closing verses and colophon
(`^a-1 … ^a-5`) may be quoted near the end of chapter 8.

Run every command from the vault root `D:\Work\OpenPecha\Treasury_of_Abhidharma-rails`. Use `python -I -X utf8`.

## Files (read-only)
- Commentary: `0-INBOX/temp/transclusion-snying-po/source.md` (exact copy of the 1-SOURCES file). Blocks are separated
  by blank lines; each content block ends with its own `^id`; headings start with `#` (bold `**…**` deeper than 6).
- Root text: `1-SOURCES/Text/ཆོས་མངོན་པ་མཛོད།.md` (8 `##` chapters; verse ids `^N-V`, front `^I-1…3`, chapter colophons
  `^N-a`, back `^a-1…5`). Look a block up with e.g. `grep -n "\^3-45\s*$" <root>`.
- Seeds: `0-INBOX/temp/transclusion-snying-po/seeds/seeds-<PART>.tsv` — every place where a commentary block shares ≥ 6
  consecutive syllables with a root block (`line` = first line of the commentary block). Evidence, not answers.
- This is a fresh run: do not use any earlier transclusion files .

Never edit any file except your output file. Keep ALL your own working files in
`0-INBOX/temp/transclusion-snying-po/work/<PART>/` — other agents run in parallel. Read your range in pieces
(≈150 lines at a time), not all at once.

## What to produce
`0-INBOX/temp/transclusion-snying-po/place-<PART>.tsv`, UTF-8, tab-separated, this header exactly:

```
heading	root_block	line	kind	words
```

One row per (commentary block, root block) that the block quotes, glosses or cites:
- `heading` — the block id of the nearest heading above the block (e.g. `1-2-3-4-2-2-3-1-1-0`), for reference.
- `root_block` — the root block id without `^` (e.g. `3-45`).
- `line` — the FIRST line number (1-based, in source.md) of the commentary block. Never a heading line, never a blank
  line, never the 2nd+ line of a multi-line block. The transclusion is inserted directly before this block.
- `kind` — `lemma` (quotes the root's words to explain them), `gloss` (explains a specific root verse in its own words,
  e.g. a `ངག་དོན་ནི།` paraphrase) or `proof` (cites the root as authority for another point).
- `words` — the root words as the commentary gives them (≤ 25 syllables; `…` to elide).

## Rules
1. **Only the root text counts.** A quotation from another work is not a root citation — unless the shared words are
   the root's own verse being explained there. The autocommentary (`རང་འགྲེལ་ལས།`) often repeats verse words; a block
   that only quotes the autocommentary gets no row.
2. **Seeds: decide each one.** Keep a seed when the block really quotes/explains/cites THAT root block. When the same
   words match several root blocks, choose the one the commentary is discussing — normally in the SAME root chapter as
   the commentary chapter you are in, and the verse currently being explained or its neighbour. Drop stock phrases and
   matches inside quotations of other works.
3. **Look for what the matcher missed.** Read every content block in your range. Short lemmas (`… ཞེས་སོགས་`), range
   statements and paraphrases are not in the seeds. Find their root block by searching the root for the quoted
   syllables; add a row only when you are confident.
4. **Range statements** (`A ཞེས་པ་ནས་ B ཞེས་པའི་བར་གྱིས་བསྟན།`, `… ཞེས་སོགས་རྐང་པ་བཅུ་གཉིས`): list every root block in the
   range when it is ≤ ~12 blocks and the block opens that stretch; for a longer range give only the first and last.
5. A block can carry several root blocks (several rows, same `line`); a root block can appear at several lines. Do not
   add a row just because a block lies inside a section about some verse — only blocks that quote, gloss or cite it.
   Placement scope: everything after a transclusion group up to the next group or heading is aligned to it, so put the
   row on the block where the discussion of that verse starts, and again on a later block only when the commentary
   returns to that verse after discussing another one.
6. **Validate before you finish** and fix every problem it reports:
   `python -I -X utf8 0-INBOX/temp/transclusion-snying-po/validate_place.py 0-INBOX/temp/transclusion-snying-po/place-<PART>.tsv <PART>`

## Reply (≤ 15 lines)
The output path; rows by kind; seeds kept / dropped (main reasons); rows added beyond the seeds; root chapters and
verse range covered; anything you were unsure of (line + root block); the validator's last line.
