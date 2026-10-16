# ཆོས་མངོན་རྒྱ་མཚོའི་སྙིང་པོ། — headings (§A) + fresh transclusion, 2026-10-16

**Written to 1-SOURCES** (not committed, not uploaded). Backup of the original:
`0-INBOX/migration-backups/2026-10-16/snying-po.before-A4-and-transclusion.md`.

## Headings — same method as ནོར་བུ / མངོན་པའི་རྒྱན།
- The original had 2042 headings, depth up to 23 `#`, and 430 empty sections (A.4).
- **Depth cap 16:** the 459 headings deeper than 17 `#` were dropped *before* anchoring (`deep.txt`).
- **Section openings:** 15 agents (`parts/P1…P15`) placed all 1583 remaining headings. Blocks were cut at the openers.
  Chapter headings sit on each chapter's own opening homage verse (chapters 2, 6 and 8 have one).
- **Dropped:** 18 headings with no text of their own:
  - the three groups of beings (one sentence);
  - the eight sub-continents (only listed);
  - the rasāsvāda/śuddhaka/anāsrava kinds;
  - the four immeasurables (only listed; treated under the next section).
- **Content-based collapse:** 8 agents. 118 of 260 leaf groups were collapsed (mostly verse-line glosses, cosmology measures and counts):
  304 child headings dropped, 102 paragraph merges.
- **A.5 ordinals:** 127 heading lines. The 2 checker hits left are false positives (the ordinal is inside the title: སྐྱེ་གནས་དང་པོ… / བསྐལ་པ་དང་པོ…).
- **Opening:** `## ཀླད་ཀྱི་དོན། ^I-0` (title line) and `## མཆོད་བརྗོད། ^II-0` (homage verses + verse of commitment). There is no preface.
- **Chapter body IDs:** chapters `^1-2-3-4-2-2-N-0` → `^1-N-k`. The frame keeps `^1-1…66`.
- **Bug found and fixed** (`apply_anchors.py`): at a cut right after a plain space, that space was reused as the ID separator, so one
  space of text was lost per such cut. Now a cut piece always keeps its trailing whitespace. The other two commentaries were unaffected:
  their cuts follow NBSP, and both passed the whitespace-exact text check.
- Result: 1263 headings, 2247 blocks (1642 originally). Text identical, whitespace-exact. Map: `idmap.v5.tsv`.

## Transclusion — fresh (`../transclusion-snying-po/`)
- 19 part agents → 1100 rows (1062 lemma / 7 gloss / 31 proof), plus 3 return-after-proof rows.
  Result: 1099 links in 946 groups.
- Parse: 2247 segments, 1263 TOC nodes, max depth 16, **1870 alignment pairs**, 1558 of 2247 blocks aligned.
  Root coverage is 613 of 614 (only the root title line I-1 is missing; the full title is covered by I-2). The longest scope is 11 blocks.
- `upload_text.py` dry run: all pairs resolve in the live root edition.

## Upload (not done)
Same two steps as before: `../A4-nor-bu/replace_edition.py "<file>" --execute` (deletes the live toc EqIlW8zYEvLMCT5SNM84k +
edition pbXnseLH7MmuHw3QmHAiJ, keeps the text UG86XzLP5mcDmcAAR1Qy1), then `upload_text.py "<file>" --execute` and verify.
