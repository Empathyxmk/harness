#include <gtest/gtest.h>
#include "pytracking/tracking.h"
#include "pytracking/configuration.h"
#include "util/base64.h"
#include "util/json.h"

using namespace pytracking;

const std::string ANOTHER_URL = "https://anotherdomain.org";
const std::string ANOTHER_WEBHOOK = "https://anotherwebhook.org/notify";
const std::string ANOTHER_KEY = util::base64_urlsafe_encode(std::vector<uint8_t>(32, '9'));


TEST(PublicTrackingUnit, PublicConfigurationInitFields) {
    Configuration config(
        ANOTHER_WEBHOOK,
        15,
        false,
        "https://tracker.domain.io/open",
        "https://tracker.domain.io/click",
        std::map<std::string, util::Any>({{"user", "alice"}}),
        false,
        nullptr,
        "latin-1",
        false
    );
    EXPECT_EQ(config.webhook_url, ANOTHER_WEBHOOK);
    EXPECT_EQ(config.webhook_timeout_seconds, 15);
    EXPECT_EQ(config.base_open_tracking_url, "https://tracker.domain.io/open");
    EXPECT_FALSE(config.include_webhook_url);
    EXPECT_FALSE(config.include_default_metadata);
    EXPECT_FALSE(config.append_slash);
}

TEST(PublicTrackingUnit, PublicStrAndDeepcopyAndMerge) {
    Configuration config_1("PublicWebhook", "OpenURL", "ClickURL", nullptr);
    std::string s = config_1.str();
    EXPECT_NE(s.find("<pytracking.Configuration>"), std::string::npos);
    auto cp = config_1.deepcopy();
    EXPECT_EQ(cp.webhook_url, config_1.webhook_url);
    auto new_c = config_1.merge_with_kwargs({{"webhook_url", util::Any(std::string("SecondWebhook"))}});
    EXPECT_EQ(new_c.webhook_url, "SecondWebhook");
    EXPECT_EQ(new_c.base_open_tracking_url, "OpenURL");
}

TEST(PublicTrackingUnit, PublicGetDataToEmbedVariedAndMetadata) {
    Configuration config(
        ANOTHER_WEBHOOK, false, std::map<std::string, util::Any>({{"role", "dev"}}), false, "click123", "open456"
    );
    auto data = config.get_data_to_embed(ANOTHER_URL, std::map<std::string, util::Any>({{"device", "mobile"}}));
    EXPECT_EQ(std::get<std::string>(data["url"]), ANOTHER_URL);
    EXPECT_TRUE(data.find("metadata") != data.end());
    auto metadata = std::get<std::map<std::string, util::Any>>(data["metadata"]);
    EXPECT_EQ(std::get<std::string>(metadata["role"]), "dev");
    EXPECT_EQ(std::get<std::string>(metadata["device"]), "mobile");
    EXPECT_TRUE(data.find("webhook") == data.end());

    // No defaults/metadata
    Configuration config_2;
    auto res = config_2.get_data_to_embed(nullptr, nullptr);
    EXPECT_TRUE(res.empty());

    // Only url, no metadata/default
    auto res_2 = config_2.get_data_to_embed("https://demo", nullptr);
    EXPECT_EQ(res_2.size(), 1);
    EXPECT_EQ(std::get<std::string>(res_2["url"]), "https://demo");
}

TEST(PublicTrackingUnit, PublicGetUrlEncodedDataStrWithoutEncryption) {
    Configuration cfg;
    cfg.encoding = "utf-16";
    std::map<std::string, util::Any> plain = {{"alpha", "beta"}};
    std::string b64str = cfg.get_url_encoded_data_str(plain);
    std::string decoded_json = util::base64_urlsafe_decode(b64str, "utf-16");
    auto decoded = util::json_loads(decoded_json);
    EXPECT_EQ(decoded["alpha"], "beta");
}

// Only if cryptography/fernet available
#ifdef HAS_CRYPTOGRAPHY
TEST(PublicTrackingUnit, PublicGetUrlEncodedDataStrWithEncryption) {
    auto key = util::fernet_generate_key();
    Configuration cfg;
    cfg.encoding = "utf-8";
    cfg.encryption_bytestring_key = key;
    std::map<std::string, util::Any> obj = {{"foo", "barbaz"}};
    std::string enc = cfg.get_url_encoded_data_str(obj);
    std::string decrypted = util::fernet_decrypt(enc, key);
    auto round_trip = util::json_loads(decrypted);
    EXPECT_EQ(round_trip["foo"], "barbaz");
}
#endif

TEST(PublicTrackingUnit, PublicReprAndDefaults) {
    Configuration config;
    EXPECT_EQ(PNG_MIME_TYPE, "image/png");
    EXPECT_TRUE(typeid(TRACKING_PIXEL) == typeid(std::vector<uint8_t>));
    EXPECT_EQ(config.encryption_key, nullptr);
    EXPECT_EQ(config.webhook_timeout_seconds, DEFAULT_TIMEOUT_SECONDS);
}

TEST(PublicTrackingUnit, PublicMergeWithKwargsDoesNotChangeOriginal) {
    Configuration cfg;
    cfg.webhook_url = "web1";
    auto newcfg = cfg.merge_with_kwargs({{"webhook_url", util::Any(std::string("web2"))}});
    EXPECT_EQ(newcfg.webhook_url, "web2");
    EXPECT_EQ(cfg.webhook_url, "web1");
}