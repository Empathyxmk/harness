#include <gtest/gtest.h>

// Dummy Figure class for demonstration
namespace termplotlib {
namespace figure {
    class Figure {};
}
}

TEST(TestFigure, TestFigureInit) {
    termplotlib::figure::Figure fig;
    EXPECT_TRUE((std::is_same<decltype(fig), termplotlib::figure::Figure>::value));
}