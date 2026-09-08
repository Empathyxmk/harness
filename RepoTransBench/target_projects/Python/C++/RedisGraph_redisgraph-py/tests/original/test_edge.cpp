#include <gtest/gtest.h>
#include "edge.h"
#include "node.h"
#include <string>
#include <map>
#include <vector>

using namespace redisgraph;

class TestEdge : public ::testing::Test {
protected:
    void SetUp() override {}
    void TearDown() override {}
};

TEST_F(TestEdge, Init) {
    EXPECT_THROW({ Edge(nullptr, nullptr, nullptr); }, std::invalid_argument);

    EXPECT_THROW({ Edge(new Node(), nullptr, nullptr); }, std::invalid_argument);

    EXPECT_THROW({ Edge(nullptr, nullptr, new Node()); }, std::invalid_argument);

    Edge* valid = new Edge(new Node(1), nullptr, new Node(2));
    EXPECT_TRUE(valid != nullptr);
    delete valid;
}

TEST_F(TestEdge, ToString) {
    std::map<std::string, Value> props = {{"a", "a"}, {"b", 10}};
    Edge e1(new Node(), nullptr, new Node(), props);
    EXPECT_EQ(e1.toString(), "{a:\"a\",b:10}");
    Edge e2(new Node(), nullptr, new Node(), std::map<std::string, Value>());
    EXPECT_EQ(e2.toString(), "");
}

TEST_F(TestEdge, Stringify) {
    Node john("a", {"person"}, {{"name", "John Doe"}, {"age", 33}, {"someArray", std::vector<Value>{1,2,3}}});
    Node japan("b", {"country"}, {{"name", "Japan"}});
    Edge edge_with_relation(&john, "visited", &japan, {{"purpose", "pleasure"}});
    EXPECT_EQ(str(john) + "-[:visited{purpose:\"pleasure\"}]->" + str(japan),
              str(edge_with_relation));
    Edge edge_no_relation_no_props(&japan, "", &john);
    EXPECT_EQ(str(japan) + "-[]->" + str(john), str(edge_no_relation_no_props));
    Edge edge_only_props(&john, "", &japan, {{"a", "b"}, {"c", 3}});
    EXPECT_EQ(str(john) + "-[{a:\"b\",c:3}]->" + str(japan), str(edge_only_props));
}

TEST_F(TestEdge, Comparision) {
    Node* node1 = new Node(1);
    Node* node2 = new Node(2);
    Node* node3 = new Node(3);
    Edge edge1(node1, nullptr, node2);

    EXPECT_EQ(edge1, Edge(node1, nullptr, node2));
    EXPECT_NE(edge1, Edge(node1, "bla", node2));
    EXPECT_NE(edge1, Edge(node1, nullptr, node3));
    EXPECT_NE(edge1, Edge(node3, nullptr, node2));
    EXPECT_NE(edge1, Edge(node2, nullptr, node1));
    EXPECT_NE(edge1, Edge(node1, nullptr, node2, {{"a", 10}}));

    delete node1;
    delete node2;
    delete node3;
}