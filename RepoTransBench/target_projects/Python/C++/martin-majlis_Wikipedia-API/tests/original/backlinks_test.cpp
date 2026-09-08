#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

class TestBackLinks : public ::testing::Test {
protected:
    void SetUp() override {
        wiki = std::make_unique<Wikipedia>(mock_user_agent, "en");
        wiki->set_query_func(wikipedia_api_request(wiki.get()));
    }
    std::unique_ptr<Wikipedia> wiki;
};

TEST_F(TestBackLinks, BacklinksNonexistentCount) {
    auto page = wiki->page("Non_Existent");
    ASSERT_EQ(page.backlinks().size(), 0);
}

TEST_F(TestBackLinks, BacklinksSinglePageCount) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.backlinks().size(), 3);
}

TEST_F(TestBackLinks, BacklinksSinglePageTitles) {
    auto page = wiki->page("Test_1");
    std::vector<std::string> titles;
    for (const auto& kv : page.backlinks()) titles.push_back(kv.second->title());
    std::sort(titles.begin(), titles.end());
    std::vector<std::string> expected;
    for (int i = 0; i < 3; ++i) expected.push_back("Title - " + std::to_string(i+1));
    ASSERT_EQ(titles, expected);
}

TEST_F(TestBackLinks, BacklinksMultiPageCount) {
    auto page = wiki->page("Test_2");
    ASSERT_EQ(page.backlinks().size(), 5);
}

TEST_F(TestBackLinks, BacklinksMultiPageTitles) {
    auto page = wiki->page("Test_2");
    std::vector<std::string> titles;
    for (const auto& kv : page.backlinks()) titles.push_back(kv.second->title());
    std::sort(titles.begin(), titles.end());
    std::vector<std::string> expected;
    for (int i = 0; i < 5; ++i) expected.push_back("Title - " + std::to_string(i+1));
    ASSERT_EQ(titles, expected);
}