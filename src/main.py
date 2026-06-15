from .page import generate_page
from .utils import copy_tree


def main():
    copy_tree("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


main()
