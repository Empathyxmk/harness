#include <gtest/gtest.h>
#include <string>
#include <map>
#include <variant>
#include <memory>
#include <vector>
// Assume these are implemented as part of your main library
#include "pytracking/tracking.h"

using namespace pytracking;

// Helper: For base64, and json, assume you have functions util::base64_urlsafe_encode / decode and util::json_loads / dumps.
// Alternatively, use a base64/json library.

const std::string DUMMY_URL = "http://example.com";
const std::string DUMMY_WEBHOOK = "http://webhook.com";
const std::string DUMMY_KEY = util::base64_urlsafe_encode(std::vector<uint8_t>(32, '0')); // not a valid Fernet but tests struct


TEST(TrackingUnit, ConfigurationBasicInitFields) {
    Configuration config(
        DUMMY_WEBHOOK,
        10,
        true,
        "http://open.example.com",
        "http://click.example.com",
        std::map<std::string, util::Any>({{"x", 1}}),
        true,
        nullptr,
        "utf-8",
        true
    );
    EXPECT_EQ(config.webhook_url, DUMMY_WEBHOOK);
    EXPECT_EQ(config.webhook_timeout_seconds, 10);
    EXPECT_EQ(config.base_open_tracking_url, "http://open.example.com");
    EXPECT_TRUE(config.include_webhook_url);
    EXPECT_TRUE(config.include_default_metadata);
    EXPECT_FALSE(config.append_slash);  // not set by param!
}

TEST(TrackingUnit, StrAndDeepcopyAndMerge) {
    Configuration config_1("A", "B", "C", nullptr);
    std::string s = config_1.str();
    EXPECT_NE(s.find("<pytracking.Configuration>"), std::string::npos);
    auto cp = config_1.deepcopy();
    EXPECT_EQ(cp.webhook_url, config_1.webhook_url);
    auto new_c = config_1.merge_with_kwargs({{"webhook_url", util::Any(std::string("D"))}});
    EXPECT_EQ(new_c.webhook_url, "D");
    EXPECT_EQ(new_c.base_open_tracking_url, "B");
    // test cache_encryption_key without encryption_key; handled internally
}

TEST(TrackingUnit, GetDataToEmbedBaseAndMetadata) {
    Configuration config(
        DUMMY_WEBHOOK, true, std::map<std::string, util::Any>({{"foo", "bar"}}), true, "ccc", "ooo"
    );
    auto data = config.get_data_to_embed(DUMMY_URL, std::map<std::string, util::Any>({{"meta", 1}}));
    EXPECT_EQ(std::get<std::string>(data["url"]), DUMMY_URL);
    EXPECT_TRUE(data.find("metadata") != data.end());
    auto metadata = std::get<std::map<std::string, util::Any>>(data["metadata"]);
    EXPECT_EQ(std::get<std::string>(metadata["foo"]), "bar");
    EXPECT_EQ(std::get<int>(metadata["meta"]), 1);
    EXPECT_EQ(std::get<std::string>(data["webhook"]), DUMMY_WEBHOOK);

    // Without defaults
    Configuration config_2;
    auto res = config_2.get_data_to_embed(nullptr, nullptr);
    EXPECT_TRUE(res.empty());

    // Only url
    auto res_2 = config_2.get_data_to_embed("http://x", nullptr);
    EXPECT_EQ(res_2.size(), 1);
    EXPECT_EQ(std::get<std::string>(res_2["url"]), "http://x");
}

TEST(TrackingUnit, GetUrlEncodedDataStrWithoutEncryption) {
    Configuration cfg;
    cfg.encoding = "utf-8";
    std::map<std::string, util::Any> plain = {{"key", "value"}};
    std::string b64str = cfg.get_url_encoded_data_str(plain);
    // Should be decodable
    std::string decoded_json = util::base64_urlsafe_decode(b64str);
    auto decoded = util::json_loads(decoded_json);
    EXPECT_EQ(decoded["key"], "value");
}

// Skip fernet encrypt tests if unavailable: In C++ test, use ifdef or small runtime check
#ifdef HAS_CRYPTOGRAPHY
TEST(TrackingUnit, GetUrlEncodedDataStrWithEncryption) {
    auto key = util::fernet_generate_key();
    Configuration cfg;
    cfg.encoding = "utf-8";
    cfg.encryption_bytestring_key = key;
    std::map<std::string, util::Any> obj = {{"hello", "world"}};
    std::string enc = cfg.get_url_encoded_data_str(obj);
    std::string decrypted = util::fernet_decrypt(enc, key);
    auto round_trip = util::json_loads(decrypted);
    EXPECT_EQ(round_trip["hello"], "world");
}
#endif

TEST(TrackingUnit, ReprAndDefaults) {
    Configuration config;
    EXPECT_EQ(PNG_MIME_TYPE, "image/png");
    EXPECT_TRUE(typeid(TRACKING_PIXEL) == typeid(std::vector<uint8_t>));
    EXPECT_EQ(config.encryption_key, nullptr);
    EXPECT_EQ(config.webhook_timeout_seconds, DEFAULT_TIMEOUT_SECONDS);
}

TEST(TrackingUnit, MergeWithKwargsDoesNotChangeOriginal) {
    Configuration cfg;
    cfg.webhook_url = "x";
    auto newcfg = cfg.merge_with_kwargs({{"webhook_url", util::Any(std::string("y"))}});
    EXPECT_EQ(newcfg.webhook_url, "y");
    EXPECT_EQ(cfg.webhook_url, "x");
}