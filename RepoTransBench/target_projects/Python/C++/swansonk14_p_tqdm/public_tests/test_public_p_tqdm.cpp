#include <gtest/gtest.h>
#include <vector>
#include <functional>
#include <algorithm>
#include "../../include/p_tqdm_api.h"

// Simulate combine_values: a + b*3 + c*4, with b=2, c=1 defaults
int combine_values(int a, int b = 2, int c = 1) {
    return a + b*3 + c*4;
}

class Test_p_map_public : public ::testing::Test {
protected:
    std::function<std::vector<int>(
        std::function<int(int,int,int)>, const std::vector<int>&, const std::vector<int>&, const std::vector<int>&
    )> func_3;

    std::function<std::vector<int>(
        std::function<int(int)>, const std::vector<int>&
    )> func_1;

    std::function<std::vector<int>(
        std::function<int(int,int)>, const std::vector<int>&, const std::vector<int>&
    )> func_2;

    bool generator = false;
    bool ordered = true;

    void SetUp() override {
        func_1 = p_map_cpp_1;
        func_2 = p_map_cpp_2;
        func_3 = p_map_cpp_3;
        generator = false;
        ordered = true;
    }
};

TEST_F(Test_p_map_public, test_two_lists_and_one_single) {
    std::vector<int> array_1 = {2, 8, 14};
    std::vector<int> array_2 = {7, 1, 4};
    int single = 5;
    // c=single, b=array_1, a=array_2
    auto comb_fn = [single](int a, int b) { return combine_values(a, b, single); };
    std::vector<int> result = func_2(comb_fn, array_2, array_1);
    if (generator) {} // ignore, always materialized
    std::vector<int> correct = {
        array_2[0] + array_1[0]*3 + single*4,
        array_2[1] + array_1[1]*3 + single*4,
        array_2[2] + array_1[2]*3 + single*4,
    };
    if (ordered) {
        EXPECT_EQ(correct, result);
    }
}

TEST_F(Test_p_map_public, test_one_list_and_two_singles) {
    std::vector<int> array = {20, 25, 28};
    int single_1 = 4, single_2 = 6;
    auto comb_fn = [single_1, single_2](int a) { return combine_values(a, single_1, single_2); };
    std::vector<int> result = func_1(comb_fn, array);
    if (generator) {}
    std::vector<int> correct;
    for (int v : array) correct.push_back(v + single_1*3 + single_2*4);
    if (ordered) {
        EXPECT_EQ(correct, result);
    }
}

TEST_F(Test_p_map_public, test_single_list) {
    std::vector<int> array = {5, 15, 35};
    auto comb_fn = combine_values;
    std::vector<int> result = func_1(comb_fn, array);
    if (generator) {}
    std::vector<int> correct;
    for (int v : array) correct.push_back(v + 2*3 + 1*4);
    if (ordered) {
        EXPECT_EQ(correct, result);
    }
}

TEST_F(Test_p_map_public, test_multiple_lists) {
    std::vector<int> array1 = {5,9,13};
    std::vector<int> array2 = {2,4,6};
    std::vector<int> array3 = {3,5,7};
    // a,b,c
    auto comb_fn = [](int a, int b, int c) { return combine_values(a,b,c); };
    std::vector<int> result = func_3(comb_fn, array1, array2, array3);
    if (generator) {}
    std::vector<int> correct;
    for (size_t i=0; i<array1.size(); ++i) {
        correct.push_back(array1[i]+array2[i]*3+array3[i]*4);
    }
    if (ordered) {
        EXPECT_EQ(correct, result);
    }
}

TEST_F(Test_p_map_public, test_different_func) {
    auto cube_sum = [](int a, int b) { return (a+b)*(a+b)*(a+b); };
    std::vector<int> list1 = {1,3,5};
    std::vector<int> list2 = {2,4,6};
    std::vector<int> result = func_2(cube_sum, list1, list2);
    if (generator) {}
    std::vector<int> expected = {(1+2)*(1+2)*(1+2), (3+4)*(3+4)*(3+4), (5+6)*(5+6)*(5+6)};
    EXPECT_EQ(expected, result);
}

class Test_p_imap_public : public Test_p_map_public {
    void SetUp() override {
        func_1 = p_imap_cpp_1;
        func_2 = p_imap_cpp_2;
        func_3 = p_imap_cpp_3;
        generator = true;
    }
};