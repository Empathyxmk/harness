#include <gtest/gtest.h>
#include <map>
#include <vector>
#include <tuple>
#include <algorithm>
#include <string>

// --- Placeholders: replace with real includes if translating full implementation
class Node {
public:
    int id;
    std::map<std::string, int> weights;
    Node(int id_): id(id_) {}
};

class Edge {
public:
    Node parent, child;
    std::map<std::string, int> weights;
    Edge(Node parent_, Node child_, int weight_) : parent(parent_), child(child_) {
        weights["weight"] = weight_;
    }
};

class CallGraph {
public:
    std::vector<Node> nodes;
    std::vector<Edge> edges;
    CallGraph() { }
    void add_stack(std::vector<Node> stack, std::map<std::string, int> weights) {
        for (const auto& n : stack) {
            auto it = std::find_if(nodes.begin(), nodes.end(), [&](const Node& x){return x.id == n.id;});
            if (it == nodes.end())
                nodes.push_back(n);
        }
        if (stack.size() >= 2) {
            for (size_t i = 0; i + 1 < stack.size(); ++i) {
                edges.emplace_back(stack[i], stack[i+1], weights["weight"]);
            }
        }
    }
    std::vector<Edge> get_top_edges(const std::string& key, size_t n) {
        std::vector<Edge> out = edges;
        std::sort(out.begin(), out.end(), [&](const Edge& a, const Edge& b){ return a.weights.at(key) > b.weights.at(key); });
        if (n < out.size()) out.resize(n);
        return out;
    }
    std::vector<Node> get_top_nodes(const std::string& key, size_t n) {
        std::vector<Node> out = nodes;
        std::sort(out.begin(), out.end(), [&](const Node& a, const Node& b){ return a.weights.count(key) && b.weights.count(key) ? a.weights.at(key) > b.weights.at(key) : false; });
        if (n < out.size()) out.resize(n);
        return out;
    }
};

class PublicSimpleCallgraphTest : public ::testing::Test {
protected:
    CallGraph graph;
    void SetUp() override {
        // Different node IDs/structure from original test
        graph.add_stack({Node(10), Node(20)}, {{"weight", 2}});
        graph.add_stack({Node(10), Node(30)}, {{"weight", 8}});
        graph.add_stack({Node(10), Node(20), Node(30)}, {{"weight", 4}});
        graph.add_stack({Node(18), Node(10), Node(40)}, {{"weight", 6}});

        for (auto& n : graph.nodes) {
            switch (n.id) {
                case 30: n.weights["weight"] = 12; break;
                case 20: n.weights["weight"] = 2; break;
                case 10: n.weights["weight"] = 0; break;
                default: n.weights["weight"] = 0; break;
            }
        }
    }
};

TEST_F(PublicSimpleCallgraphTest, BasicAttrs) {
    EXPECT_EQ(graph.nodes.size(), 4u);
    EXPECT_EQ(graph.edges.size(), 5u);
}

TEST_F(PublicSimpleCallgraphTest, TopEdges) {
    auto top_edges = graph.get_top_edges("weight", 2);
    std::vector<std::tuple<int, int, int>> summary;
    for (const auto& e : top_edges) {
        summary.push_back({e.parent.id, e.child.id, e.weights.at("weight")});
    }
    std::vector<std::tuple<int, int, int>> expected = {
        {10, 30, 12}, {10, 20, 6}
    };
    EXPECT_EQ(summary, expected);
}

TEST_F(PublicSimpleCallgraphTest, TopNodes) {
    auto top_nodes = graph.get_top_nodes("weight", 3);
    std::vector<std::pair<int, int>> summary;
    for (const auto& n : top_nodes) {
        summary.push_back({n.id, n.weights["weight"]});
    }
    std::vector<std::pair<int, int>> expected = {{30, 12}, {10, 0}, {20, 2}};
    EXPECT_EQ(summary, expected);
}