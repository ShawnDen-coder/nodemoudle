import unittest
from unittest import TestCase

from src import make_item_class


class TestMakeItemClass(TestCase):

    def test_create_class(self):
        Item = make_item_class('data', 'parent', 'children')

        data = ['item1']
        parent = None
        children = []

        item = Item(data=data, parent=parent, children=children)
        self.assertEqual(item.data, data)
        self.assertEqual(item.parent, parent)
        self.assertEqual(item.children, children)

        child_item = Item(data=['child_item1'], parent=None, children=[])
        item.addChild(child_item)

        expected_dict = {
            'data': ['item1'],
            'parent': None,
            'children': [
                {
                    'data': ['child_item1'],
                    'parent': {'data': ['item1'], 'parent': None, 'children': []},
                    'children': []
                }
            ]}

        self.assertEqual(item.to_dict(), expected_dict)

        expected_json = '{"data": ["item1"], "parent": null, "children": [{"data": ["child_item1"], "parent": {"data": ["item1"], "parent": null, "children": []}, "children": []}]}'
        self.assertEqual(item.to_json(), expected_json)

        expected_yaml = 'data: [item1]\nparent: null\nchildren:\n- data: [child_item1]\n  parent: {data: [item1], parent: null, children: []}\n  children: []\n'
        self.assertEqual(item.to_yaml(), expected_yaml)

        expected_xml = '<?xml version=\'1.0\' encoding=\'unicode\'?><item><data>item1</data><item><data>child_item1</data></item></item>'
        self.assertEqual(item.to_xml(), expected_xml)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)