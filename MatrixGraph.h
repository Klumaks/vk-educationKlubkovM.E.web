#ifndef MATRIXGRAPH_H
#define MATRIXGRAPH_H

#include "IGraph.h"
#include <vector>

class MatrixGraph : public IGraph {
public:
  explicit MatrixGraph(int verticesCount);
  explicit MatrixGraph(const IGraph &other);
  MatrixGraph &operator=(const MatrixGraph &other) = default;

  void AddEdge(int from, int to) override;
  int VerticesCount() const override;
  std::vector<int> GetNextVertices(int vertex) const override;
  std::vector<int> GetPrevVertices(int vertex) const override;

private:
  std::vector<std::vector<bool>> adjacencyMatrix;

  void validateVertex(int vertex) const;
};

#endif
