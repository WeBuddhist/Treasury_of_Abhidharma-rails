# མངོན་པའི་རྒྱན། — headings (§A) + fresh transclusion, 2026-10-16

**Written to 1-SOURCES** (not committed, not uploaded). Backup of the original:
`0-INBOX/migration-backups/2026-10-16/mngon-rgyan.before-A4-and-transclusion.md`.

## Headings — same method as ནོར་བུ
1. **Section openings:** 17 isolated agents (`BRIEF.md`, `parts/P1…P17/anchors.tsv`). Headings moved to their openers, with blocks cut there
   (`../A4-nor-bu/apply_anchors.py`).
2. **Dropped:** 11 headings with no text of their own (`drop.txt`):
   - 1-2-1-0, and 1-2-3-3-0 with its 2 children;
   - the 5 misplaced duplicates …-1-1-5-1…5. These were the parent-after-child A.3 errors, and their titles only repeat 1-1-1…1-1-5.
   - …-3-4-3-0 (12 minds: covered by its parent's opening and closing; this also fixes the 1/3/2 sibling order);
   - …-5-2-1-4-2-0.
   Gaps left: under 1-2 [2,3] and under 1-2-3 [1,2,4].
3. **Content-based collapse** (`collapse/`, 6 agents): 7 of 60 leaf groups are definition, list or count only, so 21 child headings were dropped
   and 34 paragraphs merged. Max depth is 15 `#`, so the depth cap removes nothing.
4. **A.5 ordinals**, majority rule (`fix_ordinals.py`): 27 heading lines. The remaining checker hit (`གནས་བརྒྱད་ལས་དང་པོ`) is a false positive.
5. **Opening** (user: three zones): `## ཀླད་ཀྱི་དོན། ^I-0` (title lines), `## མཆོད་བརྗོད། ^II-0` (homage + 3 verses of commitment),
   `## སྔོན་བྱུང་། ^III-0` (preface: Vasubandhu, the prophecy, why the Kośa was written, and the "three parts" sentence).
6. **Chapter body IDs:** chapters `^2-2-3-2-N-0` → blocks `^2-N-k`. The frame keeps `^2-1…39`; `^1-k` and the conclusion `^3-k` are unchanged.
   Script `opening_chapters.py`.
7. **Bug found and fixed:** the first build left 25 blocks containing only a zero-width space (`apply_anchors.py` did not treat
   ZWSP as a lead mark). Fixed, rebuilt (v2b…v5b), 0 such blocks. ནོར་བུ was not affected (0).
- Result: 487 headings, 2258 blocks (1996 originally). Text identical, NBSP and ZWSP included. Map: `idmap.v5b.tsv`.

## Transclusion — fresh (`../transclusion-mngon-rgyan/`)
- 13 part agents → 921 rows. These were remapped onto the rebuilt file by text position; none fell on removed blocks.
  Review added 26 "return" rows: the discussed verse again on the block after a mid-discussion proof.
- 947 rows → 943 transclusion lines in 794 groups. Parse: 2258 segments, 487 TOC nodes, max depth 14, **2292 alignment pairs**,
  1968 of 2258 blocks aligned. Root coverage 609 of 614; missing only the root front matter I-1…3 and the closing verses a-4/a-5.
- Longest scopes: 30 blocks on 1-1 (the homage), 26 on 3-60, 22 on 4-39.
- `upload_text.py` dry run: all pairs resolve in the live root edition.

## Upload (not done)
Same two steps as ནོར་བུ: `../A4-nor-bu/replace_edition.py "<file>" --execute` (deletes the live toc FSS6pNBJx39d2mjhT4RPh +
edition T9yxNPJKUgOUN4AaDEdEQ, keeps the text jLp2lPWwnIKPuTX2Ar6Ax), then `upload_text.py "<file>" --execute` and verify.
