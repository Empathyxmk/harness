#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <iostream>
#include <sstream>
#include "shortuuid/cli.h"

TEST(CLIArgparse, InvalidCommand) {
    std::vector<std::string> args = { "bogus" };
    EXPECT_EXIT(cli_main(args), ::testing::ExitedWithCode(2), ".*"); // 2 is typical for argument error
}

TEST(CLIArgparse, EncodeNoUUID) {
    std::vector<std::string> args = { "encode" };
    EXPECT_EXIT(cli_main(args), ::testing::ExitedWithCode(2), ".*");
}

TEST(CLIArgparse, DecodeNoShortuuid) {
    std::vector<std::string> args = { "decode" };
    EXPECT_EXIT(cli_main(args), ::testing::ExitedWithCode(2), ".*");
}