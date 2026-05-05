import re
from enum import Enum
from typing import List

from parentnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)


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
    if re.match(r"^```\n.+```$", block):
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
