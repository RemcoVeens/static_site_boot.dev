import re
from pathlib import Path

from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
from blocks import BlockType


def text_node_to_html_node(text_node: TextNode | None) -> LeafNode:
    assert text_node is not None, "Text node cannot be None"
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text.replace("\n", " "))
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


def text_to_textnodes(text: str) -> list[TextNode]:
    base = [TextNode(text, TextType.TEXT)]
    base = split_nodes_delimiter(base, delimiter="**", text_type=TextType.BOLD)
    base = split_nodes_delimiter(base, delimiter="_", text_type=TextType.ITALIC)
    base = split_nodes_delimiter(base, delimiter="`", text_type=TextType.CODE)
    base = split_nodes_image(base)
    base = split_nodes_link(base)
    return base


def markdown_to_blocks(markdown: str) -> list[str]:
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


def text_to_children(text):
    return [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]


# def markdown_to_html_node(markdown):
#     blocks = markdown_to_blocks(markdown)
#     children = []
#     for block in blocks:
#         block_type = block_to_block_type(block)
#         match block_type:
#             case BlockType.HEADING:
#                 level = len(block.split(" ")[0])
#                 children.append(
#                     ParentNode(
#                         f"h{level}",
#                         children=text_to_children(block.lstrip("# ").strip()),
#                     )
#                 )
#             case BlockType.CODE:
#                 code_content = block.strip("`").lstrip("\n")
#                 code_html_node = LeafNode(None, code_content)
#                 children.append(
#                     ParentNode("pre", children=[ParentNode("code", children=[code_html_node])])
#                 )
#             case BlockType.QUOTE:
#                 children.append(
#                     ParentNode("blockquote", children=text_to_children(block.strip("> ").strip()))
#                 )
#             case BlockType.UNORDERED_LIST:
#                 children.append(ParentNode("ul", children=text_to_children(block)))
#             case BlockType.ORDERED_LIST:
#                 children.append(ParentNode("ol", children=text_to_children(block)))
#             case BlockType.PARAGRAPH:
#                 children.append(ParentNode("p", children=text_to_children(block)))
#             case _:
#                 raise ValueError(f"Unknown block type: {block_type}")
#     return ParentNode("div", children=children)
def parse_list_items(block, list_marker):
    """
    Parses a block of markdown list text into a list of ParentNodes (for <li>).

    Args:
        block: The markdown string representing the list.
        list_marker: The marker for unordered lists (e.g., "- ") or None for ordered lists.

    Returns:
        A list of ParentNodes, where each node represents an <li> element.
    """
    items = []
    lines = block.split("\n")
    for line in lines:
        if list_marker is not None:
            if line.startswith(list_marker):
                item_content = line.lstrip(list_marker).strip()
                items.append(ParentNode("li", children=text_to_children(item_content)))
        else:  # Ordered list
            # For ordered lists, we need to strip the number and space, e.g., "1. "
            parts = line.split(". ", 1)
            if len(parts) == 2:
                item_content = parts[1].strip()
                items.append(ParentNode("li", children=text_to_children(item_content)))
            elif (
                line.strip()
            ):  # Handle cases where the line might just be text after a number
                items.append(ParentNode("li", children=text_to_children(line.strip())))
    return items


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                level = len(block.split(" ")[0])
                children.append(
                    ParentNode(
                        f"h{level}",
                        children=text_to_children(block.lstrip("# ").strip()),
                    )
                )
            case BlockType.CODE:
                code_content = block.strip("`").lstrip("\n")
                code_html_node = LeafNode(None, code_content)
                children.append(
                    ParentNode(
                        "pre", children=[ParentNode("code", children=[code_html_node])]
                    )
                )
            case BlockType.QUOTE:
                lines = block.split("\n")
                cleaned_lines = [line.lstrip("> ").strip() for line in lines]
                cleaned_block = " ".join(cleaned_lines)
                children.append(
                    ParentNode("blockquote", children=text_to_children(cleaned_block))
                )
            case BlockType.UNORDERED_LIST:
                # Correctly parse list items
                list_items = parse_list_items(block, "- ")
                children.append(ParentNode("ul", children=list_items))
            case BlockType.ORDERED_LIST:
                # Correctly parse list items
                list_items = parse_list_items(
                    block, None
                )  # Use None for ordered list, as numbers are part of the content
                children.append(ParentNode("ol", children=list_items))
            case BlockType.PARAGRAPH:
                children.append(ParentNode("p", children=text_to_children(block)))
            case _:
                raise ValueError(f"Unknown block type: {block_type}")
    return ParentNode("div", children=children)  # Assuming a root div, adjust as needed


def extract_title(markdown):
    """
    Extracts the title from a markdown string.
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line[1:].strip()
    else:
        raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path, basepath):
    dest_path = Path(*dest_path.parts[:1], *dest_path.parts[2:])
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    title = extract_title(markdown)
    with open(template_path, "r") as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    content = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    content = content.replace('href="/', f'href="{basepath}').replace(
        'src="/', f'src="{basepath}'
    )
    Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(content)


def generate_pages_recursive(
    dir_path: Path, template_path: str, dest_dir_path: Path, basepath: str
):
    for file_path in dir_path.iterdir():
        if file_path.is_file() and file_path.suffix == ".md":
            generate_page(
                file_path,
                template_path,
                Path(dest_dir_path) / Path(file_path).with_suffix(".html"),
                basepath,
            )
        elif file_path.is_dir():
            generate_pages_recursive(file_path, template_path, dest_dir_path, basepath)
