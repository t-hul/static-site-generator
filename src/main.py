from .page import generate_pages_recursive
from .utils import copy_tree


def main():
    copy_tree("static", "public")
    generate_pages_recursive("content", "template.html", "public")


main()
