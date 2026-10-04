import os
import sys

from huggingface_hub import (
    HfApi,
    CommitOperationCopy,
    CommitOperationDelete,
)

REPO_ID = "Esmaeil9ss/Tickdata"

TOKEN = os.environ["HF_TOKEN"]
OLD_FOLDER = os.environ["OLD_FOLDER"].strip().strip("/")
NEW_FOLDER = os.environ["NEW_FOLDER"].strip().strip("/")

if not OLD_FOLDER:
    print("ERROR: Old folder name is empty.")
    sys.exit(1)

if not NEW_FOLDER:
    print("ERROR: New folder name is empty.")
    sys.exit(1)

if OLD_FOLDER == NEW_FOLDER:
    print("ERROR: Old and new folder names are identical.")
    sys.exit(1)

print("=" * 60)
print("Hugging Face Folder Rename")
print("=" * 60)
print(f"Repository : {REPO_ID}")
print(f"Old folder : {OLD_FOLDER}")
print(f"New folder : {NEW_FOLDER}")
print("=" * 60)

api = HfApi(token=TOKEN)

print("\nReading repository files...")

files = api.list_repo_files(
    repo_id=REPO_ID,
    repo_type="dataset",
)

old_prefix = OLD_FOLDER + "/"

target_files = [
    file_path
    for file_path in files
    if file_path.startswith(old_prefix)
]

if not target_files:
    print()
    print(f"ERROR: No files found inside '{OLD_FOLDER}/'")
    print()
    print("Available top-level paths:")

    top_level = sorted(
        set(
            f.split("/")[0]
            for f in files
        )
    )

    for item in top_level:
        print(f"  - {item}")

    sys.exit(1)

print(f"\nFound {len(target_files)} file(s).")
print("\nFiles that will be moved:\n")

operations = []

for file_path in target_files:

    relative_path = file_path[len(old_prefix):]

    new_path = NEW_FOLDER + "/" + relative_path

    print(f"{file_path}")
    print(f"  -> {new_path}")
    print()

    operations.append(
        CommitOperationCopy(
            src_path_in_repo=file_path,
            path_in_repo=new_path,
        )
    )

    operations.append(
        CommitOperationDelete(
            path_in_repo=file_path,
        )
    )

print("=" * 60)
print("Creating commit...")
print("=" * 60)

api.create_commit(
    repo_id=REPO_ID,
    repo_type="dataset",
    operations=operations,
    commit_message=(
        f"Rename folder '{OLD_FOLDER}' "
        f"to '{NEW_FOLDER}'"
    ),
)

print()
print("=" * 60)
print("SUCCESS")
print("=" * 60)
print(f"Folder renamed: {OLD_FOLDER} -> {NEW_FOLDER}")
print(f"Files moved: {len(target_files)}")
print("File names were NOT changed.")
print("=" * 60)
