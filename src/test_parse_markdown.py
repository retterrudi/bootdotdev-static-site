import unittest

from src.parse_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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


if __name__ == '__main__':
    unittest.main()
