#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

class TestLinks : public ::testing::Test {
protected:
    void SetUp() override {
        wiki = std::make_unique<Wikipedia>(mock_user_agent, "en");
        wiki->set_query_func(wikipedia_api_request(wiki.get()));
    }
    std::unique_ptr<Wikipedia> wiki;
};

TEST_F(TestLinks, LinksSinglePageCount) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.links().size(), 3);
}

TEST_F(TestLinks, LinksSinglePageTitles) {
    auto page = wiki->page("Test_1");
    std::vector<std::string> titles;
    for (const auto& kv : page.links()) { titles.push_back(kv.second->title()); }
    std::sort(titles.begin(), titles.end());
    std::vector<std::string> expected;
    for (int i = 0; i < 3; ++i) expected.push_back("Title - " + std::to_string(i+1));
    ASSERT_EQ(titles, expected);
}

TEST_F(TestLinks, LinksMultiPageCount) {
    auto page = wiki->page("Test_2");
    ASSERT_EQ(page.links().size(), 5);
}

TEST_F(TestLinks, LinksMultiPageTitles) {
    auto page = wiki->page("Test_2");
    std::vector<std::string> titles;
    for (const auto& kv : page.links()) { titles.push_back(kv.second->title()); }
    std::sort(titles.begin(), titles.end());
    std::vector<std::string> expected;
    for (int i = 0; i < 5; ++i) expected.push_back("Title - " + std::to_string(i+1));
    ASSERT_EQ(titles, expected);
}

TEST_F(TestLinks, LinksNoLinksCount) {
    auto page = wiki->page("No_Links");
    ASSERT_EQ(page.links().size(), 0);
}

TEST_F(TestLinks, LinksFromVariant) {
    Wikipedia wiki_zh(mock_user_agent, "zh", "zh-tw");
    wiki_zh.set_query_func(wikipedia_api_request(&wiki_zh));
    auto page = wiki_zh.page("Test_Zh-Tw");
    std::vector<std::pair<std::string, std::string>> titles;
    for (const auto& kv : page.links()) {
        titles.emplace_back(kv.second->title(), kv.second->variant());
    }
    std::sort(titles.begin(), titles.end());
    std::vector<std::pair<std::string, std::string>> expected;
    for (int i = 0; i < 3; ++i) expected.emplace_back("Title - Zh-Tw - " + std::to_string(i+1), "zh-tw");
    ASSERT_EQ(titles, expected);
}