import os

def createDir(path):
    "Create dir in the specified path"
    if os.path.exists(path):
        os.mkdir(path)

if __name__ == "__main__":
    pass