import unittest

from src.htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_ParentNode_singleLeafNodes(self):
        node = ParentNode(
            'p',
            [
                LeafNode('b', 'Bold text'),
            ],
        )
        html = node.to_html()
        expected = '<p><b>Bold text</b></p>'
        self.assertEqual(expected, html)

    def test_ParentNode_severalLeafNodes(self):
        node = ParentNode(
            'p',
            [
                LeafNode('b', 'Bold text'),
                LeafNode(None, 'Normal text'),
                LeafNode('i', 'italic text'),
                LeafNode(None, 'Normal text'),
            ],
        )
        html = node.to_html()
        expected = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(expected, html)

    def test_ParentNode_singleNestedParentNodes(self):
        inner_node = ParentNode(
            'p',
            [
                LeafNode('b', 'Bold text'),
                LeafNode(None, 'Normal text'),
                LeafNode('i', 'italic text'),
                LeafNode(None, 'Normal text'),
            ],
        )
        outer_node = ParentNode(
            'p',
            [inner_node]
        )

        html = outer_node.to_html()
        expected = '<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>'

        self.assertEqual(expected, html)

    def test_ParentNode_nestedParentNodes(self):
        inner_node = ParentNode(
            'p',
            [
                LeafNode('b', 'Bold text'),
                LeafNode(None, 'Normal text'),
                LeafNode('i', 'italic text'),
                LeafNode(None, 'Normal text'),
            ],
        )
        outer_node = ParentNode(
            'p',
            [inner_node, inner_node]
        )

        html = outer_node.to_html()
        expected = '<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>'

        self.assertEqual(expected, html)

    def test_ParentNode_noChildren(self):
        node = ParentNode(
            'p'
        )
        node2 = ParentNode(
            'p',
            props={'href': 'https://www.google.com'}
        )

        with self.assertRaises(ValueError):
            node.to_html()
        with self.assertRaises(ValueError):
            node2.to_html()

    def test_ParentNode_noTag(self):
        node = ParentNode(
            children = [
                LeafNode('b', 'Bold text'),
                LeafNode(None, 'Normal text'),
                LeafNode('i', 'italic text'),
                LeafNode(None, 'Normal text'),
            ],
        )

        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == '__main__':
    unittest.main()
