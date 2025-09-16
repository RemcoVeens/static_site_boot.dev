import shutil
import sys
import os
from functions import generate_pages_recursive
from pathlib import Path


def mover(source_dir, destination_dir):
    """
    Write a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public)
        It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
        It should copy all files and subdirectories, nested files, etc.
        I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.
    """
    print("cleaning destination directory...")
    Path(destination_dir).mkdir(parents=True, exist_ok=True)
    shutil.rmtree(destination_dir)
    print("Copying files...")
    shutil.copytree(source_dir, destination_dir)
    print(os.listdir(destination_dir))


def main(basepath):
    source_dir = "static"
    destination_dir = "docs"
    mover(source_dir, destination_dir)
    generate_pages_recursive(
        Path("content"), "template.html", Path(destination_dir), basepath=basepath
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    # print(basepath)
    main(basepath)
