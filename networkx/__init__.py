from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, Iterable, Iterator, List, Set, Tuple


class DiGraph:
    def __init__(self) -> None:
        self._adj: Dict[str, Set[str]] = defaultdict(set)

    def add_edge(self, u: str, v: str, amount: float | None = None) -> None:
        self._adj[u].add(v)
        self._adj.setdefault(v, set())

    def nodes(self) -> List[str]:
        return list(self._adj.keys())

    def edges(self) -> List[Tuple[str, str]]:
        return [(u, v) for u, targets in self._adj.items() for v in targets]

    def neighbors(self, node: str) -> Set[str]:
        return self._adj.get(node, set())


def betweenness_centrality(graph: DiGraph) -> Dict[str, float]:
    """Cálculo simplificado de centralidad de intermediación."""
    centrality: Dict[str, float] = {node: 0.0 for node in graph.nodes()}
    nodes = graph.nodes()
    for s in nodes:
        # BFS para encontrar caminos más cortos aproximados
        queue: deque[str] = deque([s])
        predecessors: Dict[str, List[str]] = {s: []}
        distances: Dict[str, int] = {s: 0}
        while queue:
            v = queue.popleft()
            for neighbor in graph.neighbors(v):
                if neighbor not in distances:
                    queue.append(neighbor)
                    distances[neighbor] = distances[v] + 1
                    predecessors[neighbor] = [v]
                elif distances[neighbor] == distances[v] + 1:
                    predecessors[neighbor].append(v)
        dependency: Dict[str, float] = {node: 0.0 for node in nodes}
        stack = sorted(distances, key=distances.get, reverse=True)
        for w in stack:
            for v in predecessors.get(w, []):
                if w != s:
                    dependency[v] += (1 + dependency[w]) / len(predecessors[w])
            if w != s:
                centrality[w] += dependency[w]
    return centrality


def strongly_connected_components(graph: DiGraph) -> List[Set[str]]:
    index = 0
    indices: Dict[str, int] = {}
    lowlink: Dict[str, int] = {}
    stack: List[str] = []
    on_stack: Set[str] = set()
    components: List[Set[str]] = []

    def strongconnect(node: str) -> None:
        nonlocal index
        indices[node] = index
        lowlink[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for neighbor in graph.neighbors(node):
            if neighbor not in indices:
                strongconnect(neighbor)
                lowlink[node] = min(lowlink[node], lowlink[neighbor])
            elif neighbor in on_stack:
                lowlink[node] = min(lowlink[node], indices[neighbor])

        if lowlink[node] == indices[node]:
            component: Set[str] = set()
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.add(w)
                if w == node:
                    break
            components.append(component)

    for vertex in graph.nodes():
        if vertex not in indices:
            strongconnect(vertex)

    return components


__all__ = ["DiGraph", "betweenness_centrality", "strongly_connected_components"]
