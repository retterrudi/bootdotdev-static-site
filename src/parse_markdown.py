from typing import List, Tuple
import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(
        old_nodes: List['TextNode'],
        delimiter: str,
        text_type: TextType
) -> List['TextNode']:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
        else:
            new_nodes.extend(split_single_node(node, delimiter))

    return new_nodes


def split_single_node(node: 'TextNode', delimiter: str) -> List['TextNode']:
    text_type_dict = {'`': TextType.CODE, '*': TextType.ITALIC, '**': TextType.BOLD}

    if not text_type_dict.__contains__(delimiter):
        raise ValueError(f'Unexpected delimiter: {delimiter}')

    blocks = node.text.split(delimiter)

    if len(blocks) % 2 == 0:
        raise ValueError(f'Invalid Markdown syntax in node: {node}')

    new_nodes: List['TextNode'] = []
    for index, block in enumerate(blocks):
        if block == '':
            continue
        if index % 2 == 0:
            new_nodes.append(TextNode(block, TextType.TEXT))
        else:
            new_nodes.append(TextNode(block, text_type_dict[delimiter]))
    return new_nodes


def extract_markdown_images(text: str) -> List[tuple]:
    pattern = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text: str) -> List[tuple]:
    pattern = r'[^!]\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches
