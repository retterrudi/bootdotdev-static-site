import unittest

from src.textnode import TextNode


class TextTextNode(unittest.TestCase):
    def test_TextNode_eq(self):
        node = TextNode('This is a text node', 'bold')
        node2 = TextNode('This is a text node', 'bold')
        self.assertEqual(node, node2)

    def test_TextNode_eqWithGivenUrl_areEqual(self):
        node = TextNode('This is a text node', 'bold', 'https://boot.dev')
        node2 = TextNode('This is a text node', 'bold', 'https://boot.dev')
        self.assertEqual(node, node2)

    def test_TextNode_eqWithDifferingProperties_areNotEqual(self):
        node = TextNode('This is a text node', 'bold')
        node2 = TextNode('This is a text node', 'text')
        self.assertNotEqual(node, node2)


if __name__ == '__main__':
    unittest.main()
