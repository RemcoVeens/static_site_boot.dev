import shutil
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
    shutil.rmtree(destination_dir)
    print("Copying files...")
    shutil.copytree(source_dir, destination_dir)
    print(os.listdir(destination_dir))


def main():
    source_dir = "static"
    destination_dir = "public"
    mover(source_dir, destination_dir)
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive(Path("content"), "template.html", Path("public"))


if __name__ == "__main__":
    main()
