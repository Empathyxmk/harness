#include <gtest/gtest.h>
#include <string>
#include "mailmerge.h"

class TestMailMergeParseInstr : public ::testing::Test {};

TEST_F(TestMailMergeParseInstr, ParseInstrValid) {
    std::string instr = "MERGEFIELD  somefield  \\* MERGEFORMAT";
    std::string name = MailMerge::__parse_instr(instr);
    EXPECT_EQ(name, "somefield");
}

TEST_F(TestMailMergeParseInstr, ParseInstrInvalid) {
    std::string instr = "SOMETHINGELSE testing";
    std::string name = MailMerge::__parse_instr(instr);
    EXPECT_EQ(name, "");
}

TEST_F(TestMailMergeParseInstr, ParseInstrQuoted) {
    std::string instr = "MERGEFIELD \"another field\"";
    std::string name = MailMerge::__parse_instr(instr);
    EXPECT_EQ(name, "another field");
}