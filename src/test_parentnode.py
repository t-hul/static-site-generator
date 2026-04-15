import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_no_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_no_children_none(self):
        parent_node = ParentNode("div", None)
        self.assertRaisesRegex(
            ValueError, "ParentNode must have children", parent_node.to_html
        )

    def test_to_html_with_many_children(self):
        child_node1 = LeafNode("b", "Bold text")
        child_node2 = LeafNode(None, "Normal text")
        child_node3 = LeafNode("i", "italic text")
        child_node4 = LeafNode(None, "Normal text")
        parent_node = ParentNode(
            "p", [child_node1, child_node2, child_node3, child_node4]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_nested_children(self):
        child_node1 = LeafNode("h1", "Heading")
        grandchild_node1 = LeafNode("b", "Bold text")
        grandchild_node2 = LeafNode(None, "Normal text")
        grandchild_node3 = LeafNode("i", "italic text")
        grandchild_node4 = LeafNode(None, "Normal text")
        child_node2 = ParentNode(
            "p",
            [grandchild_node1, grandchild_node2, grandchild_node3, grandchild_node4],
        )
        grandgrandchild_node = LeafNode("b", "grandchild")
        grandchild_node = ParentNode("span", [grandgrandchild_node])
        child_node3 = ParentNode("div", [grandchild_node])
        parent_node = ParentNode("p", [child_node1, child_node2, child_node3])

        self.assertEqual(
            parent_node.to_html(),
            "<p><h1>Heading</h1><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><div><span><b>grandchild</b></span></div></p>",
        )


if __name__ == "__main__":
    unittest.main()
