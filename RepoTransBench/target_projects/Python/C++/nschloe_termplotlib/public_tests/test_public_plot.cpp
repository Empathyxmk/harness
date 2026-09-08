#include <gtest/gtest.h>
#include <vector>

namespace termplotlib {
namespace plot {
    void plot(const std::vector<int>& y, const std::vector<int>& x) {
        (void)y;(void)x;
    }
}
}

TEST(TestPlotPublic, TestSimplePlotDifferentData) {
    std::vector<int> y{0,4,2};
    std::vector<int> x{10,15,20};
    termplotlib::plot::plot(y, x);
}