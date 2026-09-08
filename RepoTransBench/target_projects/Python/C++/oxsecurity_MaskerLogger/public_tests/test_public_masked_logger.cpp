#include <gtest/gtest.h>
#include <string>
#include <memory>
#include <sstream>
#include <iostream>
#include "../src/masker_formatter.h"
#include "../src/utils.h"

using maskerlogger::MaskerFormatter;
using maskerlogger::MaskerFormatterJson;
using maskerlogger::AbstractMaskedLogger;

struct DummyRecord {
    std::string msg;
    bool apply_mask = true;
    DummyRecord(const std::string& message) : msg(message) {}
};

TEST(TestMaskerLoggerFullPathsPublic, MaskSecretLogicWithNewPattern) {
    AbstractMaskedLogger logger(maskerlogger::get_config_file_path());
    std::smatch match;
    std::regex re("(x)(y+)");
    std::string teststr = "xyyyy";
    std::regex_search(teststr, match, re);

    std::string result = logger._mask_secret("xyyyy abc xyyyy", {match});
    size_t star_count = std::count(result.begin(), result.end(), '*');
    ASSERT_GT(star_count, 0u);
}

TEST(TestMaskerLoggerFullPathsPublic, MaskSensitiveDataNoMatchNewmsg) {
    AbstractMaskedLogger logger(maskerlogger::get_config_file_path());
    DummyRecord rec("totally safe entry");
    logger._mask_sensitive_data(rec);
    ASSERT_EQ(rec.msg, "totally safe entry");
}

TEST(TestMaskerLoggerFullPathsPublic, MaskSensitiveDataWithMatchNewsecret) {
    AbstractMaskedLogger logger(maskerlogger::get_config_file_path());
    DummyRecord rec("\"token\": \"abcd12345efgh\" and secret_key = zyxw");
    logger.redact = 39;
    logger._mask_sensitive_data(rec);
    ASSERT_TRUE(typeid(rec.msg) == typeid(std::string));
    ASSERT_EQ(rec.msg.find("abcd12345efgh"), std::string::npos);
}

TEST(TestMaskerLoggerFullPathsPublic, FormatterFullLogIntegrationPublic) {
    MaskerFormatter formatter("%(levelname)s: %(message)s", maskerlogger::get_config_file_path(), 33);
    std::ostringstream ss;
    std::vector<std::string> messages = {
        "\"another_key\": \"AIzaSoMEoth3rKEY344sdlGh289Ka3dLPd\"",
        "\"AWS_SECRET_THISISFAKE\" and some more.",
        "Datadog token is: 'zyxw9876zyxw9876zyxw9876zyxw9876'",
        "\"pin\": \"5678\""
    };
    for (const auto& msg : messages) {
        DummyRecord rec(msg);
        auto masked = formatter.format(rec);
        ss << masked << std::endl;
    }
    std::string output = ss.str();
    ASSERT_NE(output.find("*"), std::string::npos);
}

TEST(TestMaskerLoggerFullPathsPublic, JsonFormatterLogrecordMaskingPublic) {
    MaskerFormatterJson json_formatter("%(message)s", maskerlogger::get_config_file_path(), 22);
    DummyRecord rec("auth = \"FAKENEWSECRETXYZ\"");
    auto value = json_formatter.format(rec);
    ASSERT_NE(value.find("auth"), std::string::npos);
}

TEST(TestMaskerLoggerFullPathsPublic, MaskerFormatterJsonSkipMaskPublic) {
    MaskerFormatterJson json_formatter("%(message)s", maskerlogger::get_config_file_path(), 22);
    DummyRecord rec("publiclogtext");
    rec.apply_mask = false;
    auto result = json_formatter.format(rec);
    ASSERT_NE(result.find("publiclogtext"), std::string::npos);
}

TEST(TestMaskerLoggerFullPathsPublic, ReprAndStrPublic) {
    MaskerFormatterJson json_formatter("%(message)s", maskerlogger::get_config_file_path(), 22);
    std::string clsName = typeid(json_formatter).name();
    ASSERT_NE(clsName.find("Json"), std::string::npos);
}