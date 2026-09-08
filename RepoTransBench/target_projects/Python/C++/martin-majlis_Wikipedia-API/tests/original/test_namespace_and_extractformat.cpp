#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

// Spot check a few enum values
TEST(NamespaceAndExtractFormatTest, NamespaceEnumMembers) {
    EXPECT_EQ(Namespace::MAIN, 0);
    EXPECT_EQ(Namespace::USER, 2);
    EXPECT_EQ(Namespace::CATEGORY, 14);
    EXPECT_EQ(Namespace::BOOK, 108);
    EXPECT_EQ(Namespace::GADGET, 2300);
}

TEST(NamespaceAndExtractFormatTest, ExtractFormatEnumMembers) {
    EXPECT_EQ(ExtractFormat::WIKI, 1);
    EXPECT_EQ(ExtractFormat::HTML, 2);
}

TEST(NamespaceAndExtractFormatTest, Namespace2IntWithEnum) {
    EXPECT_EQ(namespace2int(Namespace::MAIN), 0);
    EXPECT_EQ(namespace2int(Namespace::CATEGORY), 14);
}

TEST(NamespaceAndExtractFormatTest, Namespace2IntWithInt) {
    EXPECT_EQ(namespace2int(42), 42);
    EXPECT_EQ(namespace2int(0), 0);
}

TEST(NamespaceAndExtractFormatTest, InvalidNamespace2Int) {
    // Should not raise
    EXPECT_EQ(namespace2int(Namespace::USER_TALK), static_cast<int>(Namespace::USER_TALK));
}

TEST(NamespaceAndExtractFormatTest, ExtractFormatRepr) {
    EXPECT_STREQ(ExtractFormatNames::WIKI, "WIKI");
    EXPECT_STREQ(ExtractFormatNames::HTML, "HTML");
}