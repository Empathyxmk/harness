#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include "ai_functions.hpp"

using namespace ai_functions;

TEST(AiFunctionPublicTests, Success) {
    auto dummy_create = [](const std::string& model, const std::vector<std::map<std::string, std::string>>& messages) -> std::string {
        EXPECT_EQ(model, "gpt-4");
        EXPECT_EQ(messages.size(), 2);
        EXPECT_EQ(messages[0].at("role"), "system");
        EXPECT_EQ(messages[1].at("role"), "user");
        return "17";
    };
    std::string result = ai_function(
        "def subtract(a, b): return a - b",
        {"20", "3"},
        "Subtracts two numbers",
        "gpt-4",
        dummy_create
    );
    EXPECT_EQ(result, "17");
}

TEST(AiFunctionPublicTests, CustomModel) {
    auto dummy_create = [](const std::string& model, const std::vector<std::map<std::string, std::string>>& messages) -> std::string {
        EXPECT_EQ(model, "gpt-3.5-turbo");
        return "15";
    };
    std::string result = ai_function(
        "def div(a, b): return a // b",
        {"30", "2"},
        "Divide and floor two numbers",
        "gpt-3.5-turbo",
        dummy_create
    );
    EXPECT_EQ(result, "15");
}

TEST(AiFunctionPublicTests, NoArgs) {
    auto dummy_create = [](const std::string& model, const std::vector<std::map<std::string, std::string>>& messages) -> std::string {
        return "empty args handled";
    };
    std::string result = ai_function(
        "def hello(): return 'hello'",
        {},
        "No-argument greeting function",
        "gpt-4",
        dummy_create
    );
    EXPECT_EQ(result, "empty args handled");
}

TEST(AiFunctionPublicTests, ResponseStructure) {
    std::vector<std::map<std::string, std::string>> captured_messages;
    auto dummy_create = [&](const std::string& model, const std::vector<std::map<std::string, std::string>>& messages) -> std::string {
        captured_messages = messages;
        return "Y";
    };
    ai_function(
        "def echo(s): return s",
        {"foo"},
        "Echo string argument",
        "gpt-4",
        dummy_create
    );
    ASSERT_EQ(captured_messages.size(), 2);
    const auto& sys_msg = captured_messages.at(0);
    EXPECT_EQ(sys_msg.at("role"), "system");
    EXPECT_NE(sys_msg.at("content").find("python function"), std::string::npos);
    const auto& user_msg = captured_messages.at(1);
    EXPECT_EQ(user_msg.at("role"), "user");
    EXPECT_EQ(user_msg.at("content"), "foo");
}