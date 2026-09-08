#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <stdexcept>

// Stubbed example application logic, to match the likely structure of the Python cmdline module.
class CmdlineArgs {
public:
    CmdlineArgs() : verbose(false), username(""), password("") {}

    bool parse(int argc, const char* argv[]) {
        verbose = false;
        username.clear();
        password.clear();

        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg == "-v" || arg == "--verbose") {
                verbose = true;
            } else if (arg == "-u" && i + 1 < argc) {
                username = argv[++i];
            } else if (arg == "-p" && i + 1 < argc) {
                password = argv[++i];
            }
        }
        return !username.empty() && !password.empty();
    }

    bool verbose;
    std::string username;
    std::string password;
};

TEST(CmdlineTest, ParsesVerboseFlag) {
    const char* argv[] = {"prog", "-v", "-u", "alice", "-p", "pass"};
    CmdlineArgs args;
    bool result = args.parse(6, argv);
    EXPECT_TRUE(result);
    EXPECT_TRUE(args.verbose);
    EXPECT_EQ(args.username, "alice");
    EXPECT_EQ(args.password, "pass");
}

TEST(CmdlineTest, ParsesLongVerboseFlag) {
    const char* argv[] = {"prog", "--verbose", "-u", "bob", "-p", "secret"};
    CmdlineArgs args;
    bool result = args.parse(6, argv);
    EXPECT_TRUE(result);
    EXPECT_TRUE(args.verbose);
    EXPECT_EQ(args.username, "bob");
    EXPECT_EQ(args.password, "secret");
}

TEST(CmdlineTest, ReturnsFalseIfMissingUsername) {
    const char* argv[] = {"prog", "-v", "-p", "test"};
    CmdlineArgs args;
    bool result = args.parse(4, argv);
    EXPECT_FALSE(result);
}

TEST(CmdlineTest, ReturnsFalseIfMissingPassword) {
    const char* argv[] = {"prog", "-u", "joe"};
    CmdlineArgs args;
    bool result = args.parse(3, argv);
    EXPECT_FALSE(result);
}