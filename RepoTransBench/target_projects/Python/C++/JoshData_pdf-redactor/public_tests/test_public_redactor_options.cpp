#include <gtest/gtest.h>
#include "pdf_redactor.hpp"
#include <string>
#include <vector>
#include <map>

TEST(PublicRedactorOptionsTest, MetadataDefaults) {
    pdf_redactor::RedactorOptions options;
    options.metadata["Title"] = "PublicTitle";
    options.metadata["Subject"] = "PublicSubj";
    options.metadata["Author"] = "AuthorPerson";
    EXPECT_EQ(options.metadata["Title"], "PublicTitle");
    EXPECT_EQ(options.metadata["Subject"], "PublicSubj");
    EXPECT_EQ(options.metadata["Author"], "AuthorPerson");
}

TEST(PublicRedactorOptionsTest, OptionsFiltersList) {
    pdf_redactor::RedactorOptions options;
    options.content_filters = {
        {std::regex("\\d{2}-\\d{2}-\\d{4}"), [](const std::smatch&) { return std::string("REDACT"); }},
        {std::regex("SecretWord"), [](const std::smatch&) { return std::string("VisibleWord"); }}
    };
    EXPECT_EQ(options.content_filters.size(), 2);
    EXPECT_EQ(options.content_filters[1].first.mark_count(), std::regex("VisibleWord").mark_count());
}