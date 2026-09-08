#include <gtest/gtest.h>
#include <vector>
#include <stdexcept>
#include <string>
#include "../../include/p_tqdm_api.h"

using namespace std;

TEST(TestVersionPublic, test_version) {
    VersionInfo vinfo = p_tqdm_version();
    EXPECT_FALSE(vinfo.version_str.empty());
    EXPECT_TRUE(vinfo.version_str.find('.') != std::string::npos);
}

TEST(TestSequentialInternalPublic, test_sequential) {
    auto f = [](int x) { return x * 3; };
    vector<int> in = {2, 4, 6};
    vector<int> out = sequential_cpp_1(f, in);
    vector<int> correct = {6, 12, 18};
    EXPECT_EQ(out, correct);
}

TEST(TestSequentialInternalPublic, test_sequential_multiple) {
    auto f = [](int a, int b) { return a * b; };
    vector<int> in1 = {3,4};
    vector<int> in2 = {5,6};
    vector<int> out = sequential_cpp_2(f, in1, in2);
    vector<int> correct = {15, 24};
    EXPECT_EQ(out, correct);
}

TEST(TestSequentialInternalPublic, test_sequential_length) {
    auto f = [](int x, int y) { return x * y * 2; };
    vector<int> in1 = {2,3};
    vector<int> in2 = {7,11};
    vector<int> out = sequential_cpp_2(f, in1, in2);
    vector<int> correct = {28, 66};
    EXPECT_EQ(out, correct);
}

TEST(TestSequentialInternalPublic, test_sequential_with_empty) {
    auto f = [](int x) { return x * 10; };
    vector<int> empty;
    vector<int> out = sequential_cpp_1(f, empty);
    EXPECT_TRUE(out.empty());
}

TEST(TestSequentialInternalPublic, test_sequential_with_exception) {
    auto f = [](int x) -> int {
        if (x == 5) throw std::runtime_error("terrible");
        return x * 2;
    };
    vector<int> in = {3,5,7};
    EXPECT_THROW({
        sequential_cpp_1(f, in);
    }, std::runtime_error);
}