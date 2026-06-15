import re
from enum import Enum
from typing import List

from .htmlnode import HTMLNode
from .inline_markdown import text_to_textnodes
from .parentnode import ParentNode
from .textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:]
    raise Exception("No 'h1' header found in markdown file")


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    blocknodes = []
    for block in blocks:
        blocknodes.append(block_to_parent(block))
    root_parent = ParentNode("div", blocknodes)
    return root_parent


def block_to_parent(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise Exception(f"Markdown block has unknown block_type: {block_type}")


def paragraph_to_html_node(block: str) -> HTMLNode:
    block = block.replace("\n", " ")
    children = text_to_children(block)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> HTMLNode:
    levels, text = block.split(" ", maxsplit=1)
    tag = f"h{len(levels)}"
    children = text_to_children(text)
    return ParentNode(tag, children)


def code_to_html_node(block: str) -> HTMLNode:
    block = block.removeprefix("```\n")
    block = block.removesuffix("```")
    textnode = TextNode(block, TextType.CODE)
    htmlnode = text_node_to_html_node(textnode)
    return ParentNode("pre", children=[htmlnode])


def quote_to_html_node(block: str) -> HTMLNode:
    lines = []
    for line in block.splitlines():
        lines.append(line.split(">", maxsplit=1)[1])
    text = "\n".join(lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block: str) -> HTMLNode:
    items = []
    for line in block.splitlines():
        text = line.split("- ", maxsplit=1)[1]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", children=items)


def ordered_list_to_html_node(block: str) -> HTMLNode:
    items = []
    for line in block.splitlines():
        text = line.split(". ", maxsplit=1)[1]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", children=items)


def text_to_children(text: str) -> List[HTMLNode]:
    children = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        children.append(text_node_to_html_node(textnode))
    return children


def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            stripped_blocks.append(stripped_block)
    return stripped_blocks


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6}\s.+", block):
        return BlockType.HEADING
    if re.match(r"^```\n[\s\S]+```$", block):
        return BlockType.CODE
    if re.fullmatch(r"^(?:\s*>\s?.+(?:\n|$))+", block):
        return BlockType.QUOTE
    if re.fullmatch(r"^(?:\s*-\s.+(?:\n|$))+", block):
        return BlockType.UNORDERED_LIST
    if _is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def _is_ordered_list(block: str) -> bool:
    lines = block.splitlines()
    numbers = []
    for line in lines:
        match = re.match(r"^(\d+)\.\s.+$", line.strip())
        if not match:
            return False
        numbers.append(int(match.group(1)))

    return numbers == list(range(1, len(numbers) + 1))
