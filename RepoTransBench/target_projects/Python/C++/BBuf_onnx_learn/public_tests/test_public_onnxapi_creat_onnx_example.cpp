#include "onnxapi/creat_onnx_example.h"
#include <gtest/gtest.h>
#include <string>
#include <vector>

TEST(TestPublicOnnxApiCreatOnnxExample, MakeIdentity) {
    EXPECT_EQ(onnxapi::make_identity(std::string("hello")), "hello");
    std::vector<int> vec = {7,8,9};
    EXPECT_EQ(onnxapi::make_identity(vec), vec);
}

TEST(TestPublicOnnxApiCreatOnnxExample, SumList) {
    EXPECT_EQ(onnxapi::sum_list({4,5,6}), 15);
    EXPECT_EQ(onnxapi::sum_list({100}), 100);
}