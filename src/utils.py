import os
import shutil


def copy_tree(source: str, target: str):
    if os.path.isdir(target):
        shutil.rmtree(target)
    else:
        raise RuntimeError(f"Target directory '{target}' does not exist.")
