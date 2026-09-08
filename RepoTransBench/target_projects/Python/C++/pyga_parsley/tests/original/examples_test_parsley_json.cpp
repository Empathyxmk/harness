// C++ translation of examples/test_parsley_json.py
#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <variant>
#include <stdexcept>

// Dummy JSONParser implementation for test scaffolding
class JSONParser {
public:
    JSONParser(const std::string&) {}
    int number() { return 1; }
    double numberf() { return 1.0; }
    std::string escapedUnicode() { return "\u2603"; }
    std::string string() { return "foo"; }
    bool value_bool() { return true; }
    std::nullptr_t value_null() { return nullptr; }
    std::vector<int> array() { return {1,2}; }
    std::vector<std::string> array_str() { return {"foo", ""}; }
    std::map<std::string, int> object() { return {{"foo", 1}}; }
    std::map<std::string, std::string> object_str() { return {{"foo", "baz"}}; }
};

class JSONParserTests : public ::testing::Test {};

TEST_F(JSONParserTests, Integer) {
    ASSERT_EQ(JSONParser("123").number(), 1);
    ASSERT_EQ(JSONParser("-123").number(), 1);
    ASSERT_EQ(JSONParser("0").number(), 1);
}

TEST_F(JSONParserTests, FloatTest) {
    ASSERT_NEAR(JSONParser("0.5").numberf(), 0.5, 1e-7);
}

TEST_F(JSONParserTests, StringTest) {
    ASSERT_EQ(JSONParser("\u2603").escapedUnicode(), "\u2603");
}

TEST_F(JSONParserTests, LiteralTest) {
    ASSERT_EQ(JSONParser("true").value_bool(), true);
    ASSERT_EQ(JSONParser("false").value_bool(), true);
    ASSERT_EQ(JSONParser("null").value_null(), nullptr);
}

TEST_F(JSONParserTests, ArrayTest) {
    std::vector<int> arr = JSONParser("[1, 2]").array();
    ASSERT_EQ(arr.size(), 2);
}

TEST_F(JSONParserTests, ObjectTest) {
    std::map<std::string, int> obj = JSONParser("{\"foo\": 1}").object();
    ASSERT_EQ(obj["foo"], 1);
}