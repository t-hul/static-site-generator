import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_many_newline(self):
        md = """

This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single(self):
        md = "This is **bolded** paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is **bolded** paragraph"],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_single(self):
        block = "# Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_no_space(self):
        block = "#Heading"
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_heading_level6(self):
        block = "###### Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_level7(self):
        block = "####### Heading"
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_heading_different_start(self):
        block = "s# Heading"
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_code(self):
        block = """```
        test code```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_code_no_newline(self):
        block = """```test code```"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_quote(self):
        block = """> one
> two
> three"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_no_space(self):
        block = """>one
>two
>three"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_not_first(self):
        block = """one
> two
> three"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.QUOTE)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_quote_not_second(self):
        block = """> one
two
> three"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.QUOTE)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered(self):
        block = """- one
- two
- three"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_unordered_leading_space(self):
        block = """- one
                   - two
                   - three"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_unordered_no_space(self):
        block = """-one
-two
-three"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.UNORDERED_LIST)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered_not_second(self):
        block = """- one
two
- three"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.UNORDERED_LIST)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered(self):
        block = """1. one
2. two
3. three"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_leading_space(self):
        block = """1. one
                   2. two
                   3. three"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_not_starting_at_one(self):
        block = """2. one
3. two
4. three"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_not_increasing(self):
        block = """1. one
3. two
3. three"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_no_dot(self):
        block = """1. one
2 two
3. three"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_no_space(self):
        block = """1. one
2.two
3. three"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
