#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicNamespaceAndExtractFormatTest, NamespaceEnumMembersPublic) {
    EXPECT_EQ(Namespace::TALK, 1);
    EXPECT_EQ(Namespace::PROJECT, 4);
    EXPECT_EQ(Namespace::FILE, 6);
    EXPECT_EQ(Namespace::PORTAL, 100);
    EXPECT_EQ(Namespace::GADGET_TALK, 2301);
}

TEST(PublicNamespaceAndExtractFormatTest, ExtractFormatEnumMembersReversed) {
    EXPECT_EQ(ExtractFormat::HTML, 2);
    EXPECT_EQ(ExtractFormat::WIKI, 1);
}

TEST(PublicNamespaceAndExtractFormatTest, Namespace2IntEnumOther) {
    EXPECT_EQ(namespace2int(Namespace::FILE), 6);
    EXPECT_EQ(namespace2int(Namespace::PORTAL), 100);
}

TEST(PublicNamespaceAndExtractFormatTest, Namespace2IntDifferentInt) {
    EXPECT_EQ(namespace2int(99), 99);
    EXPECT_EQ(namespace2int(6), 6);
}

TEST(PublicNamespaceAndExtractFormatTest, InvalidNamespace2IntOther) {
    EXPECT_EQ(namespace2int(Namespace::PROJECT_TALK), static_cast<int>(Namespace::PROJECT_TALK));
}

TEST(PublicNamespaceAndExtractFormatTest, ExtractFormatReprOther) {
    EXPECT_STREQ(ExtractFormatNames::HTML, "HTML");
    EXPECT_STREQ(ExtractFormatNames::WIKI, "WIKI");
}