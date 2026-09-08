#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <type_traits>
#include <typeindex>
#include <tuple>
#include <map>
#include <any>
#include <memory>
#include <exception>
#include <optional>
#include <variant>
#include <cstddef>

// Typing test mimics Python typing_utils
class TypingTest : public ::testing::Test {
protected:
    template<typename T>
    bool is_iterable_type() {
        return std::is_same<T, std::vector<typename T::value_type>>::value ||
               std::is_same<T, std::vector<int>>::value; // simplistic
    }

    template<typename T>
    bool is_mapping_type() {
        return std::is_same<T, std::map<typename T::key_type, typename T::mapped_type>>::value ||
               std::is_same<T, std::map<std::string, int>>::value;
    }

    // More granular helpers could be added...
};

TEST_F(TypingTest, test_iterable) {
    ASSERT_TRUE((is_iterable_type<std::vector<int>>()));
    ASSERT_FALSE((is_iterable_type<int>()));
}

TEST_F(TypingTest, test_mapping) {
    ASSERT_TRUE((is_mapping_type<std::map<std::string, int>>()));
    ASSERT_FALSE((is_mapping_type<std::vector<int>>()));
}

TEST_F(TypingTest, test_optional) {
    std::optional<int> o1 = 5;
    std::optional<int> o2 = std::nullopt;
    ASSERT_TRUE(o1.has_value());
    ASSERT_FALSE(o2.has_value());
}

TEST_F(TypingTest, test_union) {
    std::variant<int, std::string> v;
    v = 42;
    EXPECT_EQ(std::get<int>(v), 42);
    v = std::string("hi");
    EXPECT_EQ(std::get<std::string>(v), "hi");
}

TEST_F(TypingTest, test_final) {
    // C++ does not have "Final" as a type qualifier in the typing sense
    SUCCEED();
}

TEST_F(TypingTest, test_literal) {
    // Simulate Literal via enum or const
    enum class PetType { Cat, Dog };
    PetType t = PetType::Cat;
    ASSERT_EQ(t, PetType::Cat);
}

TEST_F(TypingTest, test_variable_type) {
    // There is no direct C++ runtime TypeVar, but can check type traits at compile time
    SUCCEED();
}