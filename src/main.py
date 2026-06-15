from .textnode import TextNode, TextType
from .utils import copy_tree


def main():
    copy_tree("static", "public")
    dummy_node = TextNode(
        "This is some dummy text", TextType.LINK, "https://www.boot.dev"
    )
    print(dummy_node)


main()
