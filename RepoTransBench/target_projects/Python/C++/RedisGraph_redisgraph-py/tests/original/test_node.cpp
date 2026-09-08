#include <gtest/gtest.h>
#include "node.h"
#include <string>
#include <vector>
#include <map>
#include <initializer_list>

using namespace redisgraph;

class TestNode : public ::testing::Test {
protected:
    Node* no_args;
    Node* no_props;
    Node* props_only;
    Node* no_label;
    Node* multi_label;

    void SetUp() override {
        no_args = new Node();
        no_props = new Node(1, "alias", {"l"});
        props_only = new Node(-1, "", {}, 
                              std::map<std::string, Value>{{"a", "a"}, {"b", 10}});
        no_label = new Node(1, "alias", {},
                            std::map<std::string, Value>{{"a", "a"}});
        multi_label = new Node(1, "alias", {"l", "ll"});
    }
    void TearDown() override {
        delete no_args;
        delete no_props;
        delete props_only;
        delete no_label;
        delete multi_label;
    }
};

TEST_F(TestNode, ToString) {
    EXPECT_EQ(no_args->toString(), "");
    EXPECT_EQ(no_props->toString(), "");
    EXPECT_EQ(multi_label->toString(), "");
    EXPECT_EQ(props_only->toString(), "{a:\"a\",b:10}");
    EXPECT_EQ(no_label->toString(), "{a:\"a\"}");
}

TEST_F(TestNode, Stringify) {
    EXPECT_EQ(no_args->str(), "()");
    EXPECT_EQ(no_props->str(), "(alias:l)");
    EXPECT_EQ(props_only->str(), "({a:\"a\",b:10})");
    EXPECT_EQ(no_label->str(), "(alias{a:\"a\"})");
    EXPECT_EQ(multi_label->str(), "(alias:l:ll)");
}

TEST_F(TestNode, Comparision) {
    EXPECT_EQ(Node(), Node());
    EXPECT_EQ(Node(1), Node(1));
    EXPECT_NE(Node(1), Node(2));
    EXPECT_EQ(Node(1, "a"), Node(1, "b"));
    EXPECT_EQ(Node(1, "a"), Node(1, "a"));
    EXPECT_EQ(Node(1, "", {"a"}), Node(1, "", {"a"}));
    EXPECT_NE(Node(1, "", {"a"}), Node(1, "", {"b"}));
    EXPECT_EQ(Node(1, "a", {"l"}), Node(1, "a", {"l"}));
    EXPECT_NE(Node("a", {"l"}), Node("a", {"l1"}));
    EXPECT_EQ(Node("a", {"a", "b"}), Node("a", {"a", "b"}));
    EXPECT_NE(Node("a", {"a", "b"}), Node("a", {"a", "c"}));
    EXPECT_EQ(Node(-1, "", {}, {{"a", 10}}), Node(-1, "", {}, {{"a", 10}}));
    EXPECT_NE(Node(), Node(-1, "", {}, {{"a", 10}}));
}