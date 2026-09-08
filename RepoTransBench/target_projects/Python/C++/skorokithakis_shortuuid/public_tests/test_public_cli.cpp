#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include "shortuuid/cli.h"

static std::pair<std::string, std::string> run_cli_args(const std::vector<std::string>& args) {
    // Simulate CLI invocation, capturing stdout and stderr, using cli_main()
    std::stringstream out, err;
    std::streambuf* oldout = std::cout.rdbuf(out.rdbuf());
    std::streambuf* olderr = std::cerr.rdbuf(err.rdbuf());
    int rc = cli_main(args);
    std::cout.rdbuf(oldout);
    std::cerr.rdbuf(olderr);
    return {out.str(), err.str()};
}

TEST(PublicCLI, BasicOutput) {
    auto res = run_cli_args({"generate"});
    auto val = res.first;
    val.erase(val.find_last_not_of(" \t\n\r")+1);
    EXPECT_FALSE(val.empty());
}

TEST(PublicCLI, WithLength) {
    auto res = run_cli_args({"generate", "--length", "19"});
    auto val = res.first;
    val.erase(val.find_last_not_of(" \t\n\r")+1);
    EXPECT_EQ(val.size(), 19u);
}

TEST(PublicCLI, Help) {
    auto res = run_cli_args({"--help"});
    std::string allout = res.first + res.second;
    for (auto& c: allout) c = tolower(c);
    EXPECT_TRUE(allout.find("usage:") != std::string::npos);
}