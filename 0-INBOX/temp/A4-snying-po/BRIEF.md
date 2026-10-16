# BRIEF — where does each outline section open? (ཆོས་མངོན་རྒྱ་མཚོའི་སྙིང་པོ།)

The text is a Tibetan commentary on the Abhidharmakośa, *ཆོས་མངོན་པའི་མཛོད་ཀྱི་རྣམ་པར་བཤད་པ་ཆོས་མངོན་རྒྱ་མཚོའི་སྙིང་པོ།*.
Its sa bcad (outline) has been turned into headings, but the headings were placed only at
paragraph boundaries. Many paragraphs hold several sections, so headings often ended up stacked together before a
paragraph that actually holds the text of several sections, and often the text of a section sits
under a later heading. Your job is to find, for **every heading in your part**, the exact place in
the text where that section's own text begins. A script will then move the headings there (cutting
paragraphs where needed). The text itself is never changed.

Note: outline nodes deeper than 17 levels are being removed and are not in your list; their text simply belongs to
the deepest listed ancestor. Place only the headings in your headings.tsv.

## Your files (only these — do not open other parts or the 1-SOURCES file)

- `headings.tsv` — the headings of your part in outline order: `id` (decimal path + `-0`), `depth`,
  `title` (editorial heading), `currently_before_block` (the block it currently sits above — often wrong).
- `text.md` — the body text, one block per entry: a line `[^ID]` (the block's ID) and then the block's text.
  It includes ~10 blocks before and ~30 blocks after your part as context. It is large: read all of it, in chunks.

## What counts as the start of a section

- Normally the clause where the commentator opens that section: ordinal + restated title + ནི / ལ
  (`གསུམ་པ་རྐྱེན་བཤད་པ་ལ། …`), a bare ordinal opener in the right enumeration (`དང་པོ་ནི།`, `གཉིས་པ་ལ།`),
  or the title phrase + ནི (`ཚིག་དོན་ནི།`).
- A **parent** section starts at its own opener/announcement (`X་ལ། A་དང༌། B་གཉིས། …`). Its first child
  starts at the child's opener *after* that announcement. If the parent has no separate opening and the
  first clause is already the first child's, give both the same anchor.
- Follow the enumerations: the parent's announcement tells you how many children there are and in what
  order. Nested lists reuse དང་པོ་ནི / གཉིས་པ་ནི, so make sure each opener belongs to the right level.
  Not every ordinal is an opener: lists of examples (`དང་པོ་ནི། བྱེད་རྒྱུ་ལྟ་བུ། གཉིས་པ་…`), quoted root
  verses and quoted scripture are not section openers.
- The heading title is editorial and may be worded differently from the text. Match on meaning and
  position, not just on the words.
- A section the commentator announces but never treats on its own (or treats inside a sibling) has no
  start of its own: give `NONE` and say where its matter is, if anywhere.

## Output — `anchors.tsv` in your folder (tab-separated, header line, one row per heading, same order)

`id	block	anchor	confidence	note`

- `id` — as in headings.tsv (skip id `0`, the work's title, if it is in your list).
- `block` — the ID of the block (from the `[^ID]` line) in which the section starts, e.g. `2-117`.
- `anchor` — 6 to 15 syllables copied **character for character** from text.md, starting exactly at the
  section's first syllable (the ordinal or first word). Whitespace does not need to match (NBSP vs space is
  fine), but every letter, tsheg and shad must. If the same phrase also occurs earlier in that block, make
  it longer so that it is unique there. `NONE` when there is no start.
- `confidence` — `high` / `medium` / `low`.
- `note` — short, English; required for medium/low/NONE.

Anchors must be in **non-decreasing text order** following the order of headings.tsv.

Write only `anchors.tsv`. Do not edit any other file. When done, reply with: number of rows, how many
high/medium/low/NONE, and the ids of every low or NONE row with a one-line reason.
