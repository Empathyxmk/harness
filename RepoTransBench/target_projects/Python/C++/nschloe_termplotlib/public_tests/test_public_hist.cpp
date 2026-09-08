#include <gtest/gtest.h>
#include <vector>
#include <string>

// Dummy hist for demonstration
namespace termplotlib {
namespace hist {
    void hist(const std::vector<int>& data, int bins) {
        (void)data;
        (void)bins;
    }
    void hist(const std::vector<int>& data, int bins,
              const std::string& title, const std::string& xlabel,
              const std::string& ylabel, bool grid, bool ascii) {
        (void)data; (void)bins; (void)title; (void)xlabel; (void)ylabel; (void)grid; (void)ascii;
    }
}
}

TEST(TestHistPublic, TestSimpleHistDiffData) {
    std::vector<int> data{3,6,9,3,6,9,9};
    termplotlib::hist::hist(data, 3);
}

TEST(TestHistPublic, TestHistLabelAndAscii) {
    std::vector<int> data{7,1,6,8,7,5,5};
    termplotlib::hist::hist(data, 2, "New Title", "Alternate X", "Alternate Y", true, true);
}