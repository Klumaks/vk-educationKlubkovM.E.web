#include "MatrixGraph.h"
#include <cassert>

MatrixGraph::MatrixGraph(int verticesCount)
    : adjacencyMatrix(verticesCount, std::vector<bool>(verticesCount, false)) {}

MatrixGraph::MatrixGraph(const IGraph &other)
    : adjacencyMatrix(other.VerticesCount(),
                      std::vector<bool>(other.VerticesCount(), false)) {
  for (int i = 0; i < other.VerticesCount(); ++i) {
    std::vector<int> nextVertices = other.GetNextVertices(i);
    for (int vertex : nextVertices) {
      AddEdge(i, vertex);
    }
  }
}

void MatrixGraph::validateVertex(int vertex) const {
  assert(vertex >= 0 && vertex < VerticesCount());
}

void MatrixGraph::AddEdge(int from, int to) {
  validateVertex(from);
  validateVertex(to);
  adjacencyMatrix[from][to] = true;
}

int MatrixGraph::VerticesCount() const { return adjacencyMatrix.size(); }

std::vector<int> MatrixGraph::GetNextVertices(int vertex) const {
  validateVertex(vertex);

  std::vector<int> result;
  for (int i = 0; i < VerticesCount(); ++i) {
    if (adjacencyMatrix[vertex][i]) {
      result.push_back(i);
    }
  }
  return result;
}

std::vector<int> MatrixGraph::GetPrevVertices(int vertex) const {
  validateVertex(vertex);

  std::vector<int> result;
  for (int i = 0; i < VerticesCount(); ++i) {
    if (adjacencyMatrix[i][vertex]) {
      result.push_back(i);
    }
  }
  return result;
}
