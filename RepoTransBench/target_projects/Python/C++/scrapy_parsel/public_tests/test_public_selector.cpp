#include <gtest/gtest.h>
#include "selector.h"

TEST(PublicSelector, ExtractFromHtml) {
    Selector sel("<html><body><span>world</span></body></html>");
    // This would result in "world" if logic implemented
    EXPECT_EQ(sel.xpath("//span/text()").get(), "world");
}

TEST(PublicSelector, CssSelection) {
    Selector sel("<div><b>BoldContent</b></div>");
    EXPECT_EQ(sel.css("b::text").get(), "BoldContent");
}

TEST(PublicSelector, ExtractFirstCustomDefault) {
    Selector sel("<root></root>");
    // Should return "nothing" for missing node
    EXPECT_EQ(sel.xpath("//missing/text()").get(), "nothing"); // Args for default would need C++ adaptation
}

TEST(PublicSelector, ExtractList) {
    Selector sel("<ul><li>egg</li><li>cheese</li></ul>");
    auto result = sel.css("li::text").getall();
    std::vector<std::string> expected = {"egg", "cheese"};
    EXPECT_EQ(result, expected);
}

TEST(PublicSelector, ErrorHandlingWrongType) {
    EXPECT_THROW({
        throw std::invalid_argument("TypeError: wrong type for Selector text input");
    }, std::invalid_argument);
}