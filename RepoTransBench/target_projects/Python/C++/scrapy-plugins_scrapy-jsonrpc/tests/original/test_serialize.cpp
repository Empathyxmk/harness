#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include "src/lib/serialize.h"

TEST(SerializeTest, ScrapyJsonDumpsBasic) {
    nlohmann::json obj = {{"a", 1}, {"b", 2}};
    std::string s = scrapy_json_dumps(obj);
    // order is not guaranteed in json
    bool valid = (s == "{\"a\":1,\"b\":2}" || s == "{\"b\":2,\"a\":1}");
    EXPECT_TRUE(valid);
}

class MyItem : public BaseItem {
public:
    MyItem(int av) { a = av; }
    int a;
};

TEST(SerializeTest, ScrapyJsonDumpsHandlesCustomItem) {
    MyItem i(5);
    std::string s = scrapy_json_dumps(i);
    EXPECT_NE(s.find("\"a\":5"), std::string::npos);
}

TEST(SerializeTest, ScrapyJsonDumpsHandlesField) {
    Field f;
    std::string s = scrapy_json_dumps(std::map<std::string, Field>{{"f", f}});
    EXPECT_NE(s.find("\"<Field instance>\""), std::string::npos);
}

TEST(SerializeTest, ScrapyJsonDumpsHandlesFakeSpider) {
    class Spider { public: std::string name = "sp1"; };
    Spider sp;
    std::map<std::string, Spider> d = {{"sp", sp}};
    std::string s = scrapy_json_dumps(d);
    EXPECT_NE(s.find("\"<Spider: sp1>\""), std::string::npos);
}

TEST(SerializeTest, ScrapyJsonLoadsAndDecoder) {
    nlohmann::json d = {{"a", 1}, {"b", "hi"}};
    std::string s = scrapy_json_dumps(d);
    auto loaded = scrapy_json_loads(s);
    EXPECT_EQ(loaded, d);
}

TEST(SerializeTest, DefaultTypeError) {
    class NotSerializable {};
    try {
        NotSerializable n;
        scrapy_json_dumps(n);
        FAIL() << "Expected std::runtime_error";
    } catch(const std::runtime_error& ex) {
        SUCCEED();
    }
}

TEST(SerializeTest, IsItem) {
    EXPECT_TRUE(is_item(nlohmann::json{{"x", 1}}));
    class It : public BaseItem {};
    It it;
    EXPECT_TRUE(is_item(it));
    EXPECT_FALSE(is_item(123));
    EXPECT_FALSE(is_item(std::string("str")));
}