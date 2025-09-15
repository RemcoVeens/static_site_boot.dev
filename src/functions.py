import re
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode
from blocks import BlockType


def text_node_to_html_node(text_node: TextNode | None) -> HTMLNode:
    assert text_node is not None, "Text node cannot be None"
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unsupported text node type")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splits = node.text.split(delimiter)
        for index, split in enumerate(splits):
            if not split:
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(split, node.text_type))
            else:
                new_nodes.append(TextNode(split, text_type))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"\!\[([^\]]*)\]\(([^)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[([^\]]*)\]\(([^)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    pattern = r"(\!\[[^\]]*\]\([^)]*\))"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splits = re.split(pattern, node.text)
        for index, split in enumerate(splits):
            if not split:
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(split, node.text_type))
            else:
                matches = extract_markdown_images(split)[0]
                new_nodes.append(TextNode(matches[0], TextType.IMAGE, url=matches[1]))
    return new_nodes


def split_nodes_link(old_nodes):
    pattern = r"(\[[^\]]*\]\([^)]*\))"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splits = re.split(pattern, node.text)
        for index, split in enumerate(splits):
            if not split:
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(split, node.text_type))
            else:
                matches = extract_markdown_links(split)[0]
                new_nodes.append(TextNode(matches[0], TextType.LINK, matches[1]))
    return new_nodes


def text_to_textnodes(text) -> list[TextNode]:
    base = [TextNode(text, TextType.TEXT)]
    base = split_nodes_delimiter(base, delimiter="**", text_type=TextType.BOLD)
    base = split_nodes_delimiter(base, delimiter="_", text_type=TextType.ITALIC)
    base = split_nodes_delimiter(base, delimiter="`", text_type=TextType.CODE)
    base = split_nodes_image(base)
    base = split_nodes_link(base)
    return base


def markdown_to_blocks(markdown):
    return [block.strip("\n") for block in markdown.split("\n\n") if block]


def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("-"):
        return BlockType.UNORDERED_LIST
    elif block.startswith("1."):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
