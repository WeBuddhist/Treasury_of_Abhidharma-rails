"""Replace a commentary's live edition + TOC, keeping its text (text_id, commentary_of).
Deletes the TOC, then the edition; moves edition_id / toc_id to the ledger's 'deleted' history and
out of the frontmatter, so that upload_text.py then posts only the new edition + TOC.
usage (from the vault root): replace_edition.py FILE [--execute]
"""
import sys, datetime as dt
from pathlib import Path
sys.path.insert(0, "4-SYSTEM/scripts")
from upload_text import call, load_ledger, save_ledger, read_fm, BASE
from delete_upload import delete, unpatch_fm

path = Path(sys.argv[1]); execute = "--execute" in sys.argv
fm = read_fm(path)
tid, eid, toc = fm.get("text_id"), fm.get("edition_id"), fm.get("toc_id")
assert tid and eid and toc, (tid, eid, toc)
eds = call("GET", f"/v2/texts/{tid}/editions")
eds = [e.get("id") for e in (eds.get("items", []) if isinstance(eds, dict) else eds)]
print(f"host {BASE}\ntext {tid} (kept)\nlive editions on the text: {eds}\nwill DELETE toc {toc}, then edition {eid}")
if eds != [eid]:
    sys.exit("live editions differ from the frontmatter — stop")
if not execute:
    print("Dry run — nothing deleted."); sys.exit(0)
print("  toc:", "deleted" if delete(f"/v2/table-of-contents/{toc}") else "already gone")
print("  edition:", "deleted" if delete(f"/v2/editions/{eid}") else "already gone")
ledger = load_ledger()
entry = ledger[path.stem]
entry.setdefault("deleted", []).append({"edition_id": eid, "toc_id": toc, "text_kept": tid,
                                        "reason": "A.4 re-anchor / re-segmentation 2026-10-16",
                                        "deleted_at": dt.datetime.now().isoformat(timespec="seconds")})
entry.pop("edition_id", None); entry.pop("toc_id", None)
save_ledger(ledger)
unpatch_fm(path, ("edition_id", "toc_id"))
print("  edition_id / toc_id moved to the ledger's 'deleted' history and removed from the frontmatter")
