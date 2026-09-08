#include <gtest/gtest.h>
#include <vector>

namespace termplotlib {
namespace plot {
    void plot(const std::vector<int>& y, const std::vector<int>& x) {
        (void)y;(void)x;
    }
}
}

TEST(TestScatterPublic, TestSimpleScatterDifferentData) {
    std::vector<int> x{4,5,6};
    std::vector<int> y{6,5,4};
    termplotlib::plot::plot(y, x);
}