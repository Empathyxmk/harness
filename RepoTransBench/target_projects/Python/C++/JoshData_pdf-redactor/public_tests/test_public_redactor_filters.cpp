#include <gtest/gtest.h>
#include "pdf_redactor.hpp"
#include <sstream>
#include <regex>

// Helper for callable replacement
std::string repl(const std::smatch&) { return "MASKED"; }

TEST(PublicRedactorFiltersTest, FilterCallableReplacement) {
    std::string pdf_str = "%PDF-1.4\nSSN 159-46-2879\n%%EOF";
    std::stringstream pdf_in(pdf_str);
    pdf_redactor::RedactorOptions options;
    options.content_filters = {
        {std::regex("\\d{3}-\\d{2}-\\d{4}"), repl}
    };
    std::stringstream pdf_out;
    pdf_redactor::redactor(options, &pdf_in, &pdf_out);
    EXPECT_NE(pdf_out.str().find("MASKED"), std::string::npos);
}

TEST(PublicRedactorFiltersTest, FilterNonCallableReplacement) {
    std::string pdf_str = "%PDF-1.4\nName: Angela Bailey\n%%EOF";
    std::stringstream pdf_in(pdf_str);
    pdf_redactor::RedactorOptions options;
    options.content_filters = {
        {std::regex("Angela Bailey"), [](const std::smatch&) { return std::string("AnonName"); }}
    };
    std::stringstream pdf_out;
    pdf_redactor::redactor(options, &pdf_in, &pdf_out);
    EXPECT_NE(pdf_out.str().find("AnonName"), std::string::npos);
}