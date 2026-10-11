# Phase C — sliced tree build (orchestrator addendum to pass3-tree.md)

The merged candidates/enumerations are too large for one context, so the tree is built in 7 sequential slices
(K = 1..7). You build slice K only. Follow `4-SYSTEM/Skills/toc-generate/prompts/pass3-tree.md` for ALL
hierarchy, matching, cleaning and false-positive rules. The deviations below override it where they conflict.

Working dir: C:\Users\LENOVO\Obsidian\Treasury_of_Abhidharma-rails
Directory D = `0-INBOX/temp/TOC-nyi-ma`

## Inputs
- `D/slices/cand-K.md`  — candidates for this slice's chunks (chunks overlap by 25 lines; the same candidate may appear
  twice — emit it once).
- `D/slices/enum-K.md`  — enumerations for the same chunks.
- `D/source.md`         — the commentary; 1-based line numbers (the chunk headers `<!-- chunk NNN | lines A–B -->` give
  each candidate's line window).
- For K > 1: `D/slices/state-(K-1).md` — the open ancestor path and counters at the end of the previous slice.

## Outputs (write both)
1. `D/slices/tree-K.md` — the tree nodes for this slice ONLY, in the final format, NO header and NO frontmatter:
   `<indent>* <decimal> <title> [[N]]`
   - decimal numbering is ABSOLUTE and continues from the previous slice's state (slice 1 starts at `1.`).
     Slice 1: the top node (depth 1) is the work's overall division; use the real structure of the text.
   - indent = 3 spaces × (depth − 1); one entry per line.
   - **Pointer `[[N]]`** (deviation from pass3-tree.md, required by the QC/ingest scripts): N is the 1-based line number
     in `D/source.md` of the sentence that ANNOUNCES/opens that node (the clause carrying its ordinal/title). Locate it by
     grepping the title text or the candidate's CONTEXT in `D/source.md` within the chunk's line window. Pointers must
     be non-decreasing in document order (a parent and its first child may share a line). If after a real attempt a
     node's line cannot be found, write `[[?]]` — but try hard; do not guess a number.
   - Node titles: title only, ordinal kept, no trailing shad, per pass3-tree.md.
2. `D/slices/state-K.md` — the ancestor path open at the END of this slice, as lines
   `<decimal> | <title> | declared_children=<n or ?> | children_so_far=<m>`, root-to-deepest, followed by the line
   `LAST_POINTER=<N>`. Next slice's agent resumes from this.

## Rules specific to slices
- Do not repeat nodes already emitted in earlier slices; continue siblings under the open ancestors in state-(K-1).md.
- If the first candidates of this slice are continuations (e.g. `གཉིས་པ་` under an open parent), attach them to the right
  open ancestor using the declared counts.
- Cover the whole slice's line range; do not drop branches. Drop false-positive candidates per pass3-tree.md rule A.
- Output Tibetan titles only; no commentary in the tree file. Reply with the two paths and the node count only.
