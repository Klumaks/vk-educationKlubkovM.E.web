#include "ArcGraph.h"
#include "ListGraph.h"
#include "MatrixGraph.h"
#include "SetGraph.h"
#include <cassert>
#include <iostream>
#include <algorithm>

bool areGraphsEqual(const IGraph &graph1, const IGraph &graph2) {
  if (graph1.VerticesCount() != graph2.VerticesCount()) {
    return false;
  }

  for (int i = 0; i < graph1.VerticesCount(); ++i) {
    std::vector<int> next1 = graph1.GetNextVertices(i);
    std::vector<int> next2 = graph2.GetNextVertices(i);

    std::sort(next1.begin(), next1.end());
    std::sort(next2.begin(), next2.end());

    if (next1 != next2) {
      return false;
    }
  }

  return true;
}

void testGraphImplementations() {
  std::cout << "Testing graph implementations..." << std::endl;

  ListGraph listGraph(5);
  listGraph.AddEdge(0, 1);
  listGraph.AddEdge(0, 2);
  listGraph.AddEdge(1, 2);
  listGraph.AddEdge(2, 3);
  listGraph.AddEdge(3, 4);
  listGraph.AddEdge(4, 0);

  MatrixGraph matrixFromList(listGraph);
  SetGraph setFromList(listGraph);
  ArcGraph arcFromList(listGraph);

  assert(areGraphsEqual(listGraph, matrixFromList));
  assert(areGraphsEqual(listGraph, setFromList));
  assert(areGraphsEqual(listGraph, arcFromList));

  std::vector<int> nextFrom0 = listGraph.GetNextVertices(0);
  assert(nextFrom0.size() == 2);
  assert(std::find(nextFrom0.begin(), nextFrom0.end(), 1) != nextFrom0.end());
  assert(std::find(nextFrom0.begin(), nextFrom0.end(), 2) != nextFrom0.end());

  std::vector<int> prevTo2 = listGraph.GetPrevVertices(2);
  assert(prevTo2.size() == 2);
  assert(std::find(prevTo2.begin(), prevTo2.end(), 0) != prevTo2.end());
  assert(std::find(prevTo2.begin(), prevTo2.end(), 1) != prevTo2.end());

  listGraph.AddEdge(0, 1);
  assert(listGraph.GetNextVertices(0).size() == 2);

  std::cout << "All tests passed!" << std::endl;
}

int main() {
  testGraphImplementations();

  std::cout << "\nExample usage:" << std::endl;

  ListGraph graph(4);
  graph.AddEdge(0, 1);
  graph.AddEdge(0, 2);
  graph.AddEdge(1, 2);
  graph.AddEdge(2, 3);
  graph.AddEdge(3, 0);

  std::cout << "Graph has " << graph.VerticesCount() << " vertices"
            << std::endl;

  for (int i = 0; i < graph.VerticesCount(); ++i) {
    std::vector<int> next = graph.GetNextVertices(i);
    std::vector<int> prev = graph.GetPrevVertices(i);

    std::cout << "Vertex " << i << ": ";
    std::cout << "outgoing - {";
    for (size_t j = 0; j < next.size(); ++j) {
      std::cout << next[j];
      if (j < next.size() - 1)
        std::cout << ", ";
    }
    std::cout << "}, incoming - {";
    for (size_t j = 0; j < prev.size(); ++j) {
      std::cout << prev[j];
      if (j < prev.size() - 1)
        std::cout << ", ";
    }
    std::cout << "}" << std::endl;
  }

  return 0;
}
