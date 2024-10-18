import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.parse_markdown import block_to_heading, block_to_code, block_to_paragraph, block_to_quote, \
    block_to_ordered_list, block_to_unordered_list, markdown_to_html_node


class TestBlockToHeading(unittest.TestCase):
    def test_firstLevelHeading(self):
        block = '# This is a first level heading'
        node = block_to_heading(block)
        expected = ParentNode('h1', [LeafNode(None, 'This is a first level heading')])
        self.assertEqual(str(expected), str(node))

    def test_secondLevelHeading(self):
        block =  '## This is a second level heading'
        node = block_to_heading(block)
        expected = ParentNode('h2', [LeafNode(None, 'This is a second level heading')])
        self.assertEqual(str(expected), str(node))

    def test_sixthLevelHeading(self):
        block =  '###### This is a sixth level heading'
        node = block_to_heading(block)
        expected = ParentNode('h6', [LeafNode(None, 'This is a sixth level heading')])
        self.assertEqual(str(expected), str(node))

class TestBlockToCode(unittest.TestCase):
    def test_singleLine(self):
        block = '```This is a code block```'
        node = block_to_code(block)
        expected = HTMLNode(
            tag='pre',
            value=None,
            children=[HTMLNode(
                tag='code',
                value='This is a code block',
                children=None,
                props=None
            )],
            props=None
        )
        self.assertEqual(str(expected), str(node))

    def test_multiLine(self):
        block = """```This is a code block
That covers more than one line```"""
        node = block_to_code(block)
        expected = HTMLNode(
            tag='pre',
            value=None,
            children=[HTMLNode(
                tag='code',
                value="""This is a code block
That covers more than one line""",
                children=None,
                props=None
            )],
            props=None
        )
        self.assertEqual(str(expected), str(node))


class TestBlockToParagraph(unittest.TestCase):
    def test_simpleText(self):
        block = 'This is just a simple and plain text'
        node = block_to_paragraph(block)
        expected = ParentNode(
            tag='p',
            children=[LeafNode(
                tag=None,
                value='This is just a simple and plain text',
                props=None
            )],
            props=None
        )
        self.assertEqual(str(expected), str(node))

    def test_textWithBoldInline(self):
        block = 'This is text containing **bold** parts'
        node = block_to_paragraph(block)
        expected = ParentNode(
            tag='p',
            children=[
                LeafNode(None, 'This is text containing ', None),
                LeafNode('b', 'bold', None),
                LeafNode(None, ' parts', None)],
            props=None
        )
        self.assertEqual(str(expected), str(node))

    def test_textWithBoldAndItalicInline(self):
        block = 'This is *text* containing **bold** parts'
        node = block_to_paragraph(block)
        expected = ParentNode(
            tag='p',
            children=[
                LeafNode(None, 'This is ', None),
                LeafNode('i', 'text', None),
                LeafNode(None, ' containing ', None),
                LeafNode('b', 'bold', None),
                LeafNode(None, ' parts', None)],
            props=None
        )
        self.assertEqual(str(expected), str(node))


class TestBlockToQuote(unittest.TestCase):
    def test_singleLineQuote(self):
        block = '>This is a quote'
        node = block_to_quote(block)
        expected = ParentNode(
            'blockquote',
            [LeafNode(None, 'This is a quote', None)],
            None
        )
        self.assertEqual(str(expected), str(node))

    def test_multiLineQuote(self):
        block = """>This is a quote
>that covers two lines"""
        node = block_to_quote(block)
        expected_value = """This is a quote
that covers two lines"""
        expected = ParentNode(
            'blockquote',
            [LeafNode(None, expected_value, None)],
            None
        )
        self.assertEqual(str(expected), str(node))

    def test_quoteWithInlineBold(self):
        block = '>This **is** a quote'
        node = block_to_quote(block)
        expected = ParentNode(
            'blockquote',
            [
                LeafNode(None, 'This ', None),
                LeafNode('b', 'is', None),
                LeafNode(None, ' a quote', None)],
            None
        )
        self.assertEqual(str(expected), str(node))

    def test_multiLineQuoteWithInlineBold(self):
        block = """>This is a quote
>that covers **two** lines"""
        node = block_to_quote(block)
        expected = ParentNode(
            'blockquote',
            [
                LeafNode(None, 'This is a quote\nthat covers ', None),
                LeafNode('b', 'two', None),
                LeafNode(None, ' lines', None)
            ],
            None
        )
        self.assertEqual(str(expected), str(node))


