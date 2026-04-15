import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_html_node_properties(self):
        node = HTMLNode(
            "test_tag", "test_value", None, {"key1": "value1", "key2": "value2"}
        )
        self.assertEqual(node.tag, "test_tag")
        self.assertEqual(node.value, "test_value")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"key1": "value1", "key2": "value2"})

    def test_repr_tag(self):
        node = HTMLNode(
            tag="test_tag",
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=test_tag, value=None, children=None, props=None)",
        )

    def test_repr_value(self):
        node = HTMLNode(
            value="test_value",
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=None, value=test_value, children=None, props=None)",
        )

    def test_repr_children(self):
        node = HTMLNode(
            tag="test_tag",
            value="test_value",
        )
        node2 = HTMLNode(children=[node])
        self.assertEqual(
            repr(node2),
            "HTMLNode(tag=None, value=None, children=[HTMLNode(tag=test_tag, value=test_value, children=None, props=None)], props=None)",
        )

    def test_repr_props(self):
        node = HTMLNode(
            props={"key1": "value1", "key2": "value2"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=None, value=None, children=None, props={'key1': 'value1', 'key2': 'value2'})",
        )

    def test_props_to_html(self):
        node = HTMLNode(
            props={"key1": "value1", "key2": "value2"},
        )
        self.assertEqual(node.props_to_html(), ' key1="value1" key2="value2"')

    def test_none_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
