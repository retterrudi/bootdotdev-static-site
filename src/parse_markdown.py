import re
from typing import List

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

def split_nodes_image(old_nodes: List['TextNode']) -> List['TextNode']:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
            else:
                text = node.text
                for (alt_text, url) in images:
                    split_text = text.split(f'![{alt_text}]({url})')
                    if split_text[0] != '':
                        new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                    split_text.pop(0)
                    text = ''.join(split_text)
                if text != '':
                    new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: List['TextNode']) -> List['TextNode']:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
            else:
                text = node.text
                for (alt_text, url) in links:
                    split_text = text.split(f'[{alt_text}]({url})')
                    if split_text[0] != '':
                        new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                    split_text.pop(0)
                    text = ''.join(split_text)
                if text != '':
                    new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text: str) -> List[tuple]:
    pattern = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text: str) -> List[tuple]:
    pattern = r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches

def text_to_textnodes(text: str) -> List['TextNode']:
    old_nodes = [TextNode(text, TextType.TEXT)]
    bold_nodes = split_nodes_delimiter(old_nodes, '**', TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, '*', TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, '`', TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    return link_nodes
