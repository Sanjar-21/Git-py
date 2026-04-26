import hashlib
import json
import os
import sys

COMMANDS = ["init", "add", "commit", "status"]
MYGIT = ".mygit"
INDEX = f"{MYGIT}/index.json"
HEAD = f"{MYGIT}/HEAD"
COMMITS = f"{MYGIT}/commits"


def init():
    if os.path.exists(MYGIT):
        print("Already initialized")
        return
    os.mkdir(MYGIT)
    os.mkdir(COMMITS)
    with open(INDEX, "w") as f:
        json.dump({}, f)
    with open(HEAD, "w") as f:
        f.write("None")
    print("Initialized empty repository")


def add(file):
    if not os.path.exists(MYGIT):
        print("Repository not initialized")
        return
    if not os.path.exists(file):
        print(f"File not found: {file}")
        return

    with open(file, "rb") as f:
        sha1 = hashlib.sha1(f.read()).hexdigest()

    with open(INDEX, "r") as f:
        index = json.load(f)
    index[file] = sha1
    with open(INDEX, "w") as f:
        json.dump(index, f)
    print(f"Added {file}")


def commit(message):
    if not os.path.exists(MYGIT):
        print("Repository not initialized")
        return

    with open(INDEX, "r") as f:
        index = json.load(f)
    if not index:
        print("Nothing to commit")
        return

    with open(HEAD, "r") as f:
        parent = f.read().strip()

    commit_data = {"message": message, "parent": parent, "files": index}
    commit_hash = hashlib.sha1(
        json.dumps(commit_data, sort_keys=True).encode()
    ).hexdigest()

    with open(f"{COMMITS}/{commit_hash}.json", "w") as f:
        json.dump(commit_data, f)

    with open(HEAD, "w") as f:
        f.write(commit_hash)

    print(f"Committed: {commit_hash[:7]} {message}")


def status():
    if not os.path.exists(MYGIT):
        print("Repository not initialized")
        return

    with open(INDEX, "r") as f:
        index = json.load(f)

    with open(HEAD, "r") as f:
        head = f.read().strip()

    # Get files from last commit
    committed = {}
    if head != "None" and os.path.exists(f"{COMMITS}/{head}.json"):
        with open(f"{COMMITS}/{head}.json", "r") as f:
            committed = json.load(f)["files"]

    staged_new, staged_modified = [], []
    for file, sha1 in index.items():
        if file not in committed:
            staged_new.append(file)
        elif committed[file] != sha1:
            staged_modified.append(file)

    if staged_new or staged_modified:
        print("Changes to be committed:")
        for f in staged_new:
            print(f"  new file:  {f}")
        for f in staged_modified:
            print(f"  modified:  {f}")
    else:
        print("Nothing to commit, working tree clean")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"Usage: git.py <{'|'.join(COMMANDS)}>")
        return

    cmd = sys.argv[1]

    if cmd == "init":
        init()
    elif cmd == "add":
        if len(sys.argv) != 3:
            print("Usage: git.py add <file>")
            return
        add(sys.argv[2])
    elif cmd == "commit":
        if len(sys.argv) != 3:
            print('Usage: git.py commit "<message>"')
            return
        commit(sys.argv[2])
    elif cmd == "status":
        status()


if __name__ == "__main__":
    main()
