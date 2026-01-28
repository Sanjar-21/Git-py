import hashlib
import json
import os
import sys

argments = ["init", "add", "commit", "status"] # git commands

def main_init():
    if len(sys.argv) != 2:
        print("Error")
        return

    argment = sys.argv[1]
        

    if argment not in argments:
        print("Error not commit error")
        return

    if (argment == "init" and not os.path.exists(".mygit")):
        # create add folder mygit and mygit/commits
        os.mkdir(".mygit/")
        os.mkdir(".mygit/commits")
        # json add file create
        with open(".mygit/index.json", "w") as f:
            f.write("{}")
        # HEAD add file create
        with open(".mygit/HEAD", "w") as file:
            file.write("None")
    
def main_add():
    # if len sys.argv not 3 break
    if len(sys.argv) != 3:
        print("Error")
        return
    

    argv, file = sys.argv[1], sys.argv[2]

    if not os.path.exists(".mygit"):
        print("Repository not initialized")
        return

    if argv != "add":
        print(f"Not found: {argv}")
        return
    
    if not os.path.exists(file):
        print(f"File not found: {file}")
        return
    
    with open(file, "rb") as f:
        file_obj = f.read()
        hash_obj = hashlib.sha1(file_obj)
        sha1 = hash_obj.hexdigest()
    
    with open(".mygit/index.json", "r") as f:
        file_data = json.load(f)
        file_data[file] = sha1
    
    with open(".mygit/index.json", "w") as f:
        json.dump(file_data, f)
        

    
    


    
    
        

if __name__ == "__main__":

    # main_init()
    main_add()
