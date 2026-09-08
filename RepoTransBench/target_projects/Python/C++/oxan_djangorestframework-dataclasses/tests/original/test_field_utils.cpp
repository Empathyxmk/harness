#include <gtest/gtest.h>
#include <string>
#include <typeindex>
#include <map>
#include <typeinfo>
#include <stdexcept>

// Simulate Python's Literal type
template<typename...>
struct LiteralTag {};

template<typename T>
struct TypeIdentity { using type = T; };

class FieldUtilsTest : public ::testing::Test {
protected:
    // Simulate type mapping and type lookup as in Python test
    std::map<std::type_index, int> mapping;

    void SetUp() override {
        mapping[typeid(std::string)] = 1;
        mapping[typeid(int)] = 2;
        mapping[typeid(std::variant<int, std::string>)] = 3;
    }

    template<typename T>
    int lookup_type_in_mapping() {
        auto it = mapping.find(typeid(T));
        if (it != mapping.end())
            return it->second;
        // Check for inheritance: if T derives from an existing mapped type
        // (simulate type('email', (str,), {}) in Python)
        if constexpr(std::is_base_of<std::string, T>::value) {
            return mapping[typeid(std::string)];
        }
        throw std::out_of_range("Key not found");
    }
};

TEST_F(FieldUtilsTest, test_lookup_type) {
    // Test builtin types
    EXPECT_EQ(lookup_type_in_mapping<std::string>(), 1);
    EXPECT_EQ(lookup_type_in_mapping<int>(), 2);
    EXPECT_EQ(lookup_type_in_mapping<std::variant<int, std::string>>(), 3);

    // Simulate a "subclass" of string
    struct email : public std::string {};
    EXPECT_EQ(lookup_type_in_mapping<email>(), 1);

    // Test expected failures
    try {
        lookup_type_in_mapping<float>();
        FAIL() << "Expected out_of_range for float";
    } catch(const std::out_of_range&) {
        SUCCEED();
    }

    // Simulate Literal['a', 'b'] as distinct, expect not found
    try {
        struct Literal_ab {};
        lookup_type_in_mapping<Literal_ab>();
        FAIL() << "Expected out_of_range for Literal['a', 'b']";
    } catch(const std::out_of_range&) {
        SUCCEED();
    }
}