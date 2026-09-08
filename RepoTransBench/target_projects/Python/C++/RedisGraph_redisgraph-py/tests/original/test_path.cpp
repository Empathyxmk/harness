#include <gtest/gtest.h>
#include "path.h"
#include "node.h"
#include "edge.h"

using namespace redisgraph;

class TestPath : public ::testing::Test {
protected:
    void SetUp() override {}
    void TearDown() override {}
};

TEST_F(TestPath, Init) {
    EXPECT_THROW({ Path(nullptr, nullptr); }, std::invalid_argument);

    EXPECT_THROW({ Path(new std::vector<Node*>(), nullptr); }, std::invalid_argument);

    EXPECT_THROW({ Path(nullptr, new std::vector<Edge*>()); }, std::invalid_argument);

    Path* p = new Path(new std::vector<Node*>(), new std::vector<Edge*>());
    EXPECT_TRUE(p != nullptr);
    delete p;
}

TEST_F(TestPath, NewEmptyPath) {
    Path* new_empty_path = Path::new_empty_path();
    EXPECT_TRUE(new_empty_path != nullptr);
    EXPECT_EQ(new_empty_path->_nodes.size(), 0);
    EXPECT_EQ(new_empty_path->_edges.size(), 0);
    delete new_empty_path;
}

TEST_F(TestPath, WrongFlows) {
    Node* node_1 = new Node(1);
    Node* node_2 = new Node(2);
    Node* node_3 = new Node(3);

    Edge* edge_1 = new Edge(node_1, nullptr, node_2);
    Edge* edge_2 = new Edge(node_1, nullptr, node_3);

    Path* p = Path::new_empty_path();
    EXPECT_THROW({ p->add_edge(edge_1); }, std::runtime_error);

    p->add_node(node_1);
    EXPECT_THROW({ p->add_node(node_2); }, std::runtime_error);

    p->add_edge(edge_1);
    EXPECT_THROW({ p->add_edge(edge_2); }, std::runtime_error);

    delete node_1;
    delete node_2;
    delete node_3;
    delete edge_1;
    delete edge_2;
    delete p;
}

TEST_F(TestPath, NodesAndEdges) {
    Node* node_1 = new Node(1);
    Node* node_2 = new Node(2);
    Edge* edge_1 = new Edge(node_1, nullptr, node_2);

    Path* p = Path::new_empty_path();
    EXPECT_EQ(p->nodes().size(), 0);
    p->add_node(node_1);
    EXPECT_EQ(p->edges().size(), 0);
    EXPECT_EQ(p->edge_count(), 0);
    std::vector<Node*> n = {node_1};
    EXPECT_EQ(p->nodes(), n);
    EXPECT_EQ(p->get_node(0), node_1);
    EXPECT_EQ(p->first_node(), node_1);
    EXPECT_EQ(p->last_node(), node_1);
    EXPECT_EQ(p->nodes_count(), 1);
    p->add_edge(edge_1);
    std::vector<Edge*> e = {edge_1};
    EXPECT_EQ(p->edges(), e);
    EXPECT_EQ(p->edge_count(), 1);
    EXPECT_EQ(p->get_relationship(0), edge_1);
    p->add_node(node_2);
    std::vector<Node*> n2 = {node_1, node_2};
    EXPECT_EQ(p->nodes(), n2);
    EXPECT_EQ(p->first_node(), node_1);
    EXPECT_EQ(p->last_node(), node_2);
    EXPECT_EQ(p->nodes_count(), 2);

    delete node_1;
    delete node_2;
    delete edge_1;
    delete p;
}

TEST_F(TestPath, Compare) {
    Node* node_1 = new Node(1);
    Node* node_2 = new Node(2);
    Edge* edge_1 = new Edge(node_1, nullptr, node_2);

    Path* p1 = Path::new_empty_path();
    Path* p2 = Path::new_empty_path();
    EXPECT_EQ(*p1, *p2);
    delete p1; delete p2;

    std::vector<Node*> nodes_vec{node_1, node_2};
    std::vector<Edge*> edges_vec{edge_1};
    Path* p3 = new Path(nodes_vec, edges_vec);
    Path* p4 = new Path(nodes_vec, edges_vec);
    EXPECT_EQ(*p3, *p4);
    delete p3; delete p4;

    Path* p5 = new Path(std::vector<Node*>{node_1}, std::vector<Edge*>{});
    Path* p6 = new Path(std::vector<Node*>{}, std::vector<Edge*>{});
    EXPECT_NE(*p5, *p6);
    delete p5; delete p6;

    Path* p7 = new Path(std::vector<Node*>{node_1}, std::vector<Edge*>{});
    Path* p8 = new Path(std::vector<Node*>{node_2}, std::vector<Edge*>{});
    EXPECT_NE(*p7, *p8);
    delete p7; delete p8;

    Path* p9 = new Path(std::vector<Node*>{node_1}, std::vector<Edge*>{edge_1});
    Path* p10 = new Path(std::vector<Node*>{node_1}, std::vector<Edge*>{});
    EXPECT_NE(*p9, *p10);
    delete p9; delete p10;

    Path* p11 = new Path(std::vector<Node*>{node_1}, std::vector<Edge*>{edge_1});
    Path* p12 = new Path(std::vector<Node*>{node_2}, std::vector<Edge*>{edge_1});
    EXPECT_NE(*p11, *p12);
    delete p11; delete p12;

    delete node_1;
    delete node_2;
    delete edge_1;
}