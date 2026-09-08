#include <gtest/gtest.h>
#include "betterprompt.h"
#include <cstdlib>
#include <cmath>
#include <limits>
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

TEST(TestPublicBetterpromptEdgecases, GetFromDictOrEnvMissing) {
    std::string key = "PUBLIC_ENV_KEY";
    EnvGuard guard(key);
    guard.unset();
    std::map<std::string, std::string> empty_dict;
    try {
        betterprompt::get_from_dict_or_env(key, &empty_dict);
        FAIL() << "Expected error for missing key";
    } catch (const std::runtime_error& e) {
        ASSERT_NE(std::string(e.what()).find(key), std::string::npos);
    }
}

TEST(TestPublicBetterpromptEdgecases, GetFromDictOrEnvDict) {
    std::string key = "DICT_ONLY_KEY";
    std::map<std::string, std::string> d = { {key, "dict_value"} };
    EnvGuard guard(key);
    guard.set("env_value");
    EXPECT_EQ(betterprompt::get_from_dict_or_env(key, &d), "dict_value");
}

TEST(TestPublicBetterpromptEdgecases, GetFromDictOrEnvEnv) {
    std::string key = "ENV_ONLY_KEY_PUBLIC";
    EnvGuard guard(key);
    guard.unset();
    guard.set("from_env_public");
    EXPECT_EQ(betterprompt::get_from_dict_or_env(key, nullptr), "from_env_public");
}

TEST(TestPublicBetterpromptEdgecases, OpenAIClassDummy) {
    auto result = betterprompt::openai::Completion::create();
    ASSERT_TRUE(result.count("choices") > 0);
    auto choices = std::any_cast<std::vector<std::map<std::string, std::any>>>(result.at("choices"));
    ASSERT_FALSE(choices.empty());
}

TEST(TestPublicBetterpromptEdgecases, CallOpenAIApiKey) {
    struct DummyCompletion {
        static std::map<std::string, std::any> create() {
            std::vector<double> dummy_logprobs = {1.23, -0.8, 3.14};
            std::map<std::string, std::any> logprobs_map;
            logprobs_map["token_logprobs"] = dummy_logprobs;
            auto choice = std::map<std::string, std::any>{{"logprobs", logprobs_map}};
            std::vector<std::map<std::string, std::any>> choices = {choice};
            std::map<std::string, std::any> out;
            out["choices"] = choices;
            return out;
        }
    };
    auto old_create = betterprompt::openai::Completion::create;
    betterprompt::openai::Completion::create = DummyCompletion::create;
    std::vector<double> result = betterprompt::call_openai("test prompt", "a_public_key");
    EXPECT_EQ(result, std::vector<double>({1.23, -0.8, 3.14}));
    betterprompt::openai::Completion::create = old_create;
}

TEST(TestPublicBetterpromptEdgecases, CalculatePerplexityAllNegative) {
    std::vector<double> token_logprobs = {-2, -4, -6};
    double perplexity = betterprompt::calculate_perplexity(token_logprobs);
    double expected = std::exp(-( (-2) + (-4) + (-6) ) / 3.0 );
    EXPECT_NEAR(perplexity, expected, 1e-8);
}

TEST(TestPublicBetterpromptEdgecases, CalculatePerplexityEmpty) {
    auto result = betterprompt::calculate_perplexity({});
    EXPECT_TRUE(std::isinf(result));
}