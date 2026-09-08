#include <gtest/gtest.h>
#include <vector>
#include <algorithm>
#include <functional>

// Dummy map/parallel function declarations for demonstration (replace with production ones)
#include "../../include/p_tqdm_api.h"

using std::vector;

int add_1(int a) { return a + 1; }
int add_2(int a, int b) { return a + b; }
int add_3(int a, int b, int c = 0) { return a + 2 * b + 3 * c; }

class BaseMapTest : public ::testing::Test {
protected:
    // Function pointer or std::function for map function
    std::function<std::vector<int>(
        std::function<int(int)>, const std::vector<int>&
    )> map_func_1;

    std::function<std::vector<int>(
        std::function<int(int,int)>, const std::vector<int>&, const std::vector<int>&
    )> map_func_2;

    std::function<std::vector<int>(
        std::function<int(int,int,int)>, const std::vector<int>&, const std::vector<int>&, const std::vector<int>&
    )> map_func_3;

    bool is_generator = false;
    bool is_ordered = true;
};

TEST_F(BaseMapTest, test_one_list) {
    if (!map_func_1) GTEST_SKIP();

    std::vector<int> array = {1, 2, 3};
    std::vector<int> result = map_func_1(add_1, array);

    std::vector<int> correct_array = {2, 3, 4};
    if (is_ordered) {
        EXPECT_EQ(correct_array, result);
    } else {
        std::sort(correct_array.begin(), correct_array.end());
        std::sort(result.begin(), result.end());
        EXPECT_EQ(correct_array, result);
    }
}

TEST_F(BaseMapTest, test_two_lists) {
    if (!map_func_2) GTEST_SKIP();

    std::vector<int> array_1 = {1, 2, 3};
    std::vector<int> array_2 = {10, 11, 12};
    std::vector<int> result = map_func_2(add_2, array_1, array_2);

    std::vector<int> correct_array = {11, 13, 15};
    if (is_ordered) {
        EXPECT_EQ(correct_array, result);
    } else {
        std::sort(correct_array.begin(), correct_array.end());
        std::sort(result.begin(), result.end());
        EXPECT_EQ(correct_array, result);
    }
}

TEST_F(BaseMapTest, test_two_lists_and_one_single) {
    if (!map_func_2) GTEST_SKIP();

    std::vector<int> array_1 = {1, 2, 3};
    std::vector<int> array_2 = {10, 11, 12};
    int single = 5;
    // We'll bind single as the first argument, and the vectors as b, c
    auto bind_add_3 = [single](int b, int c) { return add_3(single, b, c); };
    std::vector<int> result = map_func_2(bind_add_3, array_1, array_2);

    std::vector<int> correct_array = {37, 42, 47};
    if (is_ordered) {
        EXPECT_EQ(correct_array, result);
    } else {
        std::sort(correct_array.begin(), correct_array.end());
        std::sort(result.begin(), result.end());
        EXPECT_EQ(correct_array, result);
    }
}

TEST_F(BaseMapTest, test_one_list_and_two_singles) {
    if (!map_func_1) GTEST_SKIP();

    std::vector<int> array = {1, 2, 3};
    int single_1 = 5;
    int single_2 = -2;
    auto bind_add_3 = [single_1, single_2](int a) { return add_3(single_1, a, single_2); };
    std::vector<int> result = map_func_1(bind_add_3, array);

    std::vector<int> correct_array = {1, 3, 5};
    if (is_ordered) {
        EXPECT_EQ(correct_array, result);
    } else {
        std::sort(correct_array.begin(), correct_array.end());
        std::sort(result.begin(), result.end());
        EXPECT_EQ(correct_array, result);
    }
}

TEST_F(BaseMapTest, test_list_and_generator_and_single_equal_length) {
    if (!map_func_2) GTEST_SKIP();
    // In C++, generators are simulated with ranges
    std::vector<int> array = {1, 2, 3};
    std::vector<int> generator = {0, 1, 2};
    int single = -3;
    auto bind_add_3 = [single](int a, int b) { return add_3(a, b, single); };

    std::vector<int> result = map_func_2(bind_add_3, array, generator);

    std::vector<int> correct_array = {-8, -5, -2};
    if (is_ordered) {
        EXPECT_EQ(correct_array, result);
    } else {
        std::sort(correct_array.begin(), correct_array.end());
        std::sort(result.begin(), result.end());
        EXPECT_EQ(correct_array, result);
    }
}

TEST_F(BaseMapTest, test_list_and_generator_and_single_unequal_length) {
    if (!map_func_2) GTEST_SKIP();
    std::vector<int> array = {1, 2, 3, 4, 5, 6};
    std::vector<int> generator = {0, 1, 2};
    int single = -3;
    auto bind_add_3 = [single](int a, int b) { return add_3(a, b, single); };

    // Only up to shorter of two lists should be taken
    std::vector<int> trimmed_array(array.begin(), array.begin() + generator.size());

    std::vector<int> result = map_func_2(bind_add_3, trimmed_array, generator);

    std::vector<int> correct_array = {-8, -5, -2};
    if (is_ordered) {
        EXPECT_EQ(correct_array, result);
    } else {
        std::sort(correct_array.begin(), correct_array.end());
        std::sort(result.begin(), result.end());
        EXPECT_EQ(correct_array, result);
    }
}

// Each specific map class supplies map_func_1/map_func_2 and the right configs

class Test_p_map : public BaseMapTest {
    void SetUp() override {
        map_func_1 = p_map_cpp_1;
        map_func_2 = p_map_cpp_2;
        is_generator = false;
        is_ordered = true;
    }
};

class Test_p_imap : public BaseMapTest {
    void SetUp() override {
        map_func_1 = p_imap_cpp_1;
        map_func_2 = p_imap_cpp_2;
        is_generator = true;
        is_ordered = true;
    }
};

class Test_p_umap : public BaseMapTest {
    void SetUp() override {
        map_func_1 = p_umap_cpp_1;
        map_func_2 = p_umap_cpp_2;
        is_generator = false;
        is_ordered = false;
    }
};

class Test_p_uimap : public BaseMapTest {
    void SetUp() override {
        map_func_1 = p_uimap_cpp_1;
        map_func_2 = p_uimap_cpp_2;
        is_generator = true;
        is_ordered = false;
    }
};

class Test_t_map : public BaseMapTest {
    void SetUp() override {
        map_func_1 = t_map_cpp_1;
        map_func_2 = t_map_cpp_2;
        is_generator = false;
        is_ordered = true;
    }
};

class Test_t_imap : public BaseMapTest {
    void SetUp() override {
        map_func_1 = t_imap_cpp_1;
        map_func_2 = t_imap_cpp_2;
        is_generator = true;
        is_ordered = true;
    }
};