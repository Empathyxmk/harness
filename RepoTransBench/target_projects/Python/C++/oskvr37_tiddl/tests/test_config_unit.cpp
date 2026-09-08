#include <gtest/gtest.h>
#include <string>
#include <map>
#include <stdexcept>
#include <algorithm>

// ----- Stub config logic for testing -----

namespace tiddl {

struct Config {
    std::map<std::string, std::string> values;

    Config() {
        // Load some defaults
        values["retry_count"] = "3";
        values["api_url"] = "https://api.example.com";
    }

    void set(const std::string& key, const std::string& value) {
        values[key] = value;
    }

    std::string get(const std::string& key, const std::string& default_val = "") const {
        auto it = values.find(key);
        if (it != values.end()) return it->second;
        return default_val;
    }

    bool validate() const {
        // For testing, require retry_count to be integer >= 0 and api_url to start with "https://"
        try {
            int retry = std::stoi(get("retry_count"));
            if (retry < 0) return false;
            std::string api_url = get("api_url");
            return api_url.rfind("https://", 0) == 0;
        } catch (...) {
            return false;
        }
    }
};

}

// -------------- Actual Unit Tests --------------

TEST(ConfigUnitTest, DefaultValuesArePresentAndValid) {
    tiddl::Config config;
    EXPECT_EQ(config.get("retry_count"), "3");
    EXPECT_EQ(config.get("api_url"), "https://api.example.com");
    EXPECT_TRUE(config.validate());
}

TEST(ConfigUnitTest, CustomValuesAreSetAndGet) {
    tiddl::Config config;
    config.set("retry_count", "10");
    config.set("api_url", "https://custom.tiddl.co");
    EXPECT_EQ(config.get("retry_count"), "10");
    EXPECT_EQ(config.get("api_url"), "https://custom.tiddl.co");
    EXPECT_TRUE(config.validate());
}

TEST(ConfigUnitTest, MissingValuesReturnDefault) {
    tiddl::Config config;
    EXPECT_EQ(config.get("not_set", "fallback"), "fallback");
    EXPECT_EQ(config.get("nonexistent"), ""); // No default, returns empty
}

TEST(ConfigUnitTest, ValidationFailsOnInvalidRetryCount) {
    tiddl::Config config;
    config.set("retry_count", "-2");
    EXPECT_FALSE(config.validate());
    config.set("retry_count", "bad_val");
    EXPECT_FALSE(config.validate());
}

TEST(ConfigUnitTest, ValidationFailsIfApiUrlNotHttps) {
    tiddl::Config config;
    config.set("api_url", "http://notsecure.example.com");
    EXPECT_FALSE(config.validate());
    config.set("api_url", "ftp://fileserver.example.com");
    EXPECT_FALSE(config.validate());
}

TEST(ConfigUnitTest, UpdatingConfigDoesNotAffectDefaultsElsewhere) {
    tiddl::Config config1;
    tiddl::Config config2;
    config1.set("retry_count", "6");
    config2.set("api_url", "https://api.other.com");
    EXPECT_EQ(config1.get("retry_count"), "6");
    EXPECT_EQ(config2.get("retry_count"), "3"); // default for config2
    EXPECT_EQ(config1.get("api_url"), "https://api.example.com");
    EXPECT_EQ(config2.get("api_url"), "https://api.other.com");
}