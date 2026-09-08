#include <gtest/gtest.h>
#include "pdf_redactor.hpp"
#include <sstream>
#include <vector>
#include <regex>
#include <string>

TEST(PublicRedactorTest, BasicRedaction) {
    std::string pdf_str = "%PDF-1.4\n% Public test: secret12345 replaced\nxyz 654-32-1987 zyx\n%%EOF";
    std::stringstream pdf_in(pdf_str);
    pdf_redactor::RedactorOptions options;
    options.content_filters = {
        {std::regex("\\b654-32-1987\\b"), [](const std::smatch&) { return std::string("[REDACTED-ID]"); }}
    };
    std::stringstream pdf_out;
    pdf_redactor::redactor(options, &pdf_in, &pdf_out);
    EXPECT_NE(pdf_out.str().find("[REDACTED-ID]"), std::string::npos);
}

TEST(PublicRedactorTest, UnicodeFilter) {
    std::string pdf_str = "%PDF-1.4\nUnusual symbol: §\nID 88-99-7766\n%%EOF";
    std::stringstream pdf_in(pdf_str);
    pdf_redactor::RedactorOptions options;
    options.content_filters = {
        {std::regex("\\b88-99-7766\\b"), [](const std::smatch&) { return std::string("<REMOVED>"); }}
    };
    std::stringstream out;
    pdf_redactor::redactor(options, &pdf_in, &out);
    EXPECT_NE(out.str().find("<REMOVED>"), std::string::npos);
}

TEST(PublicRedactorTest, MultilineFilter) {
    std::string pdf_str = "%PDF-1.4\nFirstLine\nID: 222-33-4444\nSecondLine\n%%EOF";
    std::stringstream pdf_in(pdf_str);
    pdf_redactor::RedactorOptions options;
    options.content_filters = {
        {std::regex("222-33-4444"), [](const std::smatch&) { return std::string("*****"); }}
    };
    std::stringstream out;
    pdf_redactor::redactor(options, &pdf_in, &out);
    EXPECT_NE(out.str().find("*****"), std::string::npos);
}