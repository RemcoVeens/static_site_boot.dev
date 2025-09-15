from enum import Enum

class TextType(Enum):
    # TEXT = ""
    # BOLD = "**Bold text**"
    # ITALIC = "_Italic text_"
    # CODE = "`Code text`"
    # LINK = "[anchor text](url)"
    # IMAGES = "![alt text](url)"
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGES = "images"

class TextNode:
    def __init__(self, text, text_type:TextType, url:str|None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def __eq__(self, other):
        return all([
            self.text == other.text,
            self.text_type == other.text_type,
            self.url == other.url
        ])
