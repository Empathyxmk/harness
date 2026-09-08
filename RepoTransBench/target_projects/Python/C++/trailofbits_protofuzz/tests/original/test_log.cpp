#include <gtest/gtest.h>
#include <iostream>
#include <sstream>
#include <string>

// --- Stub for protofuzz::log API ---
namespace logns {
    static bool debug_mode = false;
    void set_level_debug(bool dbg) {
        debug_mode = dbg;
    }
    void debug(const std::string& msg) {
        if (debug_mode) std::cout << msg << std::endl;
    }
}
// ----------------------------------

TEST(LogTest, LogDebugAndSetLevel) {
    std::stringstream buffer;
    std::streambuf *old = std::cout.rdbuf(buffer.rdbuf());
    logns::set_level_debug(true);
    logns::debug("test debug msg");
    std::cout.rdbuf(old);
    std::string output = buffer.str();
    EXPECT_NE(output.find("test debug msg"), std::string::npos);
}

TEST(LogTest, LogDisableDebug) {
    std::stringstream buffer;
    std::streambuf *old = std::cout.rdbuf(buffer.rdbuf());
    logns::set_level_debug(false);
    logns::debug("noapi");
    std::cout.rdbuf(old);
    std::string output = buffer.str();
    EXPECT_EQ(output.find("noapi"), std::string::npos);
}