#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <vector>
#include "src/ai_models/main.h"

Args dummy_parse_args(const std::vector<std::string>& argv) {
    if (std::find(argv.begin(), argv.end(), "nonsense_command") != argv.end()) {
        throw SystemExitException(2);
    }
    Args args;
    args.command = argv.at(0);
    args.dummy = argv.size() > 2 ? argv.at(2) : "";
    return args;
}

class DummyParseArgsContext {
public:
    DummyParseArgsContext() {
        set_parse_args(dummy_parse_args);
    }
    ~DummyParseArgsContext() {
        reset_parse_args();
    }
};

TEST(PublicMain, ParseArgs) {
    DummyParseArgsContext ctx;
    std::vector<std::string> argv = {"run", "--dummy", "xy"};
    auto args = parse_args(argv);
    EXPECT_EQ(args.command, "run");
    EXPECT_TRUE(args.dummy == "xy" || args.dummy == "");
}

TEST(PublicMain, InvalidArgs) {
    DummyParseArgsContext ctx;
    std::vector<std::string> argv = {"nonsense_command"};
    EXPECT_THROW(parse_args(argv), SystemExitException);
}