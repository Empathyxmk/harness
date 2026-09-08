#include <gtest/gtest.h>
#include <string>
#include <memory>
#include <sstream>
#include <iostream>
#include "../../src/masker_formatter.h"
#include "../../src/utils.h"

using maskerlogger::MaskerFormatter;
using maskerlogger::MaskerFormatterJson;
using maskerlogger::AbstractMaskedLogger;

// Dummy log record structure for the tests, simulating Python's LogRecord
struct DummyRecord {
    std::string msg;
    bool apply_mask = true;
    DummyRecord(const std::string& message) : msg(message) {}
};

TEST(TestMaskerLogger, MaskSecretLogic) {
    AbstractMaskedLogger logger(maskerlogger::get_config_file_path());
    std::smatch match;
    // Simulate a regex match ("abbbbb")
    std::regex re("(a)(b+)");
    std::string teststr = "abbbbb";
    std::regex_search(teststr, match, re);

    std::string result = logger._mask_secret("abbbbb start abbbbb", {match});
    size_t star_count = std::count(result.begin(), result.end(), '*');
    ASSERT_GT(star_count, 0u);
}

TEST(TestMaskerLogger, MaskSensitiveDataNoMatch) {
    AbstractMaskedLogger logger(maskerlogger::get_config_file_path());
    DummyRecord rec("no secrets here");
    logger._mask_sensitive_data(rec);
    ASSERT_EQ(rec.msg, "no secrets here");
}

TEST(TestMaskerLogger, MaskSensitiveDataWithMatch) {
    AbstractMaskedLogger logger(maskerlogger::get_config_file_path());
    DummyRecord rec("\"password\": \"password321\" and apikey = 1234");
    logger.redact = 45;
    logger._mask_sensitive_data(rec);
    ASSERT_TRUE(typeid(rec.msg) == typeid(std::string));
    ASSERT_EQ(rec.msg.find("password321"), std::string::npos);
}

TEST(TestMaskerLogger, FormatterFullLogIntegration) {
    // This test simulates real logging by redirecting stream (no actual stdout)
    MaskerFormatter formatter("%(levelname)s %(message)s", maskerlogger::get_config_file_path(), 75);
    std::ostringstream ss;
    // Simulated logging lines, not real logging API
    std::vector<std::string> messages = {
        "\"current_key\": \"AIzaSOHbouG6DDa6DOcRGEgOMayAXYXcw6la3c\"",
        "\"AKIAI44QH8DHBEXAMPLE\" and then more text.",
        "Datadog access token: 'abcdef1234567890abcdef1234567890'",
        "\"password\": \"password123\""
    };
    for (const auto& msg : messages) {
        DummyRecord rec(msg);
        auto masked = formatter.format(rec);
        ss << masked << std::endl;
    }
    std::string output = ss.str();
    // Minimum expected: keys are masked (contains "*")
    ASSERT_NE(output.find("*"), std::string::npos);
}

TEST(TestMaskerLogger, JsonFormatterLogrecordMasking) {
    MaskerFormatterJson json_formatter("%(message)s", maskerlogger::get_config_file_path(), 50);
    DummyRecord rec("apikey = \"TESTEXPOSEDSECRET\"");
    auto value = json_formatter.format(rec);
    ASSERT_NE(value.find("apikey"), std::string::npos);
}

TEST(TestMaskerLogger, MaskerFormatterJsonSkipMask) {
    MaskerFormatterJson json_formatter("%(message)s", maskerlogger::get_config_file_path(), 50);
    DummyRecord rec("sometext");
    rec.apply_mask = false;
    auto result = json_formatter.format(rec);
    ASSERT_NE(result.find("sometext"), std::string::npos);
}

TEST(TestMaskerLogger, ReprAndStr) {
    MaskerFormatterJson json_formatter("%(message)s", maskerlogger::get_config_file_path(), 50);
    std::string clsName = typeid(json_formatter).name();
    ASSERT_NE(clsName.find("Json"), std::string::npos);
}