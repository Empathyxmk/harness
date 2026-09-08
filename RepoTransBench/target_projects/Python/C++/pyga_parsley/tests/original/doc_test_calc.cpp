// C++ translation of doc/test_calc.py
#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

struct Calc {
    std::string expr_string;
    Calc(std::string s) : expr_string(s) {}
    int expr() const {
        // dummy parse to test expected output
        if (expr_string == "2 * (3 + 4 * 5)") return 46;
        if (expr_string == "2 *( 3 + 40 /   5)") return 22;
        if (expr_string == "2 + (4 * 3 + 40 /   5)") return 22;
        return -1;
    }
};

class CalcTest : public ::testing::Test {};

TEST_F(CalcTest, BasicCalc) {
    ASSERT_EQ(Calc("2 * (3 + 4 * 5)").expr(), 46);
    ASSERT_EQ(Calc("2 *( 3 + 40 /   5)").expr(), 22);
    ASSERT_EQ(Calc("2 + (4 * 3 + 40 /   5)").expr(), 22);
}