#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "shortuuid/cli.h"

static std::pair<std::string, std::string> run_cli_args(const std::vector<std::string>& args) {
    std::stringstream out, err;
    std::streambuf* oldout = std::cout.rdbuf(out.rdbuf());
    std::streambuf* olderr = std::cerr.rdbuf(err.rdbuf());
    int rc = cli_main(args);
    std::cout.rdbuf(oldout);
    std::cerr.rdbuf(olderr);
    return {out.str(), err.str()};
}

TEST(PublicCLIArgparse, InvalidCommand) {
    auto res = run_cli_args({"notacommand"});
    std::string text = res.first + res.second;
    for (char& c : text) c = tolower(c);
    EXPECT_TRUE(
        text.find("invalid") != std::string::npos ||
        text.find("unknown") != std::string::npos ||
        text.find("unrecognized") != std::string::npos
    );
}

TEST(PublicCLIArgparse, DecodeBadString) {
    auto res = run_cli_args({"decode", "333BADSHORTuuid!"});
    std::string text = res.first + res.second;
    for (char& c : text) c = tolower(c);
    EXPECT_TRUE(
        text.find("error") != std::string::npos ||
        text.find("invalid") != std::string::npos ||
        text.empty()
    );
}

TEST(PublicCLIArgparse, EncodingTooFewArgs) {
    auto res = run_cli_args({"encode"});
    std::string text = res.first + res.second;
    for (char& c : text) c = tolower(c);
    EXPECT_TRUE(
        text.find("usage") != std::string::npos ||
        text.find("argument") != std::string::npos ||
        text.find("error") != std::string::npos
    );
}