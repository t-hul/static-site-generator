import re
from typing import List

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        split_nodes = []
        if len(split_text) % 2 == 0:
            raise Exception(
                f'Text node "{node.text}" does not contain matching pair of "{delimiter}" delimiter'
            )
        for i, part in enumerate(split_text):
            if part == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(part, TextType.TEXT))
            else:
                split_nodes.append(TextNode(part, text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
