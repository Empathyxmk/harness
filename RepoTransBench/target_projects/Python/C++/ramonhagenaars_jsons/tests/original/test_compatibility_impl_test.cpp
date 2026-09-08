#include <gtest/gtest.h>
#include <type_traits>
#include <map>
#include <string>
#include <stdexcept>
#include <unordered_map>

// Bitwise flag simulation
class Flag {
public:
    int value;
    explicit Flag(int v) : value(v) {}
    Flag operator|(const Flag& rhs) const { return Flag(value | rhs.value); }
    bool operator==(const Flag& rhs) const { return value == rhs.value; }
    bool operator!=(const Flag& rhs) const { return !(*this == rhs); }
    bool in(const Flag& mask) const { return (value & mask.value) != 0; }
};


TEST(TestCompatibilityImpl, test_flag) {
    class F {
    public:
        static const Flag A, B, C, D, E;
    };
    const Flag F::A = Flag(0);
    const Flag F::B = Flag(10);
    const Flag F::C = Flag(20);
    const Flag F::D = Flag(40);
    const Flag F::E = Flag(80);

    EXPECT_EQ(F::C.value, 20);
    EXPECT_EQ((F::B | F::C).value, 30);
    EXPECT_TRUE(F::A.in(F::B | F::C) == false);
    EXPECT_TRUE(F::B.in(F::B | F::C));
    EXPECT_TRUE(F::C.in(F::B | F::C));
    EXPECT_FALSE(F::D.in(F::B | F::C));
    EXPECT_FALSE(F::C.in(F::B | F::D));
    EXPECT_FALSE(F::E.in(F::B | F::D));
}

// Simulates a get_type_hints fallback
std::unordered_map<std::string, int> get_type_hints(bool raiseNameError = false) {
    std::unordered_map<std::string, int> hints;
    if (raiseNameError) throw std::runtime_error("NameError");
    return hints;
}

TEST(TestCompatibilityImpl, test_get_type_hints) {
    auto result = get_type_hints(false);
    EXPECT_EQ(result, std::unordered_map<std::string, int>{});

    bool raised = false;
    try {
        auto result = get_type_hints(true);
    } catch (const std::runtime_error& e) {
        raised = true;
        EXPECT_STREQ(e.what(), "NameError");
    }
    EXPECT_TRUE(raised);
}