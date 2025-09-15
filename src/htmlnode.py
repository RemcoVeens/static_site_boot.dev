class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ):
        """
        tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        children - A list of HTMLNode objects representing the children of this node
        props - A dictionary of key-value pairs representing the attributes of the HTML tag.
        For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        """
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        return f"HTMLNode({self.tag=}, {self.value=}, {self.children=}, {self.props=})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict | None = None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        main = f"{self.value}"
        if self.tag:
            if self.props:
                main = f"<{self.tag} {self.props_to_html()}>{main}</{self.tag}>"
            else:
                main = f"<{self.tag}>{main}</{self.tag}>"
        return main


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str | None, children: list | None, props: dict | None = None
    ):
        super().__init__(tag, None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        if self.props:
            main = f"<{self.tag} {self.props_to_html()}>"
        else:
            main = f"<{self.tag}>"
        for child in self.children:
            main += child.to_html()
        main += f"</{self.tag}>"
        return main
