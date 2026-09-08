#include <gtest/gtest.h>
#include "pdf_redactor.hpp"
#include <string>
#include <vector>
#include <functional>
#include <filesystem>
#include <fstream>
#include <regex>
#include <cstdio>
#include <cstdlib>
#include <memory>

// Helper: mimic Python RedactFixture as c++ class
class RedactFixture {
    std::string input_path;
    pdf_redactor::RedactorOptions &options;
    std::string redacted_path;
    std::ifstream input_file;
    std::ofstream redacted_file;
public:
    RedactFixture(const std::string& inpath, pdf_redactor::RedactorOptions& opts)
        : input_path(inpath), options(opts) {}

    const std::string& getRedactedPath() const { return redacted_path; }

    void enter() {
        input_file.open(input_path, std::ios::binary);
        options.input_stream = &input_file;
        char path_template[L_tmpnam];
        tmpnam(path_template);
        redacted_path = path_template;
        redacted_path += ".pdf";
        redacted_file.open(redacted_path, std::ios::binary);
        options.output_stream = &redacted_file;
        pdf_redactor::redactor(options);
        redacted_file.close();
    }
    void exit() {
        input_file.close();
        redacted_file.close();
        std::remove(redacted_path.c_str());
    }
};

std::string pdf_to_text(const std::string& fn) {
    std::string cmd = "pdftotext \"" + fn + "\" -";
    std::string result;
    std::array<char, 4096> buffer;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"), pclose);
    if (!pipe) throw std::runtime_error("popen failed");
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

std::string pdf_to_html(const std::string& fn) {
    std::string cmd = "pdftohtml -stdout \"" + fn + "\"";
    std::string result;
    std::array<char, 4096> buffer;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"), pclose);
    if (!pipe) throw std::runtime_error("popen failed");
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

TEST(RedactorTest, TextSSNs) {
    // You must provide test-ssns.pdf in the root directory for this test.
    std::string fixture_path = "./test-ssns.pdf";
    pdf_redactor::RedactorOptions options;
    options.content_filters = {
        {std::regex("[−–—~‐]"), [](const std::smatch&) { return std::string("-"); }},
        {std::regex("(?<!\\d)(?!666|000|9\\d{2})([OoIli0-9]{3})([\\s-]?)(?!00)([OoIli0-9]{2})\\2(?!0{4})([OoIli0-9]{4})(?!\\d)"),
         [](const std::smatch&) { return std::string("XXX-XX-XXXX"); }}
    };
    RedactFixture fx(fixture_path, options);
    fx.enter();
    std::string text = pdf_to_text(fx.getRedactedPath());
    EXPECT_NE(text.find("Here are some fake SSNs"), std::string::npos);
    EXPECT_NE(text.find("XXX-XX-XXXX"), std::string::npos);
    fx.exit();
}

TEST(RedactorTest, Metadata) {
    std::string fixture_path = "./test-ssns.pdf";
    pdf_redactor::RedactorOptions options;
    options.metadata_filters = {
        {"Title", {[](const std::string& value) { return std::regex_replace(value, std::regex("test"), "sentinel"); }}},
        {"Subject", {[](const std::string& value) { return std::string(value.rbegin(), value.rend()); }}},
        {"DEFAULT", {[](const std::string& value) { return std::string(); }}}
    };
    RedactFixture fx(fixture_path, options);
    fx.enter();
    std::string cmd = "pdfinfo \"" + fx.getRedactedPath() + "\"";
    FILE* pipe = popen(cmd.c_str(), "r");
    ASSERT_TRUE(pipe != nullptr);
    char buffer[8192];
    std::string metadata;
    while (fgets(buffer, sizeof(buffer), pipe)) {
        metadata += buffer;
    }
    pclose(pipe);
    EXPECT_NE(metadata.find("this is a sentinel"), std::string::npos);
    EXPECT_NE(metadata.find("FDP a si"), std::string::npos);
    EXPECT_EQ(metadata.find("CreationDate"), std::string::npos);
    EXPECT_EQ(metadata.find("LibreOffice"), std::string::npos);
    fx.exit();
}

TEST(RedactorTest, XMP) {
    std::string fixture_path = "./test-ssns.pdf";
    pdf_redactor::RedactorOptions options;
    options.metadata_filters = {
        {"DEFAULT", {[](const std::string& value) { return std::string(); }}}
    };
    // For the actual test: We'll simulate xmp_filter, but focusing on if the field is replaced.
    // In this stub, just check the system call's output.
    RedactFixture fx(fixture_path, options);
    fx.enter();
    std::string cmd = "pdfinfo -meta \"" + fx.getRedactedPath() + "\"";
    FILE* pipe = popen(cmd.c_str(), "r");
    ASSERT_TRUE(pipe != nullptr);
    char buffer[8192];
    std::string metadata;
    while (fgets(buffer, sizeof(buffer), pipe)) {
        metadata += buffer;
    }
    pclose(pipe);
    EXPECT_NE(metadata.find("Sentinel"), std::string::npos);
    EXPECT_EQ(metadata.find("Writer"), std::string::npos);
    fx.exit();
}

TEST(RedactorTest, Link) {
    std::string fixture_path = "./test-ssns.pdf";
    pdf_redactor::RedactorOptions options;
    options.content_filters = {
        {std::regex(std::regex_replace(std::string("link to issue #13"), std::regex("([.^$|()\\[\\]{}*+?\\\\])"), "\\$1")),
         [](const std::smatch&) { return std::string("this link was removed"); }}
    };
    options.link_filters = {
        [](const std::string& href, void* annotation) { return std::string("https://www.google.com"); }
    };
    RedactFixture fx(fixture_path, options);
    fx.enter();
    std::string text = pdf_to_text(fx.getRedactedPath());
    EXPECT_EQ(text.find("link to issue #13"), std::string::npos);
    EXPECT_NE(text.find("this link was re#o#e#"), std::string::npos); // glyph replacements
    std::string html = pdf_to_html(fx.getRedactedPath());
    EXPECT_EQ(html.find("github"), std::string::npos);
    EXPECT_NE(html.find("href=\"https://www.google.com\""), std::string::npos);
    fx.exit();
}

// NOTE: No check on actual comment text/title due to extract tool absence (as in original python test)
TEST(RedactorTest, Comment) {
    std::string fixture_path = "./test-ssns.pdf";
    pdf_redactor::RedactorOptions options;
    options.content_filters = {
        {std::regex(std::regex_replace(std::string("I have a comment!"), std::regex("([.^$|()\\[\\]{}*+?\\\\])"), "\\$1")),
         [](const std::smatch&) { return std::string("all gone"); }},
        {std::regex(std::regex_replace(std::string("Unknown Author"), std::regex("([.^$|()\\[\\]{}*+?\\\\])"), "\\$1")),
         [](const std::smatch&) { return std::string("Some Person"); }}
    };
    RedactFixture fx(fixture_path, options);
    fx.enter();
    std::string text = pdf_to_text(fx.getRedactedPath());
    // We cannot extract comments (see Python test's TODO)
    fx.exit();
}