#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include <iostream>
#include <vector>
#include "shortuuid/cli.h"
#include "shortuuid/shortuuid.h"

// Simulate the CLI by calling cli_main() with appropraite arguments and redirecting std::cout.

TEST(CLI, EncodeAndDecode) {
    // Test encode
    std::string uuid_val = ShortUUID().uuid();
    std::vector<std::string> args_encode = { "encode", uuid_val };
    std::stringstream outbuf;
    std::streambuf* old_cout = std::cout.rdbuf(outbuf.rdbuf());
    int rc_encode = cli_main(args_encode);
    std::cout.rdbuf(old_cout);
    std::string out_encode = outbuf.str();
    out_encode.erase(out_encode.find_last_not_of(" \t\n\r") + 1);

    EXPECT_EQ(rc_encode, 0);
    EXPECT_FALSE(out_encode.empty());
    EXPECT_GT(out_encode.size(), 0);

    // Test decode
    std::vector<std::string> args_decode = { "decode", out_encode };
    outbuf.str("");
    old_cout = std::cout.rdbuf(outbuf.rdbuf());
    int rc_decode = cli_main(args_decode);
    std::cout.rdbuf(old_cout);
    std::string out_decode = outbuf.str();
    out_decode.erase(out_decode.find_last_not_of(" \t\n\r") + 1);

    // Should be a valid UUID (use ShortUUID to check parse)
    EXPECT_NO_THROW({
        auto uval = ShortUUID().decode(out_decode);
        (void)uval;
    });
}

TEST(CLI, DecodeLegacy) {
    std::string uuid_val = ShortUUID().uuid();
    std::string encoded = ShortUUID().encode(uuid_val);
    std::reverse(encoded.begin(), encoded.end());
    std::vector<std::string> args = { "decode", encoded, "--legacy" };
    std::stringstream outbuf;
    std::streambuf* old_cout = std::cout.rdbuf(outbuf.rdbuf());
    int rc = cli_main(args);
    std::cout.rdbuf(old_cout);
    std::string output = outbuf.str();
    output.erase(output.find_last_not_of(" \t\n\r") + 1);

    EXPECT_EQ(rc, 0);
    EXPECT_NO_THROW({
        auto uval = ShortUUID().decode(output);
        (void)uval;
    });
}

TEST(CLI, NoFn) {
    std::vector<std::string> args = {}; // No subcommand, generates a uuid.
    std::stringstream outbuf;
    std::streambuf* old_cout = std::cout.rdbuf(outbuf.rdbuf());
    int rc = cli_main(args);
    std::cout.rdbuf(old_cout);
    std::string output = outbuf.str();
    output.erase(output.find_last_not_of(" \t\n\r") + 1);

    EXPECT_EQ(rc, 0);
    EXPECT_FALSE(output.empty());
}