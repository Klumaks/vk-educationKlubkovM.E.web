#ifndef ARCGRAPH_H
#define ARCGRAPH_H

#include "IGraph.h"
#include <vector>

class ArcGraph : public IGraph {
public:
  explicit ArcGraph(int verticesCount);
  explicit ArcGraph(const IGraph &other);
  ArcGraph &operator=(const ArcGraph &other) = default;

  void AddEdge(int from, int to) override;
  int VerticesCount() const override;
  std::vector<int> GetNextVertices(int vertex) const override;
  std::vector<int> GetPrevVertices(int vertex) const override;

private:
  std::vector<std::pair<int, int>> edges;
  int verticesCount;

  void validateVertex(int vertex) const;
};

#endif
