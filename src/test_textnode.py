import unittest

from src.textnode import TextNode, TextType


class TextTextNode(unittest.TestCase):
    def test_TextNode_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node2)

    def test_TextNode_eqWithGivenUrl_areEqual(self):
        node = TextNode('This is a text node', TextType.BOLD, 'https://boot.dev')
        node2 = TextNode('This is a text node', TextType.BOLD, 'https://boot.dev')
        self.assertEqual(node, node2)

    def test_TextNode_eqWithDifferingProperties_areNotEqual(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.ITALIC)
        self.assertNotEqual(node, node2)


if __name__ == '__main__':
    unittest.main()
