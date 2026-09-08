#include "convert2onnx/pytorch2onnx_resize.h"
#include <gtest/gtest.h>
#include <string>
#include <utility>

TEST(TestPyTorch2ONNXResize, DummyResizeFunc) {
    auto p1 = convert2onnx::dummy_resize_func(4, 5);
    EXPECT_EQ(p1, std::make_pair(4, 5));
    
    auto p2 = convert2onnx::dummy_resize_func(std::string("x"), 42);
    EXPECT_EQ(p2, std::make_pair(std::string("x"), 42));
}