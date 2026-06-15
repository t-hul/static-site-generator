import sys

from .page import generate_pages_recursive
from .utils import copy_tree


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_tree("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
