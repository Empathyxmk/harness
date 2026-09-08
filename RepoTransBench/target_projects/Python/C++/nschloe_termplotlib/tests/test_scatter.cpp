#include <gtest/gtest.h>
#include <vector>

// Dummy plot namespace for demonstration
namespace termplotlib {
namespace plot {
    void plot(const std::vector<int>& y, const std::vector<int>& x) {
        // Suppose this would produce a scatter or line plot
        (void)y; (void)x;
    }
}
}

TEST(TestScatter, TestSimpleScatter) {
    std::vector<int> x{1,2,3};
    std::vector<int> y{3,2,1};
    termplotlib::plot::plot(y, x);
    // No assertions as in original Python test.
}