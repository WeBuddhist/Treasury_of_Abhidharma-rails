# ནོར་བུའི་བང་མཛོད། — fresh transclusion (Method B), 2026-10-16

**Written to 1-SOURCES** (not committed, not uploaded). Backup: `0-INBOX/migration-backups/2026-10-16/nor-bu.before-transclusion.md`.

- Fresh run, with none of the Oct-14 run's maps. Seeds = verbatim matches of ≥ 6 syllables (`root_quotes.py` → `seeds/`): 396 blocks, 490 matches.
- 7 isolated part agents (`BRIEF.md`; P1 opening + frame + ch.1, P2 ch.2, P3 ch.3, P4 ch.4, P5 ch.5, P6 ch.6–7, P7 ch.8 + conclusion),
  run in batches gated on the 5-hour limit (paused at 96%, resumed after the reset).
  Every `place-P*.tsv` validates with 0 problems. Rows per part: 79 / 119 / 139 / 81 / 59 / 110 / 46.
- 633 rows (409 lemma / 140 gloss / 84 proof) → 633 transclusion lines in 409 groups, no repeated groups. Text otherwise unchanged (checked by `insert_transclusions.py`).
- Root coverage: 468 of 614 root blocks. Gaps are verses this dka' gnas commentary does not treat (lists in the agents' reports, e.g. 3-29…35, 4-79…94, 5-54…58).
  Chapter colophons 1-a…7-a are placed. 8-a has no row (the commentary has no chapter-8 closing), and the root back matter a-1…5 is not quoted.
- Parse: 1014 segments, 434 TOC nodes, max depth 16, **1200 alignment pairs**, 749 of 1014 blocks aligned.
  Longest scope: 22 blocks at ^2-3-131 → 3-89/3-90, the calendar digression (months, ཞག་མི་ཐུབ, year), which matches those verses.
- `upload_text.py` dry run: all 1200 pairs resolve in the LIVE root edition hKRCkws7bBmMH1TA3nZ6h.
- 8 deliberate "returns to a verse" (e.g. 4-112 at l.2418, 7-28 at l.3181, 2-23 at l.795) are kept.

## Upload (on hold — user)
The frontmatter still holds the OLD edition_id / toc_id, so upload in two steps:
1. `python -X utf8 0-INBOX/temp/A4-nor-bu/replace_edition.py "<file>" [--execute]` — deletes the old TOC + edition, keeps the text.
2. `python -X utf8 4-SYSTEM/scripts/upload_text.py "<file>" [--execute]` — new edition (1014) + TOC (434) + alignment (1200 pairs).
Then `--verify` and read the alignment back.
