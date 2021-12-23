import os

def delete(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print("ERROR: path not found")

def create(path):
    print("TODO: def create(path)")