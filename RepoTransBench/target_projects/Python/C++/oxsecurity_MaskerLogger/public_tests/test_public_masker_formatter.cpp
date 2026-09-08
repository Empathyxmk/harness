#include <gtest/gtest.h>
#include <string>
#include "../src/masker_formatter.h"

using maskerlogger::MaskerFormatter;
using maskerlogger::MaskerFormatterJson;
using maskerlogger::AbstractMaskedLogger;

struct DummyRecord {
    std::string msg;
    bool apply_mask = true;
    DummyRecord(const std::string& message) : msg(message) {}
};

TEST(TestMaskerFormatterPublic, NoMaskingIfNoMatchPublic) {
    MaskerFormatter formatter("%(message)s");
    DummyRecord rec("12345 is a safe message");
    std::string out = formatter.format(rec);
    ASSERT_EQ(out, "12345 is a safe message");
}

TEST(TestMaskerFormatterPublic, MaskingWithRegexMatchPublic) {
    MaskerFormatter formatter("%(message)s");
    DummyRecord rec("apikey: mytopsecret");
    std::string out = formatter.format(rec);
    ASSERT_NE(out.find("***"), std::string::npos);
}

TEST(TestMaskerFormatterPublic, SkipMaskPublic) {
    MaskerFormatterJson formatter("%(message)s");
    DummyRecord rec("nothing to mask here");
    rec.apply_mask = false;
    std::string out = formatter.format(rec);
    ASSERT_EQ(out, "nothing to mask here");
}

TEST(TestAbstractMaskedLoggerPublic, MaskSecretPublic) {
    AbstractMaskedLogger logger;
    std::smatch m;
    std::regex re("(mytopsecret)");
    std::string s = "apikey: mytopsecret";
    std::regex_search(s, m, re);
    std::string masked = logger._mask_secret("apikey: mytopsecret", {m});
    ASSERT_NE(masked.find("***"), std::string::npos);
}