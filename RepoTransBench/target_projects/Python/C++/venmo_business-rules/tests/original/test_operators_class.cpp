#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "business_rules/operators.h"
#include <string>

class SomeType : public BaseType {
public:
    // Must define mocking for _assert_valid_value_and_cast
    MOCK_METHOD(void, _assert_valid_value_and_cast, (std::string), ());
    bool some_operator(std::string other_param) { return true; }
    bool other_operator(std::string other_param) { return true; }
};

TEST(OperatorsClassTests, base_has_no_operators) {
    EXPECT_EQ(BaseType::get_all_operators().size(), 0);
}

TEST(OperatorsClassTests, get_all_operators) {
    std::vector<OperatorMetadata> operators = SomeType::get_all_operators();
    ASSERT_EQ(operators.size(), 1);
    auto some_operator = operators[0];
    EXPECT_EQ(some_operator.name, "some_operator");
    EXPECT_EQ(some_operator.label, "Some Operator");
    EXPECT_EQ(some_operator.input_type, "text");
}

// etc.