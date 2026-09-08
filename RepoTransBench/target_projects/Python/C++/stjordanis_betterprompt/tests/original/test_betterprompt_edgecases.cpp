#include <gtest/gtest.h>
#include "betterprompt.h"
#include <cstdlib>
#include <cmath>
#include <limits>
#include <stdexcept>
#include <map>

class EnvGuard {
public:
    EnvGuard(const std::string& key) : key_(key), had_var_(false) {
        const char* oldval = std::getenv(key.c_str());
        if (oldval) { had_var_ = true; oldval_ = std::string(oldval); }
    }
    ~EnvGuard() {
        if (had_var_)
            setenv(key_.c_str(), oldval_.c_str(), 1);
        else
            unsetenv(key_.c_str());
    }
    void unset() { unsetenv(key_.c_str()); }
    void set(const std::string& val) { setenv(key_.c_str(), val.c_str(), 1); }
private:
    std::string key_;
    bool had_var_;
    std::string oldval_;
};

TEST(TestBetterpromptEdgeCases, GetFromDictOrEnvEmptyDictNoEnv) {
    std::string key = "TEST_MISSING_KEY";
    EnvGuard guard(key);
    guard.unset();
    std::map<std::string, std::string> empty_dict;
    try {
        betterprompt::get_from_dict_or_env(key, &empty_dict);
        FAIL() << "Expected exception for missing key";
    } catch (const std::runtime_error& e) {
        ASSERT_NE(std::string(e.what()).find(key), std::string::npos);
    }
}

TEST(TestBetterpromptEdgeCases, GetFromDictOrEnvNoneDictEnv) {
    std::string key = "ENV_ONLY_KEY";
    EnvGuard guard(key);
    guard.set("val");
    EXPECT_EQ(betterprompt::get_from_dict_or_env(key, nullptr), "val");
}

TEST(TestBetterpromptEdgeCases, GetFromDictOrEnvDictEmpty) {
    std::string key = "NO_DICT_KEY";
    EnvGuard guard(key);
    guard.set("from_env");
    std::map<std::string, std::string> empty_dict;
    EXPECT_EQ(betterprompt::get_from_dict_or_env(key, &empty_dict), "from_env");
}

TEST(TestBetterpromptEdgeCases, OpenAIClassAndDummy) {
    auto res = betterprompt::openai::Completion::create();
    ASSERT_TRUE(res.count("choices") > 0);
}

TEST(TestBetterpromptEdgeCases, CallOpenAIApiKey) {
    // We'll redefine openai::Completion::create for testing
    struct DummyCompletion {
        static std::map<std::string, std::any> create() {
            std::vector<double> dummy_logprobs = {0.4, 0.5, 0.6};
            std::map<std::string, std::any> logprobs_map;
            logprobs_map["token_logprobs"] = dummy_logprobs;
            std::map<std::string, std::any> choice = {{"logprobs", logprobs_map}};
            std::vector<std::map<std::string, std::any>> choices = {choice};
            std::map<std::string, std::any> out;
            out["choices"] = choices;
            return out;
        }
    };
    // Replace function pointer
    auto old_create = betterprompt::openai::Completion::create;
    betterprompt::openai::Completion::create = DummyCompletion::create;
    std::vector<double> result = betterprompt::call_openai("prompt", "explicit_key");
    EXPECT_EQ(result, std::vector<double>({0.4, 0.5, 0.6}));
    // Restore original
    betterprompt::openai::Completion::create = old_create;
}

TEST(TestBetterpromptEdgeCases, CalculatePerplexityRegular) {
    std::vector<double> token_logprobs = {0, -1, -2};
    double expected = std::exp(-( (0 + -1 + -2) / 3.0));
    double perplexity = betterprompt::calculate_perplexity(token_logprobs);
    EXPECT_NEAR(perplexity, expected, 1e-8);
}

TEST(TestBetterpromptEdgeCases, CalculatePerplexityEmpty) {
    auto result = betterprompt::calculate_perplexity({});
    EXPECT_TRUE(std::isinf(result));
}