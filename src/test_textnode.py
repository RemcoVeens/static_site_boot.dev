import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        node2 = TextNode("This is a text node", TextType.BOLD, url)
        self.assertEqual(node2.url, url)

    def test_diff(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a not text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
