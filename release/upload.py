"""Build the release folder and upload it to the Hugging Face Hub.

    .venv-convert/bin/python release/upload.py \
        --repo-id YOURNAME/openai-hf-incident-recovered-tables \
        --author "Your Name"

Which account gets used
-----------------------

This machine is used with more than one Hugging Face account. The script will not upload
until the logged in account owns the namespace in --repo-id. If you pass
--repo-id alice/thing and you are logged in as bob, it stops and tells you so.

It also refuses to push into an organization namespace. Pass --allow-org if you have
decided that is what you want.

To pick the account for one run without changing what is stored on disk, pass a token
directly:

    --token hf_...

Or read it from a file so it stays out of your shell history:

    --token-file ~/personal-hf-token.txt

With neither option the script uses whatever `hf auth login` last stored, and prints the
account name before it asks you to confirm. Read that line.

Publishing
----------

The repository is created private. Look at it on the Hub, then make it public from the
dataset settings page or by passing --public on a later run. The script prints the file
list and waits for you to type the repository id back before it sends anything.

Generate the DOI last, from the dataset settings page. Once a DOI exists, deleting,
renaming or hiding the dataset needs a support request.
"""

import argparse
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent

COMMIT_MESSAGE = ("Tables recovered from the chart data published with METR's OpenAI and "
                  "Hugging Face incident report")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-id", required=True, help="for example yourname/openai-hf-incident-recovered-tables")
    parser.add_argument("--author", required=True, help="author name for the citation block")
    parser.add_argument("--github-repo", default="",
                        help="owner/name of a public GitHub repository holding the extraction "
                             "code. Unset means the card says the code is not published yet.")
    parser.add_argument("--public", action="store_true",
                        help="create the dataset public. The default is private.")
    parser.add_argument("--token", help="use this token for one run instead of the stored login")
    parser.add_argument("--token-file", help="read the token from this file")
    parser.add_argument("--allow-org", action="store_true",
                        help="permit uploading into an organization namespace")
    parser.add_argument("--yes", action="store_true", help="skip the typed confirmation")
    args = parser.parse_args()

    if "/" not in args.repo_id:
        print(f"--repo-id needs an owner and a name, for example yourname/{args.repo_id}")
        return 1
    owner = args.repo_id.split("/", 1)[0]

    token = args.token
    if args.token_file:
        if token:
            print("Pass one of --token and --token-file. Both were given.")
            return 1
        token_path = pathlib.Path(args.token_file).expanduser()
        if not token_path.is_file():
            print(f"No such token file: {token_path}")
            return 1
        token = token_path.read_text().strip()
        if not token:
            print(f"The token file is empty: {token_path}")
            return 1

    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("huggingface_hub is not installed. Run: pip install -U huggingface_hub")
        return 1

    build = subprocess.run([sys.executable, str(HERE / "build_release.py"),
                            "--repo-id", args.repo_id,
                            "--author", args.author,
                            "--github-repo", args.github_repo])
    if build.returncode != 0:
        print("The build failed, so nothing was uploaded.")
        return 1

    staging = HERE / "staging"
    files = sorted(staging.iterdir())

    api = HfApi(token=token)
    try:
        identity = api.whoami()
    except Exception as error:
        print(f"Not logged in to the Hub ({error}).")
        print("Run `hf auth login` with the account you want to publish under, or pass")
        print("--token or --token-file to this script.")
        return 1

    who = identity["name"]
    orgs = sorted(org["name"] for org in identity.get("orgs", []))

    print()
    print("Account this run would use")
    print(f"  username    {who}")
    if identity.get("fullname"):
        print(f"  full name   {identity['fullname']}")
    if identity.get("email"):
        print(f"  email       {identity['email']}")
    print(f"  token from  {'--token-file' if args.token_file else '--token' if args.token else 'the stored login on this machine'}")
    print(f"  member of   {', '.join(orgs) if orgs else 'no organizations'}")
    print()

    if owner != who and not (owner in orgs and args.allow_org):
        print(f"Stopped. --repo-id names the owner '{owner}' and this run is '{who}'.")
        if owner in orgs:
            print(f"'{owner}' is an organization you belong to. Add --allow-org to upload there.")
        else:
            print("Change --repo-id, or log in as the account that owns that namespace, or")
            print("pass --token for the right account. Then run this again.")
        return 1

    if owner in orgs:
        print(f"Uploading into the organization '{owner}' because --allow-org was passed.")

    print(f"About to upload {len(files)} files to {args.repo_id} "
          f"({'public' if args.public else 'private'}):")
    for path in files:
        print(f"  {path.name:<24} {path.stat().st_size / 1024:>8.1f} KiB")
    print()
    print("The six source files from metr.org are not in this list. That is intended.")
    print("The collusion.wiki files are not in this list either. That is also intended.")
    print()

    if not args.yes:
        typed = input("Type the repository id to upload, or anything else to stop: ").strip()
        if typed != args.repo_id:
            print("Stopped. Nothing was uploaded.")
            return 1

    api.create_repo(repo_id=args.repo_id, repo_type="dataset",
                    private=not args.public, exist_ok=True)
    url = api.upload_folder(folder_path=str(staging), repo_id=args.repo_id,
                            repo_type="dataset", commit_message=COMMIT_MESSAGE)
    print()
    print(f"Uploaded. {url}")
    print(f"Dataset page: https://huggingface.co/datasets/{args.repo_id}")
    print()
    print("Next:")
    print("  1. Read the rendered card and open the Data Studio viewer on all three tables.")
    print("  2. Make the dataset public from the settings page.")
    print("  3. Email METR that it is up, with the report link and this dataset link.")
    print("  4. Generate the DOI from the settings page, after the content is settled.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
