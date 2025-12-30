#ifndef SETGRAPH_H
#define SETGRAPH_H

#include "IGraph.h"
#include <unordered_set>
#include <vector>

class SetGraph : public IGraph {
public:
  explicit SetGraph(int verticesCount);
  explicit SetGraph(const IGraph &other);
  SetGraph &operator=(const SetGraph &other) = default;

  void AddEdge(int from, int to) override;
  int VerticesCount() const override;
  std::vector<int> GetNextVertices(int vertex) const override;
  std::vector<int> GetPrevVertices(int vertex) const override;

private:
  std::vector<std::unordered_set<int>> adjacencySets;
  std::vector<std::unordered_set<int>> reverseAdjacencySets;

  void validateVertex(int vertex) const;
};

#endif
