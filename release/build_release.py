"""Assemble the folder that gets uploaded to the Hugging Face Hub.

Reads from this repository, writes a self-contained folder, and prints what it wrote.
Nothing is uploaded. Run upload.sh for that.

    python3 release/build_release.py --repo-id USER/openai-hf-incident-recovered-tables \
        --author "Your Name"

What it does:

  * copies the three CSV files out of data/processed/ under shorter names
  * copies results/data_audit.json with the collusion.wiki section removed, because that
    archive is a separate incident whose download page carries a no-sharing banner
  * copies README.md, LICENSE, LICENSE-CODE, source_manifest.json and fetch_and_verify.py
  * fills the {{...}} tokens in README.md with the repository id, author, git commit and
    GitHub path
  * checks every row count in README.md against the file it describes and stops on a
    mismatch, so the card cannot ship a number the data does not support
"""

import argparse
import csv
import json
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

# Source name in this repository, name in the uploaded folder, rows the card claims.
TABLES = [
    ("data/processed/metr_agents.csv", "agents.csv", 1206),
    ("data/processed/metr_workstream_counts.csv", "workstream_counts.csv", 12404),
    ("data/processed/metr_cohort_followup.csv", "cohort_followup.csv", 18),
]

COPY_AS_IS = ["LICENSE", "LICENSE-CODE", "source_manifest.json", "fetch_and_verify.py"]

# Key in data_audit.json, value the card states.
AUDIT_CHECKS = {
    "agent_rows": 1206,
    "positioned_hf_onsets": 684,
    "declared_verified_hf_participants": 688,
    "hf_before_board_read": 15,
    "missing_board_write": 60,
    "observed_stop_flags": 47,
    "workstream_sparse_rows": 1772,
    "workstreams": 22,
    "communicative_purposes": 7,
}


def git_commit():
    try:
        return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "main"


def row_count(path):
    with path.open(newline="") as handle:
        return sum(1 for _ in csv.reader(handle)) - 1


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-id", required=True,
                        help="Hub dataset id, for example yourname/openai-hf-incident-recovered-tables")
    parser.add_argument("--author", required=True, help="author name for the citation block")
    parser.add_argument("--github-repo", default="",
                        help="owner/name of a public GitHub repository holding the extraction "
                             "code, for example LauraGomezjurado/openai-hf. Leave it unset while "
                             "that repository is private. The card then says the code is not "
                             "published yet instead of printing a link nobody can open.")
    parser.add_argument("--out", default=str(HERE / "staging"),
                        help="folder to write. It is emptied first.")
    args = parser.parse_args()

    out = pathlib.Path(args.out).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    problems = []

    for source_name, target_name, claimed in TABLES:
        source = ROOT / source_name
        if not source.exists():
            problems.append(f"{source_name} is missing")
            continue
        shutil.copy2(source, out / target_name)
        actual = row_count(out / target_name)
        flag = "ok" if actual == claimed else "MISMATCH"
        if actual != claimed:
            problems.append(f"{target_name} has {actual} rows, the card says {claimed}")
        print(f"  {target_name:<24} {actual:>6} rows  ({flag})")

    audit = json.loads((ROOT / "results/data_audit.json").read_text())
    dropped = audit.pop("wiki_separate_incident", None)
    audit["cautions"] = [c for c in audit["cautions"] if "Wiki" not in c]
    audit["note"] = ("The collusion.wiki section of this file is removed in the published "
                     "copy. That archive is a separate incident and its download page "
                     "carries a no-sharing banner.")
    (out / "data_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(f"  {'data_audit.json':<24} wiki section removed: {dropped is not None}")

    for key, claimed in AUDIT_CHECKS.items():
        actual = audit.get(key)
        if actual != claimed:
            problems.append(f"data_audit.json {key} is {actual}, the card says {claimed}")

    for name in COPY_AS_IS:
        shutil.copy2(HERE / name, out / name)
        print(f"  {name:<24} copied")

    if args.github_repo:
        base = f"https://github.com/{args.github_repo}/blob/{git_commit()}"
        code_link = f"Code that produced the tables: <{base}/scripts/audit_public_data.py>"
        rebuild = (f"To rebuild the tables from scratch, run `fetch_and_verify.py` from a clone "
                   f"of <https://github.com/{args.github_repo}>, then run "
                   f"`scripts/audit_public_data.py`. That script also reads two files from "
                   f"collusion.wiki that are left out here, so `data_audit.json` will only "
                   f"rebuild in full if you download those separately. The three CSV files "
                   f"rebuild from the metr.org files alone.")
    else:
        code_link = ("The code that produced these tables is not published yet. This card will "
                     "link it when it is.")
        rebuild = ("Rebuilding the tables from the source files needs the extraction code, which\n"
                   "is not published yet. Until then, `source_manifest.json` and this script are\n"
                   "what let you confirm the tables were derived from the bytes they claim.")

    tokens = {
        "{{REPO_ID}}": args.repo_id,
        "{{CODE_LINK}}": code_link,
        "{{REBUILD}}": rebuild,
        "{{AUTHOR}}": args.author,
        "{{BIBTEX_KEY}}": args.repo_id.split("/")[-1].replace("-", "_") + "_2026",
    }
    card = (HERE / "README.md").read_text()
    for token, value in tokens.items():
        card = card.replace(token, value)
    left = [line for line in card.splitlines() if "{{" in line]
    if left:
        problems.append(f"README.md still holds unfilled tokens: {left}")
    (out / "README.md").write_text(card)
    print(f"  {'README.md':<24} {len(tokens)} tokens filled")

    print()
    if problems:
        print("Stopped. Fix these before uploading:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    total = sum(p.stat().st_size for p in out.iterdir())
    print(f"Wrote {len(list(out.iterdir()))} files to {out} ({total / 1024:.0f} KiB).")
    print("Every row count and audit number in the card matches the data.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
