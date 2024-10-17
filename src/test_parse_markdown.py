import unittest
from imp import new_module

from src.parse_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, \
    split_nodes_image, text_to_textnodes, markdown_to_blocks
from src.textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def test_nothingToSplit(self):
        old_nodes = [
            TextNode('Here is some text', TextType.TEXT),
            TextNode('Here is some more text.', TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '**', TextType.BOLD)

        self.assertEqual(old_nodes, new_nodes)

        old_nodes = [
            TextNode('Here is some text', TextType.TEXT),
            TextNode('Here is some more text.', TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '*', TextType.ITALIC)

        self.assertEqual(old_nodes, new_nodes)

        old_nodes = [
            TextNode('Here is some text', TextType.TEXT),
            TextNode('Here is some more text.', TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '`', TextType.CODE)

        self.assertEqual(old_nodes, new_nodes)

    def test_splitBold(self):
        old_nodes = [
            TextNode('Here is some **bold** text', TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '**', TextType.BOLD)
        expected_nodes = [
            TextNode('Here is some ', TextType.TEXT),
            TextNode('bold', TextType.BOLD),
            TextNode(' text', TextType.TEXT)
        ]

        self.assertEqual(expected_nodes, new_nodes)

    def test_splitItalic(self):
        old_nodes = [
            TextNode('Here is some *italic* text', TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '*', TextType.ITALIC)
        expected_nodes = [
            TextNode('Here is some ', TextType.TEXT),
            TextNode('italic', TextType.ITALIC),
            TextNode(' text', TextType.TEXT)
        ]

        self.assertEqual(expected_nodes, new_nodes)

    def test_splitCode(self):
        old_nodes = [
            TextNode('Here is some `code` text', TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '`', TextType.CODE)
        expected_nodes = [
            TextNode('Here is some ', TextType.TEXT),
            TextNode('code', TextType.CODE),
            TextNode(' text', TextType.TEXT)
        ]

        self.assertEqual(expected_nodes, new_nodes)

    def test_appendList(self):
        old_nodes = [
            TextNode('Here is some text', TextType.TEXT),
            TextNode('Here is some **bold** text', TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '**', TextType.BOLD)

        expected_nodes = [
            TextNode('Here is some text', TextType.TEXT),
            TextNode('Here is some ', TextType.TEXT),
            TextNode('bold', TextType.BOLD),
            TextNode(' text', TextType.TEXT)
        ]

        self.assertEqual(expected_nodes, new_nodes)

    def test_boldTest(self):
        old_nodes = [
            TextNode('Here is some text', TextType.BOLD),
            TextNode('Here is some **bold** text', TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '**', TextType.BOLD)

        expected_nodes = [
            TextNode('Here is some text', TextType.BOLD),
            TextNode('Here is some ', TextType.TEXT),
            TextNode('bold', TextType.BOLD),
            TextNode(' text', TextType.TEXT)
        ]

        self.assertEqual(expected_nodes, new_nodes)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_noMatch(self):
        text = 'Nothing to see here!'
        images = extract_markdown_images(text)
        expected = []
        self.assertEqual(expected, images)

    def test_singleMatch(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        images = extract_markdown_images(text)
        expected = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif')]
        self.assertEqual(expected, images)

    def test_multipleMatches(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        expected = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(expected, images)

    def test_noMatchForLink(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        images = extract_markdown_images(text)
        expected = []
        self.assertEqual(expected, images)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_noMatch(self):
        text = 'Nothing to see here!'
        links = extract_markdown_links(text)
        expected = []
        self.assertEqual(expected, links)

    def test_singleMatch(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        links = extract_markdown_links(text)
        expected = [('to boot dev', 'https://www.boot.dev')]
        self.assertEqual(expected, links)

    def test_multipleMatches(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        expected = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(expected, links)

    def test_noMatchForAnImage(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        links = extract_markdown_links(text)
        expected = []
        self.assertEqual(expected, links)


class TestSplitNodesImage(unittest.TestCase):
    def test_noImage(self):
        old_nodes = [TextNode('This is text with no image', TextType.TEXT), TextNode('This is bold text', TextType.BOLD)]
        new_nodes = split_nodes_image(old_nodes)
        expected = [TextNode('This is text with no image', TextType.TEXT), TextNode('This is bold text', TextType.BOLD)]
        self.assertEqual(expected, new_nodes)

    def test_singleImage(self):
        old_nodes = [
            TextNode(
                "![rick roll](https://i.imgur.com/aKaOqIh.gif)",
                TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected = [
            TextNode('rick roll', TextType.IMAGE, 'https://i.imgur.com/aKaOqIh.gif'),
        ]
        self.assertEqual(expected, new_nodes)

    def test_paddedImage(self):
        old_nodes = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ",
                TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected = [
            TextNode('This is text with a ', TextType.TEXT),
            TextNode('rick roll', TextType.IMAGE, 'https://i.imgur.com/aKaOqIh.gif'),
            TextNode(' and ', TextType.TEXT),
        ]
        self.assertEqual(expected, new_nodes)

    def test_multipleImages(self):
        old_nodes = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected = [
            TextNode('This is text with a ', TextType.TEXT),
            TextNode('rick roll', TextType.IMAGE, 'https://i.imgur.com/aKaOqIh.gif'),
            TextNode(' and ', TextType.TEXT),
            TextNode('obi wan', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg')
        ]
        self.assertEqual(expected, new_nodes)

    def test_multipleNodesAndImages(self):
        old_nodes = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT),
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected = [
            TextNode('This is text with a ', TextType.TEXT),
            TextNode('rick roll', TextType.IMAGE, 'https://i.imgur.com/aKaOqIh.gif'),
            TextNode(' and ', TextType.TEXT),
            TextNode('obi wan', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
            TextNode('This is text with a ', TextType.TEXT),
            TextNode('rick roll', TextType.IMAGE, 'https://i.imgur.com/aKaOqIh.gif'),
            TextNode(' and ', TextType.TEXT),
            TextNode('obi wan', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg')
        ]
        self.assertEqual(expected, new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_noLink(self):
        old_nodes = [TextNode("This is text with no link", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode('This is text with no link', TextType.TEXT),
        ]
        self.assertEqual(expected, new_nodes)

    def test_singleLink(self):
        old_nodes = [TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
        ]
        self.assertEqual(expected, new_nodes)

    def test_paddedLink(self):
        old_nodes = [
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and ",
                TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode('This is text with a link ', TextType.TEXT),
            TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
            TextNode(' and ', TextType.TEXT),
        ]
        self.assertEqual(expected, new_nodes)

    def test_multipleLinks(self):
        old_nodes = [
            TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode('This is text with a link ', TextType.TEXT),
            TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
            TextNode(' and ', TextType.TEXT),
            TextNode('to youtube', TextType.LINK, 'https://www.youtube.com/@bootdotdev')
        ]
        self.assertEqual(expected, new_nodes)

    def test_multipleLinksAndNodes(self):
        old_nodes = [
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT),
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode('This is text with a link ', TextType.TEXT),
            TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
            TextNode(' and ', TextType.TEXT),
            TextNode('to youtube', TextType.LINK, 'https://www.youtube.com/@bootdotdev'),
            TextNode('This is text with a link ', TextType.TEXT),
            TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
            TextNode(' and ', TextType.TEXT),
            TextNode('to youtube', TextType.LINK, 'https://www.youtube.com/@bootdotdev')
        ]
        self.assertEqual(expected, new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_emptyText(self):
        text = ''
        nodes = text_to_textnodes(text)
        expected = []
        self.assertEqual(expected, nodes)

    def test_allNodes(self):
        text = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(expected, nodes)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_emptyString(self):
        text = ''
        blocks = markdown_to_blocks(text)
        self.assertEqual([], blocks)

    def test_multipleBlocks(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        blocks = markdown_to_blocks(text)
        expected = [
        '# This is a heading',
        'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
        """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        ]

        self.assertEqual(expected, blocks)

    def test_singleBlock(self):
        text = '# This is a heading'
        blocks = markdown_to_blocks(text)

        self.assertEqual(['# This is a heading'], blocks)

if __name__ == '__main__':
    unittest.main()
