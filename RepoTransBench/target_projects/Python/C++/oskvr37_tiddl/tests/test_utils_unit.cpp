#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <cstdio>
#include <cstdlib>
#include <stdexcept>

// Stubs for utility functions if not implemented yet
namespace tiddl {

// Return True if `filename` has an extension in allowed_exts (e.g. ".mp3", ".flac" etc.), case-insensitive
bool has_allowed_extension(const std::string& filename, const std::vector<std::string>& allowed_exts) {
    for (const auto& ext : allowed_exts) {
        if (filename.size() >= ext.size()) {
            auto file_ext = filename.substr(filename.size() - ext.size());
            bool match = std::equal(file_ext.begin(), file_ext.end(),
                                    ext.begin(), ext.end(),
                                    [](char a, char b){ return std::tolower(a) == std::tolower(b); });
            if (match) return true;
        }
    }
    return false;
}

std::string strip_invalid_filename_chars(const std::string& input) {
    std::string output;
    for (auto c : input) {
        if (c == '\\' || c == '/' || c == ':' || c == '*' || c == '?' || c == '"' || c == '<' || c == '>' || c == '|')
            output += '_';
        else if (std::iscntrl(static_cast<unsigned char>(c)))
            output += '_';
        else
            output += c;
    }
    return output;
}

std::string basename_no_ext(const std::string& filename) {
    size_t last_slash = filename.find_last_of("/\\");
    std::string base = (last_slash == std::string::npos) ? filename : filename.substr(last_slash + 1);
    size_t last_dot = base.find_last_of(".");
    return (last_dot == std::string::npos) ? base : base.substr(0, last_dot);
}

// Dummy function to simulate safe cast, always returns true if input is valid int string
bool safe_int_cast(const std::string& str, int& out) {
    char* end;
    long val = std::strtol(str.c_str(), &end, 10);
    if (*end != '\0') return false;
    out = static_cast<int>(val);
    return true;
}

}

// ---- Actual Unit Tests ----

TEST(UtilsUnitTest, HasAllowedExtensionWorks) {
    std::vector<std::string> exts = {".mp3", ".flac"};
    EXPECT_TRUE(tiddl::has_allowed_extension("track01.mp3", exts));
    EXPECT_TRUE(tiddl::has_allowed_extension("track01.MP3", exts));
    EXPECT_TRUE(tiddl::has_allowed_extension("song.flac", exts));
    EXPECT_FALSE(tiddl::has_allowed_extension("image.jpg", exts));
    EXPECT_FALSE(tiddl::has_allowed_extension("no_extension", exts));
}

TEST(UtilsUnitTest, StripInvalidFilenameCharsReplacesBadChars) {
    std::string in1 = "song/name:*?.mp3";
    std::string in2 = "my<album>|\"test\".flac";
    EXPECT_EQ(tiddl::strip_invalid_filename_chars(in1), "song_name_____mp3");
    EXPECT_EQ(tiddl::strip_invalid_filename_chars(in2), "my_album__ _test__flac");
}

TEST(UtilsUnitTest, BasenameNoExtWorks) {
    EXPECT_EQ(tiddl::basename_no_ext("folder/sub/track01.mp3"), "track01");
    EXPECT_EQ(tiddl::basename_no_ext("track02.flac"), "track02");
    EXPECT_EQ(tiddl::basename_no_ext("noextfile"), "noextfile");
}

TEST(UtilsUnitTest, SafeIntCastParsesValidAndRejectsInvalid) {
    int n;
    EXPECT_TRUE(tiddl::safe_int_cast("42", n));
    EXPECT_EQ(n, 42);
    EXPECT_TRUE(tiddl::safe_int_cast("-10", n));
    EXPECT_EQ(n, -10);
    EXPECT_FALSE(tiddl::safe_int_cast("1.5", n));
    EXPECT_FALSE(tiddl::safe_int_cast("abc", n));
    EXPECT_FALSE(tiddl::safe_int_cast("", n));
    EXPECT_FALSE(tiddl::safe_int_cast("42x", n));
}