#ifndef LISTGRAPH_H
#define LISTGRAPH_H

#include "IGraph.h"
#include <list>
#include <vector>

class ListGraph : public IGraph {
public:
  explicit ListGraph(int verticesCount);
  explicit ListGraph(const IGraph &other);
  ListGraph &operator=(const ListGraph &other) = default;

  void AddEdge(int from, int to) override;
  int VerticesCount() const override;
  std::vector<int> GetNextVertices(int vertex) const override;
  std::vector<int> GetPrevVertices(int vertex) const override;

private:
  std::vector<std::list<int>> adjacencyLists;
  std::vector<std::list<int>> reverseAdjacencyLists;

  void validateVertex(int vertex) const;
};

#endif
