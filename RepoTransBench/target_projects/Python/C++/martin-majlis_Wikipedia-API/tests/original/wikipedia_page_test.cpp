#include <gtest/gtest.h>
#include "mock_wikipedia.h"

// Custom helpers for encoding/unquoting, exception checks, etc. assumed available in mock_wikipedia.h and helpers.

class TestWikipediaPage : public ::testing::Test {
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

TEST_F(TestWikipediaPage, test_repr_before_fetching) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.repr(), "Test_1 (lang: en, variant: None, id: ??, ns: 0)");
}

TEST_F(TestWikipediaPage, test_repr_after_fetching) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.repr(), "Test_1 (lang: en, variant: None, id: ??, ns: 0)");
    ASSERT_EQ(page.pageid, 4);
    ASSERT_EQ(page.repr(), "Test 1 (lang: en, variant: None, id: 4, ns: 0)");
}

TEST_F(TestWikipediaPage, test_extract) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.pageid, 4);
    ASSERT_EQ(page.title, "Test 1");
    ASSERT_EQ(page.ns, 0);
    ASSERT_EQ(page.contentmodel, "wikitext");
    ASSERT_EQ(page.pagelanguage, "en");
    ASSERT_EQ(page.pagelanguagedir, "ltr");
    ASSERT_EQ(page.fullurl, "https://en.wikipedia.org/wiki/Test_1");
    ASSERT_EQ(
        page.editurl,
        "https://en.wikipedia.org/w/index.php?title=Test_1&action=edit"
    );
    ASSERT_EQ(page.canonicalurl, "https://en.wikipedia.org/wiki/Test_1");
    ASSERT_EQ(page.displaytitle, "Test 1");
    ASSERT_TRUE(page.variant.empty()); // In C++: expect empty for no variant
}

TEST_F(TestWikipediaPage, test_unknown_property) {
    auto page = wiki->page("Test_1");
    // C++ equivalent would be an exception thrown on .unknown_property access
    try {
        auto val = page.unknown_property();
        FAIL() << "Expected std::runtime_error or std::out_of_range";
    } catch(const std::exception& e) {
        SUCCEED();
    }
}

TEST_F(TestWikipediaPage, test_nonexisting) {
    auto page = wiki->page("NonExisting");
    ASSERT_FALSE(page.exists());
}

TEST_F(TestWikipediaPage, test_existing) {
    auto page = wiki->page("Test_1");
    ASSERT_TRUE(page.exists());
}

TEST_F(TestWikipediaPage, test_article_method) {
    auto p = wiki->page("Test_1");
    auto a = wiki->article("Test_1");
    ASSERT_EQ(p.pageid, a.pageid);
}

TEST_F(TestWikipediaPage, test_article_title_unquote) {
    // https://github.com/goldsmith/Wikipedia/issues/190
    WikipediaMock w(user_agent, "hi");
    w.set_query(wikipedia_api_request(w));
    auto p_encoded = w.article("%E0%A4%AA%E0%A4%BE%E0%A4%87%E0%A4%A5%E0%A4%A8", /*unquote=*/true);
    auto p_decoded = w.article(u8"पाइथन");
    ASSERT_EQ(p_encoded.pageid, p_decoded.pageid);
}

TEST_F(TestWikipediaPage, test_page_title_unquote) {
    // https://github.com/goldsmith/Wikipedia/issues/190
    WikipediaMock w(user_agent, "hi");
    w.set_query(wikipedia_api_request(w));
    auto p_encoded = w.page("%E0%A4%AA%E0%A4%BE%E0%A4%87%E0%A4%A5%E0%A4%A8", /*unquote=*/true);
    auto p_decoded = w.page(u8"पाइथन");
    ASSERT_EQ(p_encoded.pageid, p_decoded.pageid);
}

TEST_F(TestWikipediaPage, test_page_with_int_namespace) {
    auto page = wiki->page("NonExisting", 110);
    ASSERT_FALSE(page.exists());
    ASSERT_EQ(page.namespace_id, 110);
}

TEST_F(TestWikipediaPage, test_page_with_variant) {
    WikipediaMock wiki_zh(user_agent, "zh", "zh-tw");
    wiki_zh.set_query(wikipedia_api_request(wiki_zh));
    auto page = wiki_zh.page("Test_Zh-Tw");
    ASSERT_TRUE(page.exists());
    ASSERT_EQ(page.pageid, 44);
    ASSERT_EQ(page.title, "Test Zh-Tw");
    ASSERT_EQ(page.variant, "zh-tw");
    std::map<std::string, std::string> varianttitles_expected = {
        {"zh", "Test Zh"},
        {"zh-hans", "Test Zh-Hans"},
        {"zh-tw", "Test Zh-Tw"}
    };
    ASSERT_EQ(page.varianttitles, varianttitles_expected);
}

TEST_F(TestWikipediaPage, test_page_with_extra_parameters) {
    std::map<std::string, std::string> params = {{"foo", "bar"}};
    WikipediaMock wiki_extra(user_agent, "en", "", params);
    wiki_extra.set_query(wikipedia_api_request(wiki_extra));
    auto page = wiki_extra.page("Extra_API_Params");
    ASSERT_TRUE(page.exists());
}