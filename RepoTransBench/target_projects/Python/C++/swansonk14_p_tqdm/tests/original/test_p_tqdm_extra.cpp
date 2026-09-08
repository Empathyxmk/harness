#include <gtest/gtest.h>
#include <vector>
#include <stdexcept>
#include <string>
#include "../../include/p_tqdm_api.h"
using namespace std;

TEST(TestVersion, VersionHasAttribute) {
    // Simulate version struct -- in production, replace with your _version logic
    VersionInfo version = p_tqdm_version();
    EXPECT_FALSE(version.version_str.empty()); // Has "__version__"
}

TEST(TestSequentialInternal, test_sequential) {
    auto f = [](int x) { return x + 1; };
    vector<int> in = {1,2,3};
    vector<int> out = sequential_cpp_1(f, in);
    vector<int> correct = {2,3,4};
    EXPECT_EQ(out, correct);
}

TEST(TestSequentialInternal, test_sequential_multiple) {
    auto f = [](int a, int b) { return a + b; };
    vector<int> in1 = {1,2};
    vector<int> in2 = {2,3};
    vector<int> out = sequential_cpp_2(f, in1, in2);
    vector<int> correct = {3,5};
    EXPECT_EQ(out, correct);
}

TEST(TestSequentialInternal, test_sequential_length) {
    auto f = [](int x, int y) { return x + y; };
    vector<int> in1 = {1,2};
    vector<int> in2 = {5,10};
    vector<int> out = sequential_cpp_2(f, in1, in2);
    vector<int> correct = {6, 12};
    EXPECT_EQ(out, correct);
}

TEST(TestSequentialInternal, test_sequential_with_empty) {
    auto f = [](int x) { return x; };
    vector<int> empty;
    vector<int> out = sequential_cpp_1(f, empty);
    EXPECT_TRUE(out.empty());
}

TEST(TestSequentialInternal, test_sequential_with_exception) {
    auto f = [](int x) -> int {
        if (x == 2) throw std::runtime_error("bad");
        return x+1;
    };
    vector<int> in = {1,2,3};
    EXPECT_THROW({
        sequential_cpp_1(f, in);
    }, std::runtime_error);
}