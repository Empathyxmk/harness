#include <gtest/gtest.h>
#include "pythonflow/core.h"
#include "pythonflow/operations.h"
#include "pythonflow/util.h"
#include <random>
#include <complex>
#include <thread>
#include <fstream>

TEST(PythonFlow, ConsistentContext) {
    pythonflow::Graph graph;
    auto uniform = pythonflow::func_op("uniform", 0, 1);   // Replace with proper function
    auto scaled = uniform * 4;
    auto results = graph.evaluate({uniform, scaled});
    ASSERT_EQ(results[1], 4 * results[0]);
}

TEST(PythonFlow, Context) {
    pythonflow::Graph graph;
    auto a = pythonflow::placeholder<int>("a");
    auto b = pythonflow::placeholder<int>("b");
    auto c = pythonflow::placeholder<int>("c");
    auto x = a * b + c;
    int actual = graph.evaluate(x, {{"a", 4}, {"b", 7}, {"c", 9}});
    ASSERT_EQ(actual, 37);
}

// ... (Repeat for all the tests as in Python: iter, getattr, name change, cache, error paths, etc)