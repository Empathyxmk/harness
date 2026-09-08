#include <gtest/gtest.h>
#include <vector>

// Dummy barh interface for demonstration
namespace termplotlib {
namespace barh {
    void barh(const std::vector<int>& y, const std::vector<int>& x) {
        (void)y;(void)x;
    }
}
}

TEST(TestBarhPublic, TestSimpleBarhDifferentData) {
    std::vector<int> y{6,1,4};
    std::vector<int> x{7,8,9};
    termplotlib::barh::barh(y, x);
}