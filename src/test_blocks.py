import unittest
from functions import block_to_block_type, markdown_to_blocks
from blocks import BlockType


class TestBlock(unittest.TestCase):
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

    def test_block_to_block_type(self):
        self.assertEqual(
            block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH
        )

    def test_block_to_paragraph(self):
        self.assertEqual(
            block_to_block_type(
                "This is a paragraph\nThis is the same paragraph on a new line"
            ),
            BlockType.PARAGRAPH,
        )

    def test_block_to_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- This is a list\n- with items"),
            BlockType.UNORDERED_LIST,
        )

    def test_block_to_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. This is a numbered list\n2. with items"),
            BlockType.ORDERED_LIST,
        )

    def test_block_to_quote(self):
        self.assertEqual(
            block_to_block_type("> i love you 3000"),
            BlockType.QUOTE,
        )

    def test_block_to_block_code(self):
        self.assertEqual(
            block_to_block_type("```python\nprint('Hello World')\n```"),
            BlockType.CODE,
        )

    def test_block_to_block_heading(self):
        self.assertEqual(
            block_to_block_type("# you should have gone for the head"),
            BlockType.HEADING,
        )
