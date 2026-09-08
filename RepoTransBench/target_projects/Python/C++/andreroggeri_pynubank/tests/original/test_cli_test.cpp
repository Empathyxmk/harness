#include <gtest/gtest.h>
#include "pynubank/cli.h"

TEST(CliTest, HelpOptionReturnsHelp) {
    Cli cli;
    std::ostringstream out;
    bool helpShown = cli.parseArguments({"prog", "--help"}, out);
    EXPECT_TRUE(helpShown);
    EXPECT_NE(out.str().find("Usage:"), std::string::npos);
}

TEST(CliTest, InvalidOptionThrows) {
    Cli cli;
    std::ostringstream out;
    EXPECT_THROW(cli.parseArguments({"prog", "--not-an-option"}, out), CliException);
}