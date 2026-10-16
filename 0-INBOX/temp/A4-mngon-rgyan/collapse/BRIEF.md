# BRIEF — do these sub-sections need their own headings? (མངོན་པའི་རྒྱན།)

A Tibetan Abhidharmakośa commentary has its sa bcad (outline) as headings. Every outline node got a
heading, even where the "sub-sections" are only a word or a line each. Those tiny headings chop one
sentence into pieces, which is useless. Example: under `འཁོར་བར་འཇུག་པ`, the text says
`… གསུམ་ལས། དང་པོ་ནི། དབང་པོ་ལ་བརྟེན་ནས་འཇུག་པས། གནས་གཉིས་པས་བསྟན། གཉིས་པ་ནི། … གནས་གསུམ་པས་བསྟན། གསུམ་པ་ནི། … གནས་བཞི་པས་བསྟན། …`
— each child is a one-line definition or pointer, so its heading should go and the parent keeps the text as one block.

**The decision is about content, not length.**
- **COLLAPSE** — the children are simple definitions, identifications, list items, glosses or pointers
  ("X is Y", "this is taught in chapter N", a one-line gloss of a verse line), with no discussion of their own.
- **KEEP** — the children explain, argue, analyse, raise and answer doubts, cite proofs, or otherwise
  talk about their topic, so a reader benefits from navigating to each one.
- If the children are mixed (some only define, others explain), judge the group as a whole: KEEP when
  at least one child is a real explanation that deserves its own heading; otherwise COLLAPSE.

## Your file (only this one — do not open other folders or any 1-SOURCES file)

`groups.md` — one entry per group: a line `=== GROUP <parent id> — <parent title> (n children)`, then the
parent heading, the children's headings and the text exactly as it sits in the file (block IDs at line ends).

## Output — `decisions.tsv` in your folder (tab-separated, header line, one row per group, same order)

`parent_id	decision	reason`

- `parent_id` — the id after `GROUP` (e.g. `2-2-2-2-2-2-1-2-1-1-1-2-0`).
- `decision` — `COLLAPSE` or `KEEP`.
- `reason` — one short English sentence describing what the children do.

Write only `decisions.tsv`. When done, reply with the counts and the ids of any group you found hard to decide.
