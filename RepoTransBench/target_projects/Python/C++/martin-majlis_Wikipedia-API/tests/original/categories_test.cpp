#include <gtest/gtest.h>
#include "mock_wikipedia.h"

class TestCategories : public ::testing::Test {
protected:
    void SetUp() override {
        wiki = new WikipediaMock(user_agent, "en");
        wiki->set_query(wikipedia_api_request(*wiki));
    }
    void TearDown() override {
        delete wiki;
    }
    WikipediaMock* wiki;
};

TEST_F(TestCategories, test_categories_count) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.categories.size(), 3);
}

TEST_F(TestCategories, test_categories_titles) {
    auto page = wiki->page("Test_1");

    std::vector<std::string> actual_titles;
    for (const auto& kv : page.categories) {
        actual_titles.push_back(kv.second.title);
    }
    std::sort(actual_titles.begin(), actual_titles.end());

    std::vector<std::string> expected_titles;
    for (int i = 0; i < 3; ++i) {
        expected_titles.push_back("Category:C" + std::to_string(i + 1));
    }

    ASSERT_EQ(actual_titles, expected_titles);
}

TEST_F(TestCategories, test_categories_nss) {
    auto page = wiki->page("Test_1");

    std::vector<int> actual_ns;
    for (const auto& kv : page.categories) {
        actual_ns.push_back(kv.second.ns);
    }
    std::sort(actual_ns.begin(), actual_ns.end());

    std::vector<int> expected_ns(3, 14);

    ASSERT_EQ(actual_ns, expected_ns);
}

TEST_F(TestCategories, test_no_categories_count) {
    auto page = wiki->page("No_Categories");
    ASSERT_EQ(page.categories.size(), 0);
}