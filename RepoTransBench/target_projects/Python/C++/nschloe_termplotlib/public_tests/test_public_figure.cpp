#include <gtest/gtest.h>
#include <type_traits>

// Dummy Figure and Axes for demonstration
namespace termplotlib {
namespace figure {
    class Axes {};
    class Figure {
    public:
        Figure() : counter_(0) {}

        Axes* add_subplot(int /*code*/) {
            axes_.emplace_back(new Axes());
            return axes_.back();
        }
    private:
        int counter_;
        std::vector<Axes*> axes_;
    };
}
}

TEST(TestFigurePublic, TestFigureCreationAndAxes) {
    using namespace termplotlib::figure;
    Figure f;
    Axes* ax = f.add_subplot(111);
    EXPECT_TRUE((std::is_pointer<decltype(ax)>::value));
    EXPECT_TRUE((std::is_same<std::remove_pointer<decltype(ax)>::type, Axes>::value));
    Axes* ax2 = f.add_subplot(112);
    EXPECT_NE(ax, ax2);
}