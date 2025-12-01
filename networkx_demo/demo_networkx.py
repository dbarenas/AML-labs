from __future__ import annotations

import json
from pathlib import Path

import networkx as nx
from networkx_demo.models import TransactionEdge

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "transactions_data.json"


def build_graph(edges: list[TransactionEdge]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for edge in edges:
        graph.add_edge(edge.source, edge.target)
    return graph


def main() -> None:
    with DATA_FILE.open() as stream:
        raw_edges = json.load(stream)
    edges = [TransactionEdge(**edge) for edge in raw_edges]

    graph = build_graph(edges)
    centrality = nx.betweenness_centrality(graph)
    components = nx.strongly_connected_components(graph)

    print("Centralidad de intermediación (nodos clave):")
    for node, value in centrality.items():
        print(f"  {node}: {value:.3f}")

    print("\nComponentes fuertemente conectados:")
    for component in components:
        print(sorted(component))


if __name__ == "__main__":
    main()
