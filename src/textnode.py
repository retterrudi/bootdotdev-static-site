from enum import Enum
from typing import Union

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'


class TextNode:
    def __init__(self, text, text_type: TextType, url = None):
        self.text: str = text
        self.text_type: str = text_type.value
        self.url: Union[str|None] = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
            )
        return False

    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type}, {self.url})'


def text_node_to_html(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT.value:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD.value:
        return LeafNode('b', text_node.text)
    if text_node.text_type == TextType.ITALIC.value:
        return LeafNode('i', text_node.text)
    if text_node.text_type == TextType.CODE.value:
        return LeafNode('code', text_node.text)
    if text_node.text_type == TextType.LINK.value:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    if text_node.text_type == TextType.IMAGE.value:
        return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
    raise ValueError(f'Invalid text type: {text_node.text_type}')
