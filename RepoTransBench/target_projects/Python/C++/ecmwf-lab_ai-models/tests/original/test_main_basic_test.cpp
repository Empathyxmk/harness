#include <gtest/gtest.h>
#include <stdexcept>
#include <sstream>
#include "src/ai_models/main.h"

// Helper capturing stdout
class OutputCapture {
    std::stringstream buffer;
    std::streambuf* old;
public:
    OutputCapture() : old(std::cout.rdbuf(buffer.rdbuf())) {}
    ~OutputCapture() { std::cout.rdbuf(old); }
    std::string str() { return buffer.str(); }
};

TEST(MainTests, MainHelp) {
    OutputCapture cap;
    try {
        std::vector<std::string> args = {"--help"};
        _main(args);
        FAIL() << "Should have thrown SystemExit";
    } catch(const SystemExitException&) {
        std::string out = cap.str();
        EXPECT_TRUE(out.find("usage:") != std::string::npos ||
                    out.find("Usage:") != std::string::npos);
    }
}

TEST(MainTests, MainModels) {
    OutputCapture cap;
    set_available_models([](){ return std::vector<std::string>{"foo", "bar"}; });
    set_exit_handler([](int code){ throw SystemExitException(); });
    try {
        std::vector<std::string> args = {"--models"};
        _main(args);
        FAIL() << "Should have thrown SystemExit";
    } catch (const SystemExitException&) {
        std::string out = cap.str();
        EXPECT_TRUE(out.find("foo") != std::string::npos ||
                    out.find("bar") != std::string::npos);
    }
}

TEST(MainTests, MainVerboseDebug) {
    set_available_models([](){ return std::vector<std::string>{"foo"}; });
    set_available_outputs([](){ return std::vector<std::string>{"file"}; });
    set_available_inputs([](){ return std::vector<std::string>{"mars"}; });
    std::vector<std::string> args = {"--verbose"};
    EXPECT_NO_THROW(_main(args));
}