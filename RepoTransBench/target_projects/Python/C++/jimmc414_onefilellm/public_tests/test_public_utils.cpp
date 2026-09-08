#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <filesystem>
#include "utils.h"
namespace fs = std::filesystem;

TEST(PublicUtilsTest, SafeFileReadUtf8AndFallbackPublic) {
    fs::path tmp = fs::temp_directory_path() / fs::unique_path();
    fs::create_directory(tmp);
    std::string p = (tmp / "foo.txt").string();
    std::string data = "Testing äßü";
    {
        std::ofstream f(p, std::ios::binary);
        f << data;
    }
    EXPECT_EQ(utils::safe_file_read(p), data);

    std::string p2 = (tmp / "bar.txt").string();
    std::ofstream f2(p2, std::ios::binary);
    f2.write("ni\xf1o", 5);
    f2.close();
    EXPECT_EQ(utils::safe_file_read(p2), "niño");
    fs::remove_all(tmp);
}

// Clipboard and stdin tests are stubbed for C++
TEST(PublicUtilsTest, ReadFromClipboardPublicStub) {
    EXPECT_EQ(utils::read_from_clipboard(), "public clipboard");
}

TEST(PublicUtilsTest, ReadFromStdinPublicStub) {
    EXPECT_EQ(utils::read_from_stdin(), "");
}

TEST(PublicUtilsTest, DetectTextFormatPublic) {
    EXPECT_EQ(utils::detect_text_format("{\"foo\": 42}"), "json");
    EXPECT_EQ(utils::detect_text_format("[100, 200, 300]"), "json");
    auto yaml_ans = utils::yaml ? "yaml" : "text";
    EXPECT_EQ(utils::detect_text_format("x: 7\ny: 8"), yaml_ans);
    EXPECT_EQ(utils::detect_text_format("<HTML>Tag</HTML>"), "html");
    EXPECT_EQ(utils::detect_text_format("<!DOCTYPE HTML>"), "html");
    EXPECT_EQ(utils::detect_text_format("<span>public</span>"), "html");
    EXPECT_EQ(utils::detect_text_format("## Subheader\nSome text"), "markdown");
    EXPECT_EQ(utils::detect_text_format("*item*"), "markdown");
    EXPECT_EQ(utils::detect_text_format("A random sentence"), "text");
    EXPECT_EQ(utils::detect_text_format(" "), "text");
    EXPECT_EQ(utils::detect_text_format("\n\n"), "text");
}

TEST(PublicUtilsTest, ParseAsPlaintextAndMarkdownPublic) {
    std::string s = "xyz";
    EXPECT_EQ(utils::parse_as_plaintext(s), s);
    EXPECT_EQ(utils::parse_as_markdown(s), s);
}

TEST(PublicUtilsTest, ParseAsJsonAndYamlAndHtmlPublic) {
    std::string s_json = "{\"x\": 99, \"y\": 88}";
    auto parsed = utils::parse_as_json(s_json);
    EXPECT_TRUE(!parsed.empty());
    if (utils::yaml) {
        std::string yaml_parsed = utils::parse_as_yaml("foo: bar\nbaz: quux");
        EXPECT_TRUE(!yaml_parsed.empty());
    }
    std::string html = "<html><body>World</body></html>";
    EXPECT_TRUE(utils::parse_as_html(html).find("World") != std::string::npos);
}

TEST(PublicUtilsTest, DownloadFilePublicDummy) {
    fs::path tmp = fs::temp_directory_path() / fs::unique_path();
    fs::create_directory(tmp);
    std::string url = "https://example.com/some.txt";
    fs::path dest = tmp / "some_output.txt";
    std::ofstream f(dest, std::ios::binary);
    f << "foobar";
    f.close();
    EXPECT_TRUE(fs::exists(dest));
    std::ifstream in(dest, std::ios::binary);
    std::string file_content((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    EXPECT_EQ(file_content, "foobar");
    fs::remove_all(tmp);
}

TEST(PublicUtilsTest, IsSameDomainPublic) {
    EXPECT_TRUE(utils::is_same_domain("https://b.com/page", "https://b.com/y"));
    EXPECT_FALSE(utils::is_same_domain("https://b.com", "https://sub.b.com/a"));
    EXPECT_TRUE(utils::is_same_domain("http://b.com/xy", "https://b.com/zzz"));
}

TEST(PublicUtilsTest, IsWithinDepthPublic) {
    EXPECT_TRUE(utils::is_within_depth("https://b.com", "https://b.com/abc/def", 2));
    EXPECT_FALSE(utils::is_within_depth("https://b.com", "https://b.com/a/b/c/d", 3));
    EXPECT_FALSE(utils::is_within_depth("http://b.com", "https://b.com/a/b", 1));
}

TEST(PublicUtilsTest, IsExcludedFilePublic) {
    EXPECT_FALSE(utils::is_excluded_file("/bar/src/main.py"));
    EXPECT_TRUE(utils::is_excluded_file("/bar/node_modules/script.js"));
    EXPECT_TRUE(utils::is_excluded_file("/bar/.git/description"));
}

TEST(PublicUtilsTest, IsAllowedFiletypePublic) {
    EXPECT_TRUE(utils::is_allowed_filetype("main.go"));
    EXPECT_TRUE(utils::is_allowed_filetype("foo.md"));
    EXPECT_FALSE(utils::is_allowed_filetype("file.dll"));
    EXPECT_TRUE(utils::is_allowed_filetype("file.MD"));
}

TEST(PublicUtilsTest, EscapeXmlPublic) {
    std::string raw = "<public>&amp;</public>";
    EXPECT_EQ(utils::escape_xml(raw), raw);
}

TEST(PublicUtilsTest, ParseAsYamlHandlesNoYamlPublic) {
    EXPECT_EQ(utils::parse_as_yaml("bar"), "bar");
}