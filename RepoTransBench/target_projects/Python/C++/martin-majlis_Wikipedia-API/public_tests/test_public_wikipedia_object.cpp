#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicWikipediaObjectTest, InitDifferentLanguage) {
    Wikipedia wiki("public-test/3.0", "fr");
    ASSERT_NE(&wiki, nullptr);
    ASSERT_EQ(wiki.language(), "fr");
    ASSERT_EQ(wiki.extract_format(), ExtractFormat::WIKI);
}

TEST(PublicWikipediaObjectTest, InitAllArgsDifferent) {
    Headers custom_headers = {{"Test", "Header"}};
    ApiParams extra_params = {{"foo", "bar"}};
    Wikipedia wiki(
        "public-test/4.0",
        "es",
        "an",
        ExtractFormat::WIKI,
        custom_headers,
        extra_params,
        2
    );
    ASSERT_EQ(wiki.language(), "es");
    ASSERT_EQ(wiki.variant(), "an");
    ASSERT_EQ(wiki.extract_format(), ExtractFormat::WIKI);
}

TEST(PublicWikipediaObjectTest, InitShortUserAgentRaises) {
    EXPECT_THROW({
        Wikipedia wiki("ai", "fr");
    }, std::exception);
}