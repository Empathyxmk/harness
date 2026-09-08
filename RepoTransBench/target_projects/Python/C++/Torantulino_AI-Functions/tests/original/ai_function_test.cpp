#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include "ai_functions.hpp"

using namespace ai_functions;

// DummyChoice - not needed in C++ due to design, we mock at OpenAICreateFunc level
// DummyResponse - not needed; mock handler returns string

TEST(AiFunctionTests, Success) {
    auto dummy_create = [](const std::string& model, const std::vector<std::map<std::string, std::string>>& messages) -> std::string {
        EXPECT_EQ(model, "gpt-4");
        EXPECT_EQ(messages.size(), 2);
        EXPECT_EQ(messages[0].at("role"), "system");
        EXPECT_EQ(messages[1].at("role"), "user");
        return "42";
    };
    std::string result = ai_function(
        "def add(a, b): return a + b",
        {"2", "40"},
        "Adds two numbers",
        "gpt-4",
        dummy_create
    );
    EXPECT_EQ(result, "42");
}

TEST(AiFunctionTests, CustomModel) {
    auto dummy_create = [](const std::string& model, const std::vector<std::map<std::string, std::string>>& messages) -> std::string {
        EXPECT_EQ(model, "gpt-3.5-turbo");
        return "7";
    };
    std::string result = ai_function(
        "def mul(a, b): return a * b",
        {"3", "4"},
        "Multiply two numbers",
        "gpt-3.5-turbo",
        dummy_create
    );
    EXPECT_EQ(result, "7");
}

TEST(AiFunctionTests, NoArgs) {
    auto dummy_create = [](const std::string& model, const std::vector<std::map<std::string, std::string>>& messages) -> std::string {
        // Accepts empty args
        return "no args";
    };
    std::string result = ai_function(
        "def f(): return None",
        {},
        "No-argument function",
        "gpt-4",
        dummy_create
    );
    EXPECT_EQ(result, "no args");
}

TEST(AiFunctionTests, ResponseStructure) {
    // Test message construction
    std::vector<std::map<std::string, std::string>> captured_messages;
    auto dummy_create = [&](const std::string& model, const std::vector<std::map<std::string, std::string>>& messages) -> std::string {
        captured_messages = messages;
        return "X";
    };
    ai_function(
        "def f(x): return x",
        {"7"},
        "Echo integer",
        "gpt-4",
        dummy_create
    );
    ASSERT_EQ(captured_messages.size(), 2);
    const auto& sys_msg = captured_messages.at(0);
    EXPECT_EQ(sys_msg.at("role"), "system");
    EXPECT_NE(sys_msg.at("content").find("python function"), std::string::npos);
    const auto& user_msg = captured_messages.at(1);
    EXPECT_EQ(user_msg.at("role"), "user");
    EXPECT_EQ(user_msg.at("content"), "7");
}