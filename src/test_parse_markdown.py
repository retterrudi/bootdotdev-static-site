import unittest

from src.parse_markdown import split_nodes_delimiter
from src.textnode import TextNode, TextType


class MyTestCase(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
