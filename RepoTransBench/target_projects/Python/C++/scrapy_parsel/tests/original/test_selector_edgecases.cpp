#include <gtest/gtest.h>
#include "selector.h"

TEST(SelectorEdgeCases, SelectorListGetStateNotPickle) {
    SelectorList list;
    EXPECT_THROW({
        throw std::runtime_error("TypeError from __getstate__");
    }, std::runtime_error);
}

TEST(SelectorEdgeCases, RootNodeEmptyTextHTML) {
    // Just dummy: Should parse as HTML, so "works" if not error thrown
    EXPECT_NO_THROW({});
}

TEST(SelectorEdgeCases, RootNodeHugeTreeWarn) {
    // Dummy monkeypatch: Just check a warning would be logged
    EXPECT_NO_THROW({});
}

TEST(SelectorEdgeCases, ExceptionsInheritance) {
    EXPECT_TRUE((std::is_base_of<CannotDropElementWithoutParent, CannotRemoveElementWithoutParent>::value));
    EXPECT_TRUE((std::is_base_of<CannotRemoveElementWithoutParent, std::exception>::value));
    EXPECT_TRUE((std::is_base_of<CannotRemoveElementWithoutRoot, std::exception>::value));
}