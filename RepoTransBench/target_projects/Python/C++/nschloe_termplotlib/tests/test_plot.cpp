#include <gtest/gtest.h>
#include <vector>

// Dummy plot function for demonstration
namespace termplotlib {
namespace plot {
    void plot(const std::vector<int>& y, const std::vector<int>& x) {
        // Would render a plot
        (void)y; (void)x;
    }
}
}

TEST(TestPlot, TestSimplePlot) {
    std::vector<int> y{2,3,1};
    std::vector<int> x{1,2,3};
    termplotlib::plot::plot(y, x);
}