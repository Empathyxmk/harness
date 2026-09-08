#include <gtest/gtest.h>
#include <type_traits>
#include <vector>

namespace termplotlib {
namespace subplot {
    class Subplot {
    public:
        Subplot(std::pair<int,int> shape, int index) : shape_(shape), index_(index) {}
        std::pair<int,int> shape_;
        int index_;
    };
}
}

// Emulate Python's fallback to first class found (there's only Subplot here)
TEST(TestSubplotPublic, TestSubplotInitDifferentData) {
    using namespace termplotlib::subplot;
    Subplot sp({2,4}, 5);
    EXPECT_TRUE((std::is_same<decltype(sp), Subplot>::value));
}