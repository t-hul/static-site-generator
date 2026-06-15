import unittest

from src.block_markdown import (
    BlockType,
    block_to_block_type,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Header one
# Header two

No header
"""
        title = extract_title(md)
        self.assertEqual(title, "Header one")

    def test_extract_no_title(self):
        md = """
No header

Still no header # here
"""
        self.assertRaisesRegex(
            Exception,
            "No 'h1' header found in markdown file",
            extract_title,
            md,
        )


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

    def test_code_newline(self):
        block = """```
test code
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_code_multi_line(self):
        block = """```
test code
more code
```"""
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


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# Main Heading

## Second heading with _italics_

####### This has too many levels
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Heading</h1><h2>Second heading with <i>italics</i></h2><p>####### This has too many levels</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
    > quote1
    >quote2
> quote3 **bold**
        >quote4 _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote> quote1\nquote2\n quote3 <b>bold</b>\nquote4 <i>italic</i></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
    - first item
    - second item with - inside
        - third **bold** item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second item with - inside</li><li>third <b>bold</b> item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
    1. first item
    2. second item with 4. inside
        3. third **bold** item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item with 4. inside</li><li>third <b>bold</b> item</li></ol></div>",
        )
