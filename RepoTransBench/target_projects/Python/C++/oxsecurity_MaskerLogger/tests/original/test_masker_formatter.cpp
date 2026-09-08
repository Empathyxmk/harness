#include <gtest/gtest.h>
#include <string>
#include "../../src/masker_formatter.h"

using maskerlogger::MaskerFormatter;
using maskerlogger::MaskerFormatterJson;
using maskerlogger::AbstractMaskedLogger;

// DummyRecord for this module
struct DummyRecord {
    std::string msg;
    bool apply_mask = true;
    DummyRecord(const std::string& message) : msg(message) {}
};

TEST(TestMaskerFormatter, NoMaskingIfNoMatch) {
    MaskerFormatter formatter("%(message)s");
    DummyRecord rec("nothing secret here");
    std::string out = formatter.format(rec);
    ASSERT_EQ(out, "nothing secret here");
}

TEST(TestMaskerFormatter, MaskingWithRegexMatch) {
    MaskerFormatter formatter("%(message)s");
    DummyRecord rec("password: hunter2");
    std::string out = formatter.format(rec);
    ASSERT_NE(out.find("***"), std::string::npos);
}

TEST(TestMaskerFormatter, SkipMask) {
    MaskerFormatterJson formatter("%(message)s");
    DummyRecord rec("skip masking please");
    rec.apply_mask = false;
    std::string out = formatter.format(rec);
    ASSERT_EQ(out, "skip masking please");
}

TEST(TestAbstractMaskedLogger, MaskSecret) {
    AbstractMaskedLogger logger;
    std::smatch m;
    std::regex re("(hunter2)");
    std::string s = "password: hunter2";
    std::regex_search(s, m, re);
    std::string masked = logger._mask_secret("password: hunter2", {m});
    ASSERT_NE(masked.find("***"), std::string::npos);
}