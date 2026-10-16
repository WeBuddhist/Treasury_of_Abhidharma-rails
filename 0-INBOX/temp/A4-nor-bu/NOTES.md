# ནོར་བུའི་བང་མཛོད། — §A.4 fix (empty sections), 2026-10-16

## v6 (current file) — chapter body IDs (user)
- The commentator's outline is kept: the 8 chapters stay at `^2-2-2-2-2-2-N-0` (8 `#`).
- Body blocks inside chapter N are numbered `^2-N-k` (e.g. ch.1 `^2-1-1 … ^2-1-80`, ch.8 `^2-8-1 … ^2-8-36`).
  The frame under `## ^2-0` before chapter 1 keeps `^2-1 … ^2-68`. The conclusion (`^2-3-0`) continues that counter as `^2-69 … ^2-95`,
  because `^2-3-k` would collide with chapter 3.
  This departs from annotation-conventions §3, where the body counter is keyed to the `##` label only. Record it in the annex (human-only).
- Script `chapter_ids.py nor-bu.v5.md nor-bu.v6.md idmap.v5.tsv idmap.v6.tsv`. Original → final ID map: **`idmap.v6.tsv`**.
- Text whitespace-exact, no duplicate IDs, content IDs ≤ 3 parts. Lint OK; parse 1014 segments, 434 TOC nodes, max depth 16.

## v5 — opening (user): no ^0-x under the title
- `## ཀླད་ཀྱི་དོན། ^I-0` → title line `^I-1` · `## མཆོད་བརྗོད། ^II-0` → homage `^II-1` · `## …ཡན་ལག་ལྔ། ^1-0` now opens
  at `འདིར་…`, so the preamble and `དེ་དག་གི་ནང་ནས…` are one block `^1-1` (they are one sentence: `…བྱུང་ཞིང༌། དེ་དག་གི་ནང་ནས…`).
  Script `opening.py nor-bu.v4.md nor-bu.v5.md`.
- Merges now add no space: the text is identical to the original whitespace-exact, NBSP included (checked against the backup).
- 434 headings, 1014 blocks; parse: 2 front_matter / 874 paragraph / 138 verse, 434 TOC nodes, max depth 16.
  Old → final ID map: `idmap.v5.tsv`.

## v4 — user rules added after review of v2
- **Content-based headings:** a group of sub-sections whose children are only simple definitions / pointers / list
  items gets no child headings, and the parent keeps the text as one block. A group where any child explains,
  argues or discusses keeps its headings. 58 leaf-sibling groups were judged by 6 isolated agents
  (`collapse/BRIEF.md`, `collapse/C*/decisions.tsv`): 9 COLLAPSE (31 child headings dropped), 49 KEEP.
  In a collapsed section, consecutive paragraph blocks are merged into one block (9 merges, written as a single
  line; a multi-line block would be parsed as verse). Verse blocks stay separate.
- **Max depth 16** (parser TOC depth, so the deepest heading is 17 `#`). 19 deeper headings are dropped and their text
  falls to the depth-16 ancestor.
- Result: 432 headings, 1014 blocks (762 originally). Text identical, NBSP included. Lint OK; parse 1014 segments
  (876 paragraph / 138 verse), 432 TOC nodes, max depth 16. Old → final ID map: `idmap.v4.tsv`.
- Pipeline: `prep_final.py` → `rebuild.py nor-bu.v3.md report.v3.md` → `merge_collapsed.py nor-bu.v3.md nor-bu.v4.md idmap.v4.tsv <backup>`.
- Open: `…-2-1-1-2-1-0` (22 faculties) shares its parent's opener `^2-165`, whose wording matches child 2
  (`…འཇོག་པའི་རྒྱུ་མཚན`). The text does not mark the children (P3 low confidence) — scholar check.
- v2 (before these rules) is kept as `nor-bu.v2.md`. The sections below describe v2; the outline fix and the NONE drops still apply.

**Result:** written to `1-SOURCES/Commentaries/…ནོར་བུའི་བང་མཛོད།.md`.
Backup: `0-INBOX/migration-backups/2026-10-16/nor-bu.before-A4-reanchor.md`.

- Empty sections 113 → 0. `check_a.py`: A.1–A.5 clean. Two sibling-numbering gaps are left by dropped headings (see below), the same kind of gap that was accepted in Introduction_to_the_Middle_Way.
- Text unchanged, character for character including NBSP. Only headings, block cuts, block IDs and line breaks differ.
- Blocks 762 → 1060 (297 cuts at section openers + 1 split word rejoined). Body IDs renumbered: 1057 of 1060 changed.
  Old → new map: `report.v2.md` (section "old -> new block IDs").
