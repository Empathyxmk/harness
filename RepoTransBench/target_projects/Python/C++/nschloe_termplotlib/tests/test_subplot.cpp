#include <gtest/gtest.h>
#include <tuple>
#include <vector>
#include <type_traits>

// Dummy Subplot (Any class found in termplotlib::subplot)
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

TEST(TestSubplot, TestSubplotInit) {
    using namespace termplotlib::subplot;
    Subplot sp({3,3}, 7);
    EXPECT_TRUE((std::is_same<decltype(sp), Subplot>::value));
}