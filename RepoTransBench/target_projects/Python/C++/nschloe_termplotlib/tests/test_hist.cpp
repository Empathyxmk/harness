#include <gtest/gtest.h>
#include <vector>

// Dummy hist namespace for demonstration
namespace termplotlib {
namespace hist {
    void hist(const std::vector<int>& data, const std::vector<int>& bins) {
        (void)data; (void)bins;
    }
}
}

TEST(TestHist, TestSimpleHist) {
    std::vector<int> data{1,2,2,3};
    std::vector<int> bin_edges{1,2,3};
    termplotlib::hist::hist(data, bin_edges);
}