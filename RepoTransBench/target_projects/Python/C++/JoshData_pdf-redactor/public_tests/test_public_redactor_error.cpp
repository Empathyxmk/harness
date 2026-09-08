#include <gtest/gtest.h>
#include "pdf_redactor.hpp"
#include <sstream>
#include <exception>

TEST(PublicRedactorErrorTest, InvalidFilterTypeError) {
    pdf_redactor::RedactorOptions options;
    // Emulate: (12345, "foo") which is invalid in C++ context
    // We'll simulate by throwing in redactor if called with unsupported filter
    try {
        options.content_filters.push_back({std::regex(""), nullptr});
        std::stringstream in, out;
        pdf_redactor::redactor(options, &in, &out);
        FAIL() << "Expected exception";
    } catch (const std::exception&) {
        SUCCEED();
    } catch (...) {
        SUCCEED();
    }
}

TEST(PublicRedactorErrorTest, InvalidOutputStream) {
    pdf_redactor::RedactorOptions options;
    options.content_filters = {};
    // Emulate: output stream is nullptr, should throw
    try {
        std::stringstream in;
        pdf_redactor::redactor(options, &in, nullptr);
        FAIL() << "Expected exception";
    } catch (const std::exception&) {
        SUCCEED();
    } catch (...) {
        SUCCEED();
    }
}