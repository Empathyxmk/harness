#include <gtest/gtest.h>
#include "check_manifest.h"
using namespace check_manifest;

TEST(TestUI, QuietAndVerbosePublic) {
    // Use a different verbosity level for coverage
    UI ui1(1);
    EXPECT_FALSE(ui1.quiet());
    EXPECT_FALSE(ui1.verbose());

    UI ui3(3);
    EXPECT_FALSE(ui3.quiet());
    EXPECT_TRUE(ui3.verbose());
}

TEST(TestUI, InfoMethodsPublic) {
    UI ui(3);
    ui.info("public info message");
    ui.info_begin("public begin message");
    ui.info_continue("public continued...");
    ui.info_end("public done!");
    ui._to_be_continued = true;
    ui.info("public info after tbc");
    ui.error("public error message");
    ui.warning("public warn message");
}

TEST(TestUI, InfoQuietPublic) {
    UI ui(-1);
    ui.info("nothing to print here");
    ui.info_begin("still nothing begin");
    ui.info_continue("still nothing continue");
    ui.info_end("still nothing end");
}

TEST(TestUI, ErrorAndWarningPublic) {
    UI ui(1);
    ui.error("ERROR for public");
    ui.warning("WARNING for public");
}

TEST(TestFormatUtils, FormatListPublic) {
    EXPECT_EQ(format_list({"x"}), "  x");
    EXPECT_EQ(format_list({"foo", "bar", "baz"}), "  foo\n  bar\n  baz");
}

TEST(TestFormatUtils, FormatMissingPublic) {
    // Both lists non-empty
    EXPECT_EQ(
        format_missing({"first"}, {"second"}, "Alpha", "Beta"),
        "missing from Alpha:\n  first\nmissing from Beta:\n  second"
    );
    // Missing just from Beta
    EXPECT_EQ(
        format_missing({}, {"hello"}, "Src", "Dst"),
        "missing from Dst:\n  hello"
    );
    // Missing just from Alpha
    EXPECT_EQ(
        format_missing({"world"}, {}, "Src", "Dst"),
        "missing from Src:\n  world"
    );
    // Both lists empty, different section names
    EXPECT_EQ(
        format_missing({}, {}, "One", "Two"),
        ""
    );
}

TEST(TestFailure, FailureMessagePublic) {
    std::string msg = "another fail message";
    Failure f(msg);
    EXPECT_EQ(f.str(), msg);
}

TEST(TestFailure, CommandFailedPublic) {
    CommandFailed c({"echo", "abc"}, 99, "fatal error");
    std::string out = c.str();
    EXPECT_NE(out.find("failed"), std::string::npos);
    EXPECT_NE(out.find("echo"), std::string::npos);
}