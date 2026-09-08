#include <gtest/gtest.h>
#include <vector>

// Dummy barh interface for demonstration (would be in real barh.h)
namespace termplotlib {
namespace barh {
    void barh(const std::vector<int>& y, const std::vector<int>& x) {
        // Suppose the real implementation plots a bar chart
        (void)y; (void)x;
    }
}
}

TEST(TestBarh, TestSimpleBarh) {
    std::vector<int> y{3,2,5};
    std::vector<int> x{1,2,3};
    termplotlib::barh::barh(y, x);
    // No assertion: visual/interaction test in original
}