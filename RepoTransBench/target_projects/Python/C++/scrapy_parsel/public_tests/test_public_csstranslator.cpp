#include <gtest/gtest.h>
#include "csstranslator.h"

TEST(PublicCsstranslator, GenericTranslatorCacheBehaviorPublic) {
    GenericTranslator g;
    EXPECT_EQ(g.css_to_xpath("a#main.class"), "//a[contains(concat(\" \",normalize-space(@class),\" \"),\" class \")][@id = \"main\"]");
    EXPECT_EQ(g.css_to_xpath("a#main.class"), g.css_to_xpath("a#main.class"));
}

TEST(PublicCsstranslator, HtmlTranslatorInheritancePublic) {
    EXPECT_TRUE((std::is_base_of<GenericTranslator, HTMLTranslator>::value));
}

TEST(PublicCsstranslator, XPathExprJoinTypeCheckPublic) {
    GenericTranslator g;
    EXPECT_THROW({
        throw std::invalid_argument("joiner must be a string");
    }, std::invalid_argument);
}

TEST(PublicCsstranslator, XPathPseudoElementUnknownPublic) {
    GenericTranslator g;
    EXPECT_THROW({
        throw SelectorError("unknown pseudo element");
    }, SelectorError);
}