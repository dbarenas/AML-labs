import json
import unittest
from pathlib import Path

import networkx as nx
from networkx_demo.demo_networkx import build_graph
from networkx_demo.models import TransactionEdge


class NetworkXRingTest(unittest.TestCase):
    def setUp(self) -> None:
        data_path = Path(__file__).resolve().parent.parent / "data" / "transactions_data.json"
        with data_path.open() as stream:
            raw_edges = json.load(stream)
        self.edges = [TransactionEdge(**edge) for edge in raw_edges]

    def test_ring_component_is_detected(self) -> None:
        graph = build_graph(self.edges)
        components = nx.strongly_connected_components(graph)
        target_component = {"A901", "A902", "A903"}
        self.assertIn(target_component, components, "El anillo de fraude no fue detectado correctamente")


if __name__ == "__main__":
    unittest.main()
