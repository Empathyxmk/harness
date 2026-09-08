#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

class TestErrorsExtracts : public ::testing::Test {
protected:
    void SetUp() override {
        wiki = std::make_unique<Wikipedia>(mock_user_agent, "en");
        wiki->set_query_func(wikipedia_api_request(wiki.get()));
    }
    std::unique_ptr<Wikipedia> wiki;
};

TEST_F(TestErrorsExtracts, TitleBeforeFetching) {
    auto page = wiki->page("NonExisting");
    ASSERT_EQ(page.title(), "NonExisting");
}

TEST_F(TestErrorsExtracts, PageId) {
    auto page = wiki->page("NonExisting");
    ASSERT_EQ(page.pageid(), -1);
}