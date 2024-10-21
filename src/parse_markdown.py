import re
from enum import Enum
from typing import List

from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html


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

def markdown_to_blocks(markdown: str) -> List[str]:
    raw_blocks = markdown.split('\n\n')
    filtered_blocks = filter(lambda block: block != '', raw_blocks)
    trimmed_blocks = [block.strip() for block in filtered_blocks]

    return trimmed_blocks

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'


def block_to_block_type(block: str) -> 'BlockType':
    if is_heading_block(block):
        return BlockType.HEADING
    elif is_code_block(block):
        return BlockType.CODE
    elif is_quote_block(block):
        return BlockType.QUOTE
    elif is_unordered_list_block(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list_block(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def is_heading_block(block: str) -> bool:
    return block.startswith(('#', '##', '###', '####', '#####', '######'))

def is_code_block(block: str) -> bool:
    return block.startswith('```') and block.endswith('```')

def is_quote_block(block: str) -> bool:
    lines = block.split('\n')
    for line in lines:
        if not line.startswith('>'):
            return False
    return True

def is_unordered_list_block(block: str) -> bool:
    lines = block.split('\n')
    for line in lines:
        if not line.startswith(('- ', '* ')):
            return False
    return True

def is_ordered_list_block(block: str) -> bool:
    lines = block.split('\n')
    for index, line in enumerate(lines):
        if not line.startswith(f'{index + 1}.'):
            return False
    return True

def markdown_to_html_node(markdown: str) -> 'HTMLNode':
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            child_nodes.append(block_to_heading(block))
        elif block_type == BlockType.CODE:
            child_nodes.append(block_to_code(block))
        elif block_type == BlockType.QUOTE:
            child_nodes.append(block_to_quote(block))
        elif block_type == BlockType.ORDERED_LIST:
            child_nodes.append(block_to_ordered_list(block))
        elif block_type == BlockType.UNORDERED_LIST:
            child_nodes.append(block_to_unordered_list(block))
        elif block_type == BlockType.PARAGRAPH:
            child_nodes.append(block_to_paragraph(block))
        else:
            raise ValueError(f'Unknown block type: {block_type}')

    return ParentNode('div', child_nodes, None)

def block_to_heading(block: str) -> 'HTMLNode':
    split_block = block.split('#')
    heading_level = len(split_block) - 1
    text = str(split_block[-1]).strip()
    return ParentNode(
        tag = f'h{heading_level}',
        children=[LeafNode(None, text, None)],
        props=None)

def block_to_quote(block: str) -> 'HTMLNode':
    lines = block.splitlines(True)
    lines = map(lambda line: str(line).removeprefix('>').strip(), lines)
    text = ''.join(lines)
    return ParentNode(
        tag='blockquote',
        children=list(map(lambda it: text_node_to_html(it), text_to_textnodes(text))),
        props=None,
    )

def block_to_unordered_list(block: str) -> 'HTMLNode':
    return ParentNode(
        tag='ul',
        children=[ParentNode(
            'li',
            children=list(map(
                lambda it: text_node_to_html(it),
                text_to_textnodes(line[2:].strip())))) for line in block.splitlines(True)
        ],
        props=None
    )

def block_to_ordered_list(block: str) -> 'HTMLNode':
    return ParentNode(
        tag='ol',
        children=[
            ParentNode(
                'li',
                children=list(map(
                    lambda it: text_node_to_html(it),
                    text_to_textnodes(line.split('. ', 1)[1].strip())))) for line in block.splitlines(True)
        ],
        props=None
    )

def block_to_code(block: str) -> 'HTMLNode':
    # <pre>
    #   <code>...
    #   </code>
    # </pre>
    return ParentNode(
        tag='pre',
        children=[
            LeafNode(
                tag='code',
                value=block.removeprefix('```').removesuffix('```').strip(),
                props=None
            )
        ],
        props=None
    )

def block_to_paragraph(block: str) -> 'HTMLNode':
    return ParentNode(
        tag='p',
        children=list(map(lambda it: text_node_to_html(it), text_to_textnodes(block))),
        props=None
    )

def extract_title(markdown: str) -> str:
    lines = markdown.splitlines(False)

    for line in lines:
        if line.startswith('# '):
            return line.removeprefix('# ').strip()
    raise ValueError('No title found')


