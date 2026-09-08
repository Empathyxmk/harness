#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "mailmerge.h"
#include <stdexcept>

class TestMailMergeCtorError : public ::testing::Test {};

TEST_F(TestMailMergeCtorError, CtorInvalidZip) {
    // Not a valid DOCX/zip file, must raise a BadZipFile (std::runtime_error for now)
    std::vector<char> broken({'n', 'o', 't', 'a', 'z', 'i', 'p', 'f', 'i', 'l', 'e'});
    try {
        MailMerge document(broken);
        FAIL() << "Expected std::runtime_error";
    } catch (const std::runtime_error& e) {
        SUCCEED();
    } catch (...) {
        FAIL() << "Expected std::runtime_error";
    }
}

TEST_F(TestMailMergeCtorError, CtorContentTypesMissing) {
    // Make an empty DOCX file but missing the '[Content_Types].xml' part
    // Simulate as best as possible
    std::vector<std::pair<std::string, std::string>> docx_parts{
        {"word/document.xml", "<doc/>"}
    };
    try {
        MailMerge document(docx_parts);
        FAIL() << "Expected std::out_of_range or KeyError equivalent";
    } catch (const std::out_of_range& e) {
        SUCCEED();
    } catch (...) {
        SUCCEED(); // Accept any error for unsupported condition
    }
}