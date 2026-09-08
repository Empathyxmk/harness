#include <gtest/gtest.h>
#include "pynubank/cli.h"

TEST(PublicCliTest, DisplaysHelp) {
    Cli cli;
    std::ostringstream out;
    bool helpShown = cli.parseArguments({"prog", "--help"}, out);
    EXPECT_TRUE(helpShown);
}