import os
import shutil


def copy_tree(source: str, target: str):
    if os.path.isdir(target):
        print(f"Removing content from target '{target}'")
        shutil.rmtree(target)
    os.mkdir(target)
    source_content = os.listdir(source)
    for item in source_content:
        item_path = os.path.join(source, item)
        if os.path.isfile(item_path):
            print(f"Copy '{item_path}' to '{target}'")
            shutil.copy(item_path, target)
        elif os.path.isdir(item_path):
            copy_tree(item_path, os.path.join(target, item))
