#include "ListGraph.h"
#include <algorithm>
#include <cassert>

ListGraph::ListGraph(int verticesCount)
    : adjacencyLists(verticesCount), reverseAdjacencyLists(verticesCount) {}

ListGraph::ListGraph(const IGraph &other)
    : adjacencyLists(other.VerticesCount()),
      reverseAdjacencyLists(other.VerticesCount()) {
  for (int i = 0; i < other.VerticesCount(); ++i) {
    std::vector<int> nextVertices = other.GetNextVertices(i);
    for (int vertex : nextVertices) {
      AddEdge(i, vertex);
    }
  }
}

void ListGraph::validateVertex(int vertex) const {
  assert(vertex >= 0 && vertex < VerticesCount());
}

void ListGraph::AddEdge(int from, int to) {
  validateVertex(from);
  validateVertex(to);

  auto it =
      std::find(adjacencyLists[from].begin(), adjacencyLists[from].end(), to);
  if (it == adjacencyLists[from].end()) {
    adjacencyLists[from].push_back(to);
    reverseAdjacencyLists[to].push_back(from);
  }
}

int ListGraph::VerticesCount() const { return adjacencyLists.size(); }

std::vector<int> ListGraph::GetNextVertices(int vertex) const {
  validateVertex(vertex);
  return std::vector<int>(adjacencyLists[vertex].begin(),
                          adjacencyLists[vertex].end());
}

std::vector<int> ListGraph::GetPrevVertices(int vertex) const {
  validateVertex(vertex);
  return std::vector<int>(reverseAdjacencyLists[vertex].begin(),
                          reverseAdjacencyLists[vertex].end());
}
