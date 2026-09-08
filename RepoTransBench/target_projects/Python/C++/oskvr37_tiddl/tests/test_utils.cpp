#include <gtest/gtest.h>
#include <string>
#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <stdexcept>

// If tiddl/utils.h is available and functional, include it.
// #include "tiddl/utils.h"

// --- MOCK/Stub function definitions for demonstration (REMOVE if real implementations exist!) ---
namespace tiddl {

bool endswith_case_insensitive(const std::string& str, const std::string& suffix) {
    if (suffix.size() > str.size()) return false;
    auto it_str = str.end() - suffix.size();
    for (size_t i = 0; i < suffix.size(); ++i) {
        if (std::tolower(*(it_str + i)) != std::tolower(suffix[i])) return false;
    }
    return true;
}

std::string tilde_expand(const std::string& path) {
    if (path.empty() || path[0] != '~') return path;
    const char* home = std::getenv("HOME");
    if (!home) throw std::runtime_error("HOME environment variable not set");
    return std::string(home) + path.substr(1);
}

std::string normalize_filename(const std::string& name) {
    std::string result = name;
    // Replace or remove forbidden characters on most file systems
    const std::string forbidden = "\\/:?\"<>|*";
    for (char& c : result) {
        if (forbidden.find(c) != std::string::npos) c = '_';
        if (static_cast<unsigned char>(c) < 32) c = '_'; // control characters
    }
    // Remove trailing dots/spaces
    while (!result.empty() && (result.back() == '.' || result.back() == ' ')) {
        result.pop_back();
    }
    return result;
}

} // namespace tiddl
// --- END STUBS ---

//------------------------
//       TEST SUITE
//------------------------

TEST(UtilsTest, EndswithCaseInsensitiveTrue) {
    EXPECT_TRUE(tiddl::endswith_case_insensitive("Track.FLAC", ".flac"));
    EXPECT_TRUE(tiddl::endswith_case_insensitive("Track.mp3", ".MP3"));
    EXPECT_TRUE(tiddl::endswith_case_insensitive("ReadMe.TXT", ".txt"));
}

TEST(UtilsTest, EndswithCaseInsensitiveFalse) {
    EXPECT_FALSE(tiddl::endswith_case_insensitive("music.ogg", ".flac"));
    EXPECT_FALSE(tiddl::endswith_case_insensitive("cover.jpeg", ".png"));
}

TEST(UtilsTest, TildeExpandBasic) {
    // Set HOME if not already set for test stability
    setenv("HOME", "/home/testuser", 1);
    EXPECT_EQ(tiddl::tilde_expand("~"), "/home/testuser");
    EXPECT_EQ(tiddl::tilde_expand("~/music"), "/home/testuser/music");
    EXPECT_EQ(tiddl::tilde_expand("relative/path"), "relative/path");
    EXPECT_EQ(tiddl::tilde_expand("/absolute/path"), "/absolute/path");
}

TEST(UtilsTest, TildeExpandThrowsIfNoHome) {
    char* old_home = getenv("HOME");
    unsetenv("HOME");
    EXPECT_THROW(tiddl::tilde_expand("~"), std::runtime_error);
    if (old_home) setenv("HOME", old_home, 1);
}

TEST(UtilsTest, NormalizeFilenameRemovesForbiddenChars) {
    EXPECT_EQ(tiddl::normalize_filename("invalid:/file*name?.mp3"), "invalid__file_name_.mp3");
    EXPECT_EQ(tiddl::normalize_filename(" clean_name .mp3"), " clean_name .mp3");
    EXPECT_EQ(tiddl::normalize_filename("spaces....   "), "spaces");
    EXPECT_EQ(tiddl::normalize_filename("\x01\x02name.txt"), "__name.txt");  // control chars
}

TEST(UtilsTest, NormalizeFilenameHandlesEmpty) {
    EXPECT_EQ(tiddl::normalize_filename(""), "");
}