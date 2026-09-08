#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

// Test minimal Wikipedia initialization
TEST(TestWikipediaObject, InitMinimal) {
    Wikipedia wiki("test/1.0", "en");
    ASSERT_EQ(wiki.language(), "en");
    ASSERT_EQ(wiki.extract_format(), ExtractFormat::WIKI);
}

// Test Wikipedia initialization with all arguments
TEST(TestWikipediaObject, InitAllArgs) {
    std::map<std::string, std::string> headers = { {"Foo", "Bar"} };
    std::map<std::string, std::string> extra_api_params = { {"baz", "qux"} };
    Wikipedia wiki("test/2.0", "de", "bar", ExtractFormat::HTML, headers, extra_api_params, 1);
    ASSERT_EQ(wiki.language(), "de");
    ASSERT_EQ(wiki.variant(), "bar");
    ASSERT_EQ(wiki.extract_format(), ExtractFormat::HTML);
}

// Test Wikipedia initialization with short user agent should throw
TEST(TestWikipediaObject, InitShortUserAgentThrows) {
    EXPECT_THROW({
        Wikipedia wiki("bot", "en");
    }, std::exception);
}