#include "SetGraph.h"
#include <cassert>

SetGraph::SetGraph(int verticesCount)
    : adjacencySets(verticesCount), reverseAdjacencySets(verticesCount) {}

SetGraph::SetGraph(const IGraph &other)
    : adjacencySets(other.VerticesCount()),
      reverseAdjacencySets(other.VerticesCount()) {
  for (int i = 0; i < other.VerticesCount(); ++i) {
    std::vector<int> nextVertices = other.GetNextVertices(i);
    for (int vertex : nextVertices) {
      AddEdge(i, vertex);
    }
  }
}

void SetGraph::validateVertex(int vertex) const {
  assert(vertex >= 0 && vertex < VerticesCount());
}

void SetGraph::AddEdge(int from, int to) {
  validateVertex(from);
  validateVertex(to);
  adjacencySets[from].insert(to);
  reverseAdjacencySets[to].insert(from);
}

int SetGraph::VerticesCount() const { return adjacencySets.size(); }

std::vector<int> SetGraph::GetNextVertices(int vertex) const {
  validateVertex(vertex);
  return std::vector<int>(adjacencySets[vertex].begin(),
                          adjacencySets[vertex].end());
}

std::vector<int> SetGraph::GetPrevVertices(int vertex) const {
  validateVertex(vertex);
  return std::vector<int>(reverseAdjacencySets[vertex].begin(),
                          reverseAdjacencySets[vertex].end());
}
