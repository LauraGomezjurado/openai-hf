"""Download the published source files and check each one against a recorded SHA-256.

The tables in this dataset were derived from six files published on metr.org and on a
Hugging Face static space. Those six files are not redistributed here. This script
downloads them from their original URLs and compares each download to the SHA-256
recorded in source_manifest.json on 2026-09-06.

    python3 fetch_and_verify.py                 # download into ./data/raw/... and check
    python3 fetch_and_verify.py --dest /tmp/x   # download somewhere else
    python3 fetch_and_verify.py --check-only    # check files already on disk

Each file is reported as one of four results:

    MATCH       the bytes are identical to the 2026-09-06 copy.
    DOCUMENTED  the bytes changed, and this exact SHA-256 is already recorded in
                source_manifest.json under known_changes, with a note on what changed.
    CHANGED     the bytes changed and the new SHA-256 is not recorded. Fetch both
                copies and diff them before drawing any conclusion. A hash tells you
                that something changed. It does not tell you what.
    MISSING     the file could not be downloaded or was not found on disk.

Exit code 0 means every file was MATCH or DOCUMENTED. Exit code 1 means at least one
was CHANGED or MISSING.

The manifest marks two files with "affects_tables": true. Those two are the ones the
CSV tables are derived from. If those two report MATCH, the tables in this dataset can
still be reproduced from the current published files. The other four were read for
context, so a change in them leaves the tables alone and may still change how you read
the report.

Only the standard library is used. Downloaded JavaScript is written to disk and hashed.
It is never executed.
"""

import argparse
import hashlib
import json
import pathlib
import sys
import urllib.error
import urllib.request

MANIFEST = pathlib.Path(__file__).resolve().parent / "source_manifest.json"
TIMEOUT_SECONDS = 60
USER_AGENT = "openai-hf-recovered-tables/1.0 (source verification script)"


def download(url, target):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        body = response.read()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(body)
    return len(body)


def check_one(source, target, check_only):
    """Return (result, digest, note). result is MATCH, DOCUMENTED, CHANGED or MISSING."""
    if check_only:
        if not target.exists():
            return "MISSING", None, f"expected at {target}"
    else:
        try:
            download(source["url"], target)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as error:
            return "MISSING", None, f"{source['url']} {error}"

    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if digest == source["sha256"]:
        return "MATCH", digest, ""
    for change in source.get("known_changes", []):
        if change["sha256"] == digest:
            return "DOCUMENTED", digest, f"recorded {change['observed_date']}: {change['summary']}"
    return "CHANGED", digest, ""


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dest", default=".",
                        help="directory the paths in source_manifest.json are written under")
    parser.add_argument("--check-only", action="store_true",
                        help="hash files already present under --dest and skip downloading")
    args = parser.parse_args()

    dest = pathlib.Path(args.dest).resolve()
    sources = json.loads(MANIFEST.read_text())
    tally = {"MATCH": 0, "DOCUMENTED": 0, "CHANGED": 0, "MISSING": 0}
    tables_reproducible = True

    for source in sources:
        result, digest, note = check_one(source, dest / source["path"], args.check_only)
        tally[result] += 1
        if result != "MATCH" and source["affects_tables"]:
            tables_reproducible = False

        print(f"{result:<11}{source['path']}")
        if digest and result != "MATCH":
            print(f"           recorded on {source['retrieved_date']}: {source['sha256']}")
            print(f"           on disk now:            {digest}")
        elif digest:
            print(f"           {digest}")
        if note:
            for line in _wrap(note, 66):
                print(f"           {line}")

    print()
    print(f"{tally['MATCH']} matched, {tally['DOCUMENTED']} changed as documented, "
          f"{tally['CHANGED']} changed without a record, {tally['MISSING']} missing.")
    if tables_reproducible:
        print("Both files the tables are derived from are unchanged, so the CSV files in "
              "this dataset can be rebuilt from the current published sources.")
    else:
        print("At least one file the tables are derived from has changed, so the CSV files "
              "in this dataset may no longer match the current published sources.")
    return 1 if tally["CHANGED"] or tally["MISSING"] else 0


def _wrap(text, width):
    words, line, lines = text.split(), "", []
    for word in words:
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        lines.append(line)
    return lines


if __name__ == "__main__":
    sys.exit(main())