class TestBlockToOrderedList(unittest.TestCase):
    def test_multipleListItems(self):
        block = """1. Eins
2. Zwei
3. Drei
4. Vier
5. Fünf
6. Sechs
7. Sieben
8. Acht
9. Neun
10. Zehn"""
        node = block_to_ordered_list(block)
        expected = ParentNode(
            'ol',
            [
                ParentNode('li', [LeafNode(None, 'Eins')]),
                ParentNode('li', [LeafNode(None, 'Zwei')]),
                ParentNode('li', [LeafNode(None, 'Drei')]),
                ParentNode('li', [LeafNode(None, 'Vier')]),
                ParentNode('li', [LeafNode(None, 'Fünf')]),
                ParentNode('li', [LeafNode(None, 'Sechs')]),
                ParentNode('li', [LeafNode(None, 'Sieben')]),
                ParentNode('li', [LeafNode(None, 'Acht')]),
                ParentNode('li', [LeafNode(None, 'Neun')]),
                ParentNode('li', [LeafNode(None, 'Zehn')]),
            ]
        )
        self.assertEqual(str(expected), str(node))

    def test_multipleListItemsWithInlineBold(self):
        block = """1. Eins **1**
        2. Zwei
        3. Drei
        4. Vier
        5. Fünf
        6. Sechs
        7. Sieben
        8. Acht
        9. Neun
        10. Zehn"""
        node = block_to_ordered_list(block)
        expected = ParentNode(
            'ol',
            [
                ParentNode('li', [LeafNode(None, 'Eins '), LeafNode('b', '1')]),
                ParentNode('li', [LeafNode(None, 'Zwei')]),
                ParentNode('li', [LeafNode(None, 'Drei')]),
                ParentNode('li', [LeafNode(None, 'Vier')]),
                ParentNode('li', [LeafNode(None, 'Fünf')]),
                ParentNode('li', [LeafNode(None, 'Sechs')]),
                ParentNode('li', [LeafNode(None, 'Sieben')]),
                ParentNode('li', [LeafNode(None, 'Acht')]),
                ParentNode('li', [LeafNode(None, 'Neun')]),
                ParentNode('li', [LeafNode(None, 'Zehn')]),
            ]
        )
        self.assertEqual(str(expected), str(node))

    def test_singleListItem(self):
        block = """1. Eins"""
        node = block_to_ordered_list(block)
        expected = ParentNode(
            'ol',
            [
                ParentNode('li', [LeafNode(None, 'Eins')]),
            ]
        )
        self.assertEqual(str(expected), str(node))

    def test_singleListItemWithInlineBold(self):
        block = """1. Eins**Zwei**"""
        node = block_to_ordered_list(block)
        expected = ParentNode(
            'ol',
            [
                ParentNode('li', [LeafNode(None, 'Eins'), LeafNode('b', 'Zwei')]),
            ]
        )
        self.assertEqual(str(expected), str(node))


class TestBlockToUnorderedList(unittest.TestCase):
    def test_multipleListItems(self):
        block = """- One
-  Two
- Three
- Four"""
        node = block_to_unordered_list(block)
        expected = ParentNode(
            'ul',
            [
                ParentNode('li', [LeafNode(None, 'One')]),
                ParentNode('li', [LeafNode(None, 'Two')]),
                ParentNode('li', [LeafNode(None, 'Three')]),
                ParentNode('li', [LeafNode(None, 'Four')]),
            ]
        )
        self.assertEqual(str(expected), str(node))

    def test_multipleListItemsWithInlineBold(self):
        block = """- One **1**
- Two
- Three
- Four"""
        node = block_to_unordered_list(block)
        expected = ParentNode(
            'ul',
            [
                ParentNode('li', [LeafNode(None, 'One '), LeafNode('b', '1')]),
                ParentNode('li', [LeafNode(None, 'Two')]),
                ParentNode('li', [LeafNode(None, 'Three')]),
                ParentNode('li', [LeafNode(None, 'Four')]),
            ]
        )
        self.assertEqual(str(expected), str(node))


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_twoBlocks(self):
        markdown = """# This is the heading

And this is some text"""
        node = markdown_to_html_node(markdown)
        expected = ParentNode(
            'div',
            [
                ParentNode('h1', [LeafNode(None, 'This is the heading')]),
                ParentNode('p', [LeafNode(None, 'And this is some text')])
            ]
        )
        self.assertEqual(str(expected), str(node))


if __name__ == '__main__':
    unittest.main()
