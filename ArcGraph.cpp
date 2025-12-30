#include "ArcGraph.h"
#include <algorithm>
#include <cassert>

ArcGraph::ArcGraph(int verticesCount) : edges(), verticesCount(verticesCount) {}

ArcGraph::ArcGraph(const IGraph &other)
    : edges(), verticesCount(other.VerticesCount()) {
  for (int i = 0; i < other.VerticesCount(); ++i) {
    std::vector<int> nextVertices = other.GetNextVertices(i);
    for (int vertex : nextVertices) {
      AddEdge(i, vertex);
    }
  }
}

void ArcGraph::validateVertex(int vertex) const {
  assert(vertex >= 0 && vertex < verticesCount);
}

void ArcGraph::AddEdge(int from, int to) {
  validateVertex(from);
  validateVertex(to);

  auto it = std::find(edges.begin(), edges.end(), std::make_pair(from, to));
  if (it == edges.end()) {
    edges.emplace_back(from, to);
  }
}

int ArcGraph::VerticesCount() const { return verticesCount; }

std::vector<int> ArcGraph::GetNextVertices(int vertex) const {
  validateVertex(vertex);

  std::vector<int> result;
  for (const auto &edge : edges) {
    if (edge.first == vertex) {
      result.push_back(edge.second);
    }
  }
  return result;
}

std::vector<int> ArcGraph::GetPrevVertices(int vertex) const {
  validateVertex(vertex);

  std::vector<int> result;
  for (const auto &edge : edges) {
    if (edge.second == vertex) {
      result.push_back(edge.first);
    }
  }
  return result;
}
