import unittest

import distancematrix

class SimpleTestCase(unittest.TestCase):
    def test_simple(self):
        pairs = [(1, 2),
                 (2, 3),
                 (7, 8),
                 (9, 10)]
        print distancematrix.matrix_calls(pairs)

    def test_edges(self):
        edges = []
        with open('/tmp/edges') as f:
            for line in f:
                row = line.split()
                edges.append((int(row[0]), int(row[1])))

        print distancematrix.matrix_calls(edges, 10)

    def test_lobster(self):
        import networkx as nx
        import matplotlib.pyplot as plt
        g = nx.random_lobster(15, 0.8, 0.1)
        nx.draw_graphviz(g)
        plt.savefig("/tmp/lobster.png")
        print distancematrix.matrix_calls(g.edges(), 20)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleTestCase))
    return suite
