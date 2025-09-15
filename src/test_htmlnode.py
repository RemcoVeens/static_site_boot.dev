import unittest

from htmlnode import HTMLNode, LeafNode ,ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_empty(self):
        HTMLNode()


    def test_props_to_html(self):
        input = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        output = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(HTMLNode(props=input).props_to_html(), output)

    def test_props(self):
        node = HTMLNode("div", props={"class": "container"})
        self.assertEqual(node.props["class"], "container")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):
    def test_parrent_node(self):
        result = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        ).to_html()
        self.assertEqual(result, '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_no_kids(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)


    def test_no_tag(self):
        parent_node = ParentNode(None, None)
        self.assertRaises(ValueError, parent_node.to_html)


if __name__ == "__main__":
    unittest.main()
