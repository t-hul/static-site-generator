import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leafnode_to_html_h1(self):
        node = LeafNode("h1", "Front-end delopment is the Worst")
        self.assertEqual(node.to_html(), "<h1>Front-end delopment is the Worst</h1>")

    def test_leafnode_to_html_b(self):
        node = LeafNode("b", "This is bold text")
        self.assertEqual(node.to_html(), "<b>This is bold text</b>")

    def test_leafnode_to_html_none(self):
        node = LeafNode(None, "This is plain text")
        self.assertEqual(node.to_html(), "This is plain text")


if __name__ == "__main__":
    unittest.main()
