#include <gtest/gtest.h>
#include "pythonflow/core.h"
#include "pythonflow/operations.h"
#include "pythonflow/util.h"

TEST(PublicPythonFlow, ConsistentContext) {
    pythonflow::Graph graph;
    auto uniform = pythonflow::func_op("uniform", 2, 3);   // Replace with proper implementation
    auto scaled = uniform * 7;
    auto results = graph.evaluate({uniform, scaled});
    ASSERT_EQ(results[1], 7 * results[0]);
}

// ... (Repeat each test and exact public logic, names, expectations as per public Python cases)