#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"
#include <algorithm>

class TestWikiFormatExtracts : public ::testing::Test {
protected:
    void SetUp() override {
        wiki = std::make_unique<Wikipedia>(mock_user_agent, "en");
        wiki->set_query_func(wikipedia_api_request(wiki.get()));
    }
    std::unique_ptr<Wikipedia> wiki;
};

TEST_F(TestWikiFormatExtracts, TitleBeforeFetching) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.title(), "Test_1");
}

TEST_F(TestWikiFormatExtracts, PageId) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.pageid(), 4);
}

TEST_F(TestWikiFormatExtracts, TitleAfterFetching) {
    auto page = wiki->page("Test_1");
    page._fetch("extracts");
    ASSERT_EQ(page.title(), "Test 1");
}

TEST_F(TestWikiFormatExtracts, Summary) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.summary(), "Summary text");
}

TEST_F(TestWikiFormatExtracts, SectionCount) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.sections().size(), 5);
}

TEST_F(TestWikiFormatExtracts, TopLevelSectionTitles) {
    auto page = wiki->page("Test_1");
    std::vector<std::string> section_titles;
    for (const auto& section : page.sections())
        section_titles.push_back(section.title());
    std::vector<std::string> expected;
    for (int i = 0; i < 5; ++i)
        expected.push_back("Section " + std::to_string(i+1));
    ASSERT_EQ(section_titles, expected);
}

TEST_F(TestWikiFormatExtracts, SubsectionByTitle) {
    auto page = wiki->page("Test_1");
    auto section = page.section_by_title("Section 4");
    ASSERT_EQ(section.title(), "Section 4");
    ASSERT_EQ(section.level(), 1);
}

TEST_F(TestWikiFormatExtracts, Subsection) {
    auto page = wiki->page("Test_1");
    auto section = page.section_by_title("Section 4");
    ASSERT_EQ(section.title(), "Section 4");
    ASSERT_EQ(section.text(), "");
    ASSERT_EQ(section.sections().size(), 2);
}

TEST_F(TestWikiFormatExtracts, Subsubsection) {
    auto page = wiki->page("Test_1");
    auto section = page.section_by_title("Section 4.2.2");
    ASSERT_EQ(section.title(), "Section 4.2.2");
    ASSERT_EQ(section.text(), "Text for section 4.2.2");

    std::string expected_repr =
        "Section: Section 4.2.2 (3):\n"
        "Text for section 4.2.2\n"
        "Subsections (0):\n";
    ASSERT_EQ(section.repr(), expected_repr);
    ASSERT_EQ(section.sections().size(), 0);
}

TEST_F(TestWikiFormatExtracts, PageText) {
    auto page = wiki->page("Test_1");
    std::string expected =
        "Summary text\n\n"
        "Section 1\n"
        "Text for section 1\n\n"
        "Section 1.1\n"
        "Text for section 1.1\n\n"
        "Section 1.2\n"
        "Text for section 1.2\n\n"
        "Section 2\n"
        "Text for section 2\n\n"
        "Section 3\n"
        "Text for section 3\n\n"
        "Section 4\n"
        "Section 4.1\n"
        "Text for section 4.1\n\n"
        "Section 4.2\n"
        "Text for section 4.2\n\n"
        "Section 4.2.1\n"
        "Text for section 4.2.1\n\n"
        "Section 4.2.2\n"
        "Text for section 4.2.2\n\n"
        "Section 5\n"
        "Text for section 5\n\n"
        "Section 5.1\n"
        "Text for section 5.1";
    ASSERT_EQ(page.text(), expected);
}

TEST_F(TestWikiFormatExtracts, TextAndSummaryWithoutSections) {
    auto page = wiki->page("No_Sections");
    ASSERT_EQ(page.text(), "Summary text");
    ASSERT_EQ(page.summary(), "Summary text");
}