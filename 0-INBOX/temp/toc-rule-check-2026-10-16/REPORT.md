# TOC rule check — Treasury of Abhidharma (2026-10-16)

Rules: `D:\Work\OpenPecha\priority_repo.md` §A (A.1–A.5), which override this vault's 4-SYSTEM docs where they differ.
Scope: root text + 4 commentaries. **Bhāṣya (ཆོས་མངོན་པའི་མཛོད་ཀྱི་བཤད་པ།) excluded** as asked.
Read-only — nothing in `1-SOURCES/` was changed.

Tools: `check_a.py` (this folder; A.1–A.5 incl. bold rule and the majority rule for sibling ordinals) and
`Vinaya_sutra-rails/0-INBOX/temp/rails-tools/toc_attest.py` (title attestation, informational).
Full per-file lists: `check-N.txt`, `attest-N.md`.

| # | File | Headings | Max depth | A.1 `#`=depth | A.2 bold | A.3 IDs / order | A.4 empty sections | A.5 ordinals |
|---|------|---------:|---------:|:---:|:---:|:---:|---:|---:|
| 1 | ཆོས་མངོན་པ་མཛོད། (root) | 14 | 3 | ✓ | ✓ | ✓ | 0 | ✓ |
| 2 | ནོར་བུའི་བང་མཛོད། | 490 | 22 | ✓ | ✓ | ✓ | **113** | ✓ |
| 3 | མཚན་ཉིད་ཀྱི་རྗེས་སུ་འབྲང་བ། | 10 | 2 | ✓ | ✓ | ✓ | 0 | 1 group |
| 4 | མངོན་པའི་རྒྱན། | 516 | 15 | ✓ | ✓ | **2 parent-after-child, 1 order swap** | **59** | 28 groups / 29 headings |
| 5 | ཆོས་མངོན་རྒྱ་མཚོའི་སྙིང་པོ། | 2042 | 23 | ✓ | ✓ | ✓ | **430** | 216 groups / ~228 headings |

## 1. Root text — clean
All 14 headings pass A.1–A.5. Attestation "misses" for the chapter titles are expected: they are editorial titles
(the text names its chapters in the colophons, not as a phrase identical to the heading).

## 2. ནོར་བུའི་བང་མཛོད། — 113 empty sections (A.4)
Headings are stacked with no text between them, and the text that belongs to them sits under a later sibling. Example (L35–49):

```
##### དང་པོ་དབང་པོ་ལ་བརྟེན་ནས་འཇུག་པ། ^1-2-1-1-0      ← empty
##### གཉིས་པ་གང་གིས་གང་དུ་འཇུག་པ། ^1-2-1-2-0
བསྡུས་དོན་ནི། …                                       ← one block covering the whole བསྡུས་དོན
##### གསུམ་པ་གང་གི་དབང་གིས་འཇུག་པ། ^1-2-1-3-0      ← empty
#### འཁོར་བ་ལས་ལྡོག་པ། ^1-2-2-0                       ← empty
### ཚིག་དོན། ^1-3-0                                     ← empty
### མཚམས་སྦྱོར། ^1-4-0                                  ← empty
### བརྒལ་ལན། ^1-5-0
གསུམ་པ་ནི་ཟག་པ་དང་བཅས་པའི་…                           ← this is the text of ^1-2-1-3-0, not of ^1-5-0
```
Cause: the body blocks are coarser than the sa bcad, so several sections' text sits in one block and the headings
could not be placed inside it. Attestation agrees: 126 titles are found only in the parent's announcement.

## 3. མཚན་ཉིད་ཀྱི་རྗེས་སུ་འབྲང་བ། — 1 A.5 item (needs a scholar)
`## གང་ཟག་གཏན་ལ་འབེབས་པ། ^9-0` is the only chapter without `གནས་N་པ` (8 of 9 have it → majority rule says add
`གནས་དགུ་པ`). The text itself never calls it the 9th གནས — it is the pudgala-viniścaya appendix. Adding the
ordinal is an editorial choice; I'd leave it unless a scholar wants it.

## 4. མངོན་པའི་རྒྱན།
- **A.3 order (2):** `^2-2-3-2-2-2-1-2-2-1-1-5-1-0` (L1161) and `-5-2-0` (L1167) come **before** their parent
  `^…-1-1-5-0` (L1208) and are nested under the wrong sections (`-1-1-1-0` / `-1-1-2-0`). Siblings `-5-3/4/5` are correctly placed after L1208.
- **Sibling order:** under `2-2-3-2-2-2-2-3-4` the headings appear as 1, 3, 2 (L1696, L1712 `-3-0`, L1722 `-2-0`).
- **A.4:** 59 empty sections (same stacking pattern as ནོར་བུ).
- **A.5:** 28 mixed groups → 26 ADD (12 of them ties, file habit = add: 89 uniform-with vs 36 uniform-without), 2 STRIP
  (L1615 `གསུམ་པ་རྒྱུ་དེ་དག་གི་དོན་བསྡུ་བ།`, L5795 `དང་པོ་ཡུལ་སེམས་ཚད་མེད་པ།`).

## 5. ཆོས་མངོན་རྒྱ་མཚོའི་སྙིང་པོ།
- **A.4:** 430 empty sections — same pattern, e.g. L300–310: `གསུམ་པ་རོ་` / `བཞི་པ་དྲི་` stacked empty above `ལྔ་པ་རེག་བྱ་`,
  whose block starts with `གསུམ་པ་རོ་བཤད་པ་ནི།…` (it holds the text of 3, 4 and 5).
- **A.5:** 216 mixed groups → 195 ADD (130 ties, file habit = add: 449 vs 77), 21 STRIP.
  One heading lacks its ordinal in a way that looks like a typo: L7427 `བཞི་པའི་ཆོས་བཞི། ^…-3-2-2-0`, whose siblings are
  `དང་པོ་…`, `གསུམ་པ་…`, `བཞི་པ་…` → should be `གཉིས་པ་བཞི་པའི་ཆོས་བཞི།`.
- A.1–A.3 clean.

## What fixing would involve
- **A.5** — heading-line edits only (IDs and body unchanged): the majority-rule fix, as done in the other repos.
- **A.3 in མངོན་པའི་རྒྱན།** — move 2 heading lines + fix the 1/3/2 order (renumber or move).
- **A.4 (602 headings in 3 files)** — the user rule is "heading that fits some text → move it there; otherwise remove".
  Here the fitting text is mostly *inside* a block that also holds the previous section, so moving the heading
  means **splitting paragraphs**, which changes body block IDs. All three files are already uploaded
  (editions AgMgQ3…, T9yxNP…, pbXnse…), so this means a re-segmentation + re-upload of edition and TOC, not just
  a TOC replace. Needs a decision before starting.
