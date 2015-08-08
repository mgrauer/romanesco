import romanesco
import networkx as nx
from networkx.algorithms.isomorphism import is_isomorphic, numerical_edge_match
import unittest
from lxml import etree


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.GRAPHML_NS = '{http://graphml.graphdrawing.org/xmlns}'
        self.test_input = {
            'distances': {
                'format': 'graph',
                'data': nx.Graph([
                    ('US', 'UK', {'distance': 4242}),
                    ('US', 'Australia', {'distance': 9429}),
                    ('UK', 'Australia', {'distance': 9443}),
                    ('US', 'Japan', {'distance': 6303})
                ])
            }
        }


    def test_graphml(self):
        # @todo i notice tests asserting output format,
        # is this covered somewhere else?
        output = romanesco.convert('graph',
                                   self.test_input['distances'],
                                   {'format': 'graphml'})
        expected_edges = set(self.test_input['distances']['data'].edges(
            data='distance'))
        actual_edges = set()

        # @todo covered by validator?
        self.assertIsInstance(output['data'], (str, unicode))
        tree = etree.fromstring(output['data'])
        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0].tag, self.GRAPHML_NS + 'key')
        self.assertEqual(tree[1].tag, self.GRAPHML_NS + 'graph')

        for edge in tree[1].findall(self.GRAPHML_NS + 'edge'):
            edge = (edge.attrib['source'],
                    edge.attrib['target'],
                    int(edge.find(self.GRAPHML_NS + 'data').text))

            self.assertNotIn(edge, actual_edges)
            actual_edges.add(edge)

        self.assertEqual(expected_edges, actual_edges)

        output = romanesco.convert('graph',
                                   output,
                                   {'format': 'graph'})

        self.assertTrue(
            is_isomorphic(output['data'],
                          self.test_input['distances']['data'],
                          edge_match=numerical_edge_match('distance', 1)))


if __name__ == '__main__':
    unittest.main()
