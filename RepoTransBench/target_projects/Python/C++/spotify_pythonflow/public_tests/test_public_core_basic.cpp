#include <gtest/gtest.h>
#include "pythonflow/core.h"

class DummyOp : public pythonflow::Operation {
public:
    DummyOp(const std::string &name, pythonflow::Graph* graph) : Operation(name, graph) {}
    int evaluate() override { return 100; }
};

TEST(PublicCoreBasic, GraphEnterExit) {
    pythonflow::Graph g;
    ASSERT_EQ(g.getDefaultGraph(), nullptr);
    {
        pythonflow::Graph::GlobalGraphSetter setter(&g);
        ASSERT_EQ(pythonflow::Graph::getDefaultGraph(), &g);
    }
    ASSERT_EQ(g.getDefaultGraph(), nullptr);
}

// ... (Repeat all public tests as above but with _Public suffix and test tweaks)