- Lint OK; parse: 1060 segments (922 paragraph / 138 verse), 481 TOC nodes, depth 21, 0 alignment.

## Method
1. 9 isolated agents (BRIEF.md, `parts/P1…P9`) each returned the verbatim opening phrase of every heading in their part (`anchors.tsv`).
   Totals: 489 rows — 10 NONE, 3 low, 44 medium, the rest high.
2. `prep_final.py`: outline fix (below) + merges the anchors into `parts-final/P0/anchors.tsv`.
3. `apply_anchors.py pre.md parts-final nor-bu.v2.md report.v2.md --drop …`: each heading is moved to its anchor and the block is cut there.
   All anchors were found, in order. 4 cuts fall where the source has no shad between clauses (`…གཅིགགསུམ་པ…`, `…མིནགཉིས་པ…`, `…གོདང་པོ་ནི…`, and one `དང་པོ་ལ་` inside a clause).
4. Split ordinal `ག|སུམ་པ་ནི།` (end of old ^2-18 / start of ^2-19) rejoined: the ག now opens the block after heading ^2-1-2-1-1-1-3-0.

## Changes to the outline — please review
- **Moved (P5):** the sun/moon (vimāna) and Meru subtrees were nested under the 33 gods (`…-3-2-1-3-1-2-2-1-2-*`).
  The text's own announcement (`དང་པོ་ལ། རྒྱལ་ཆེན་བཞིའི་གནས། སུམ་ཅུ་རྩ་གསུམ་པའི་གནས།…`), and the heading
  `གཉིས་པ་རི་རབ་ལ་བརྟེན་པའི་རྒྱལ་ཆེན་རིགས་བཞི`, place both under the Four Great Kings.
  - 18 heading IDs were renamed `…-1-2-x` → `…-1-1-x` (same depth).
  - `གཉིས་པ་སུམ་ཅུ་རྩ་གསུམ་པའི་གནས། …-1-2-0` now sits at its own opener (old ^2-356).
- **Removed — no text of their own** (rule: a heading that fits no text is removed):
  - the six causes `…-2-3-1-2-1` … `-6` under གཞུང་དོན (the commentary treats them inside the preceding སྤྱི་དོན item 4);
  - `…-3-2-1-3-1-2-1-0` མིའི་གནས་བཤད་ཟིན (announced as "already explained") → gap: only child `2` under `…-3-2-1-3-1-2`;
  - `…-4-2-1-2-3-2-3-1-1-1-2-0` ཟག་མེད་ཀྱི་སྡོམ་པ (treated together with the dhyāna vow) → gap [1, 3];
  - `2-3-2-0` གཞུང་དོན at the end (announced, never treated).
- The nodes stay in `2-RAILS/Sections/Raw/toc-tree/nor-bu-bang-mdzod.md`, which still has the old nesting.

## For a human — notes from the agents (not changed)
- `…-6-3-2-3-0` is titled **ཕྱིར་མི་འོང** but sits where the once-returner (ཕྱིར་འོང) is treated; the non-returner passage falls inside `…-6-3-2-4`. The title probably should be ཕྱིར་འོང.
- Low-confidence placements: `…-2-1-1-1-5-0` (no ལྔ་པ opener), `…-2-1-1-2-1-0`, `2-3-1-3-1-3-0`. Medium rows: listed in `report.v2.md`.
- Source damage noted: stray `གང་དག` at the start of old ^2-41; a running-header fragment fused into an opener at old ^2-226 (`…སྟོན་པའི་གགཉིས་པ་ནི།`); `གཉིས་པས་ལམ་འབྲེལ` (old ^2-365); typos `ཉིས་པ` and `དགོས་པ`/`དྭོགས་པ` (P1).
- Text ordinals that differ from the heading's (the heading follows the outline): old ^2-180 `གསུམ་པ` for 2nd, ^2-334 `བཞི་པ` for 3rd, the བཞི་པ in P1, and the merged 1st/2nd in P6.

## Consequences
- **Live upload is now stale.** The edition AgMgQ3L63IDYAgy1bLiay has 762 segments, and the file now has 1060. The edition and the TOC (vv3VoNW15HhLeSbvexwHw) need replacing. Not done.
- `0-INBOX/temp/transclusion-nor-bu-bang-mdzod/` (mapping.tsv, map-*.tsv) uses the old block IDs. Convert it with the old → new map before using it.
- Annex migration log (`4-SYSTEM/Guidelines/vault-annex.md`) is a human-only file and still the unfilled template, so this note is the record for now.
