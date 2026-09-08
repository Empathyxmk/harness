#include <gtest/gtest.h>
#include "pythonflow/core.h"

class DummyOp : public pythonflow::Operation {
public:
    DummyOp(const std::string &name, pythonflow::Graph* graph) : Operation(name, graph) {}
    int evaluate() override { return 42; }
};

TEST(GraphCoreBasic, EnterExit) {
    pythonflow::Graph g;
    ASSERT_EQ(g.getDefaultGraph(), nullptr);
    {
        pythonflow::Graph::GlobalGraphSetter setter(&g);
        ASSERT_EQ(pythonflow::Graph::getDefaultGraph(), &g);
    }
    ASSERT_EQ(g.getDefaultGraph(), nullptr);
}

TEST(GraphCoreBasic, DuplicateEnter) {
    pythonflow::Graph g;
    pythonflow::Graph::GlobalGraphSetter setter1(&g);
    EXPECT_THROW({
        pythonflow::Graph::GlobalGraphSetter setter2(&g);
    }, std::logic_error /* Replace with real exception type for duplicate enter */);
}

TEST(GraphCoreBasic, NormalizeOperationWithInstance) {
    pythonflow::Graph g;
    auto op = std::make_shared<DummyOp>("abc", &g);
    g.operations["abc"] = op;
    ASSERT_EQ(g.normalizeOperation(op), op);
    pythonflow::Graph other;
    auto op2 = std::make_shared<DummyOp>("def", &other);
    EXPECT_THROW(g.normalizeOperation(op2), std::runtime_error);
}

TEST(GraphCoreBasic, NormalizeOperationWithName) {
    pythonflow::Graph g;
    auto op = std::make_shared<DummyOp>("abc", &g);
    g.operations["abc"] = op;
    ASSERT_EQ(g.normalizeOperation("abc"), op);
}

TEST(GraphCoreBasic, NormalizeOperationInvalid) {
    pythonflow::Graph g;
    EXPECT_THROW(g.normalizeOperation(123), std::invalid_argument);
    EXPECT_THROW(g.normalizeOperation("notfound"), std::out_of_range);
}

TEST(GraphCoreBasic, NormalizeContextAndDuplicates) {
    pythonflow::Graph g;
    auto op = std::make_shared<DummyOp>("x", &g);
    g.operations["x"] = op;
    std::map<std::string, int> ctx { {"x", 3} };
    auto norm = g.normalizeContext(ctx);
    ASSERT_TRUE(norm.count(op));
    // context not a mapping
    EXPECT_THROW(g.normalizeContextVec({{"x", 3}}), std::invalid_argument);
    // duplicate keys
    std::map<pythonflow::OperationPtr, int> ctx_dup;
    ctx_dup[op] = 1;
    // context with op + string key "x"
    EXPECT_THROW(g.normalizeContextMixed(ctx_dup, {{"x", 2}}), std::invalid_argument);
}

TEST(GraphCoreBasic, NormalizeContextKwargs) {
    pythonflow::Graph g;
    auto op = std::make_shared<DummyOp>("x", &g);
    g.operations["x"] = op;
    auto norm = g.normalizeContextWithKwargs({}, {{"x", 99}});
    ASSERT_TRUE(norm.count(op) && norm[op] == 99);
}