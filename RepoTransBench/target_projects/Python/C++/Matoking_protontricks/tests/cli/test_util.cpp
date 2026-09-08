#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <stdexcept>
#include <cstdio>

static int logger_handlers = 0;
void enable_logging() { if (logger_handlers < 2) logger_handlers = 2; }
int get_logger_handlers_count() { return logger_handlers; }

void exit_with_error(const std::string& msg, bool desktop = false) {
    if (desktop) { throw std::runtime_error("Desktop error shown: " + msg); }
    throw std::runtime_error(msg);
}

struct GuiProvider {
    std::vector<std::string> args;
    std::map<std::string, std::string> kwargs;
} gui_provider;

std::string log_file_text = "Found Steam directory";
std::string& _get_log_file_path() {
    static std::string path = "/tmp/protontricks_testlog.txt";
    return path;
}
void _delete_log_file() { log_file_text.clear(); }

TEST(CLIUtil, EnableLoggingIsIdempotent) {
    logger_handlers = 0;
    EXPECT_EQ(get_logger_handlers_count(), 0);
    enable_logging();
    EXPECT_EQ(get_logger_handlers_count(), 2);
    enable_logging();
    EXPECT_EQ(get_logger_handlers_count(), 2);
}

TEST(CLIUtil, ExitWithErrorNoLogFile) {
    _delete_log_file();
    try {
        exit_with_error("Test error", true);
        FAIL();
    } catch (const std::runtime_error& e) {
        std::string msg(e.what());
        ASSERT_TRUE(msg.find("Desktop error shown: Test error") != std::string::npos);
    }
}

TEST(CLIUtil, LogFileCleanup) {
    log_file_text = "Found Steam directory";
    ASSERT_TRUE(log_file_text.find("Found Steam directory") != std::string::npos);
    _delete_log_file();
    ASSERT_EQ(log_file_text, "");
    // No error if already missing
    _delete_log_file();
}