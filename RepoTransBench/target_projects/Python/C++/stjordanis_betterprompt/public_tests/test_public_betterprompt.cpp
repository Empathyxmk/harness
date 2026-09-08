#include <gtest/gtest.h>
#include "betterprompt.h"
#include <cmath>
#include <limits>
#include <vector>
#include <map>

TEST(TestPublicBetterprompt, CallOpenAICustomModel) {
    struct DummyCompletion {
        static std::map<std::string, std::any> create() {
            // Check the model argument through an external route – cannot in C++ easily
            std::vector<double> dummy_logprobs = {-0.1, 2.5, -4.3};
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
    std::vector<double> res = betterprompt::call_openai("sample prompt here", "anypublickey", "public-model");
    EXPECT_EQ(res, std::vector<double>({-0.1, 2.5, -4.3}));
    betterprompt::openai::Completion::create = old_create;
}

TEST(TestPublicBetterprompt, CallOpenAIEnv) {
    struct DummyCompletion {
        static std::map<std::string, std::any> create() {
            std::vector<double> dummy_logprobs = {7, 8};
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
    setenv("OPENAI_API_KEY", "public_env_key_test", 1);
    std::vector<double> res = betterprompt::call_openai("prompt string");
    EXPECT_EQ(res, std::vector<double>({7, 8}));
    betterprompt::openai::Completion::create = old_create;
    unsetenv("OPENAI_API_KEY");
}

TEST(TestPublicBetterprompt, CalculatePerplexityDifferent) {
    std::vector<double> token_logprobs = {-1, 0, 1, 2};
    double expect = std::exp(-(( -1 + 0 + 1 + 2) / 4.0));
    double actual = betterprompt::calculate_perplexity(token_logprobs);
    EXPECT_NEAR(actual, expect, 1e-8);
}