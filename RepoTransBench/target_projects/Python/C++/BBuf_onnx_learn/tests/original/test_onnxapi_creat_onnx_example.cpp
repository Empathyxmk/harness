#include "onnxapi/creat_onnx_example.h"
#include <gtest/gtest.h>
#include <vector>
#include <string>

TEST(TestOnnxApiCreatOnnxExample, MakeIdentity) {
    EXPECT_EQ(onnxapi::make_identity(100), 100);
    std::vector<int> a = {1,2,3};
    EXPECT_EQ(onnxapi::make_identity(a), a);
}

TEST(TestOnnxApiCreatOnnxExample, SumList) {
    EXPECT_EQ(onnxapi::sum_list({1,2,3}), 6);
    std::vector<int> empty;
    EXPECT_EQ(onnxapi::sum_list(empty), 0);
}