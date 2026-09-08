#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

class TestHtmlFormatExtracts : public ::testing::Test {
protected:
    void SetUp() override {
        wiki = std::make_unique<Wikipedia>(mock_user_agent, "en", ExtractFormat::HTML);
        wiki->set_query_func(wikipedia_api_request(wiki.get()));
    }
    std::unique_ptr<Wikipedia> wiki;
};

TEST_F(TestHtmlFormatExtracts, TitleBeforeFetching) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.title(), "Test_1");
}

TEST_F(TestHtmlFormatExtracts, PageId) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.pageid(), 4);
}

TEST_F(TestHtmlFormatExtracts, TitleAfterFetching) {
    auto page = wiki->page("Test_1");
    page._fetch("extracts");
    ASSERT_EQ(page.title(), "Test 1");
}

TEST_F(TestHtmlFormatExtracts, Summary) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.summary(), "<p><b>Summary</b> text\n\n</p>");
}

TEST_F(TestHtmlFormatExtracts, SectionCount) {
    auto page = wiki->page("Test_1");
    ASSERT_EQ(page.sections().size(), 5);
}

TEST_F(TestHtmlFormatExtracts, TopLevelSectionTitles) {
    auto page = wiki->page("Test_1");
    std::vector<std::string> section_titles;
    for (const auto& section : page.sections())
        section_titles.push_back(section.title());
    std::vector<std::string> expected;
    for (int i = 0; i < 5; ++i)
        expected.push_back("Section " + std::to_string(i+1));
    ASSERT_EQ(section_titles, expected);
}

TEST_F(TestHtmlFormatExtracts, SubsectionByTitle) {
    auto page = wiki->page("Test_1");
    auto section = page.section_by_title("Section 4");
    ASSERT_EQ(section.title(), "Section 4");
    ASSERT_EQ(section.level(), 1);
}

TEST_F(TestHtmlFormatExtracts, SubsectionByTitleWithMultipleSpans) {
    auto page = wiki->page("Test_1");
    auto section = page.section_by_title("Section 5");
    ASSERT_EQ(section.title(), "Section 5");
}

TEST_F(TestHtmlFormatExtracts, Subsection) {
    auto page = wiki->page("Test_1");
    auto section = page.section_by_title("Section 4");
    ASSERT_EQ(section.title(), "Section 4");
    ASSERT_EQ(section.text(), "");
    ASSERT_EQ(section.sections().size(), 2);
}

TEST_F(TestHtmlFormatExtracts, Subsubsection) {
    auto page = wiki->page("Test_1");
    auto section = page.section_by_title("Section 4.2.2");
    ASSERT_EQ(section.title(), "Section 4.2.2");
    ASSERT_EQ(section.text(), "<p><b>Text for section 4.2.2</b>\n\n\n</p>");
    std::string expected_repr =
        "Section: Section 4.2.2 (3):\n"
        "<p><b>Text for section 4.2.2</b>\n\n\n</p>\n"
        "Subsections (0):\n";
    ASSERT_EQ(section.repr(), expected_repr);
    ASSERT_EQ(section.sections().size(), 0);
}

TEST_F(TestHtmlFormatExtracts, SubsectionByTitleReturnLast) {
    auto page = wiki->page("Test_Nested");
    auto section = page.section_by_title("Subsection B");
    ASSERT_EQ(section.title(), "Subsection B");
    ASSERT_EQ(section.text(), "<p><b>Text for section 3.B</b>\n\n\n</p>");
    ASSERT_EQ(section.sections().size(), 0);
}

TEST_F(TestHtmlFormatExtracts, SubsectionsByTitle) {
    auto page = wiki->page("Test_Nested");
    auto sections = page.sections_by_title("Subsection B");
    ASSERT_EQ(sections.size(), 3);
    std::vector<std::string> expected = {
        "<p><b>Text for section 1.B</b>\n\n\n</p>",
        "<p><b>Text for section 2.B</b>\n\n\n</p>",
        "<p><b>Text for section 3.B</b>\n\n\n</p>"
    };
    std::vector<std::string> results;
    for (const auto& s : sections)
        results.push_back(s.text());
    ASSERT_EQ(results, expected);
}

TEST_F(TestHtmlFormatExtracts, PageText) {
    auto page = wiki->page("Test_1");
    std::string expected =
        "<p><b>Summary</b> text\n\n</p>\n\n"
        "<h2>Section 1</h2>\n"
        "<p>Text for section 1</p>\n\n"
        "<h3>Section 1.1</h3>\n"
        "<p><b>Text for section 1.1</b>\n\n\n</p>\n\n"
        "<h3>Section 1.2</h3>\n"
        "<p><b>Text for section 1.2</b>\n\n\n</p>\n\n"
        "<h2>Section 2</h2>\n"
        "<p><b>Text for section 2</b>\n\n\n</p>\n\n"
        "<h2>Section 3</h2>\n"
        "<p><b>Text for section 3</b>\n\n\n</p>\n\n"
        "<h2>Section 4</h2>\n"
        "<h3>Section 4.1</h3>\n"
        "<p><b>Text for section 4.1</b>\n\n\n</p>\n\n"
        "<h3>Section 4.2</h3>\n"
        "<p><b>Text for section 4.2</b>\n\n\n</p>\n\n"
        "<h4>Section 4.2.1</h4>\n"
        "<p><b>Text for section 4.2.1</b>\n\n\n</p>\n\n"
        "<h4>Section 4.2.2</h4>\n"
        "<p><b>Text for section 4.2.2</b>\n\n\n</p>\n\n"
        "<h2>Section 5</h2>\n"
        "<p><b>Text for section 5</b>\n\n\n</p>\n\n"
        "<h3>Section 5.1</h3>\n"
        "<p>Text for section 5.1\n\n\n</p>";
    ASSERT_EQ(page.text(), expected);
}

TEST_F(TestHtmlFormatExtracts, WithErroneousEdit) {
    auto page = wiki->page("Test_Edit");
    auto section = page.section_by_title("Section with Edit");
    ASSERT_EQ(section.title(), "Section with Edit");
    std::string expected =
        "<p><b>Summary</b> text\n\n</p>\n\n"
        "<h2>Section 1</h2>\n"
        "<p>Text for section 1</p>\n\n"
        "<h3>Section with Edit</h3>\n"
        "<p>Text for section with edit\n\n\n</p>";
    ASSERT_EQ(page.text(), expected);
}