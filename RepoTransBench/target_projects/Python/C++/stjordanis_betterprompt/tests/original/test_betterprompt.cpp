#include <gtest/gtest.h>
#include "betterprompt.h"

TEST(TestBetterprompt, Metadata) {
    EXPECT_TRUE(!betterprompt::version().empty());
    EXPECT_TRUE(!betterprompt::author().empty());
    EXPECT_TRUE(!betterprompt::copyright().empty());
    EXPECT_TRUE(!betterprompt::license_().empty());
    auto all = betterprompt::get_all_exports();
    auto it = std::find(all.begin(), all.end(), "get_from_dict_or_env");
    EXPECT_TRUE(it != all.end());
}

TEST(TestBetterprompt, DummyOpenAICompletionCreate) {
    auto res = betterprompt::DummyOpenAICompletion::create();
    ASSERT_TRUE(res.count("choices") > 0);
    // Should be vector of maps
    auto choices = std::any_cast<std::vector<std::map<std::string, std::any>>>(res.at("choices"));
    ASSERT_FALSE(choices.empty());
}

TEST(TestBetterprompt, OpenAICompletionStatic) {
    auto res = betterprompt::openai::Completion::create();
    ASSERT_TRUE(res.count("choices") > 0);
    auto choices = std::any_cast<std::vector<std::map<std::string, std::any>>>(res.at("choices"));
    ASSERT_FALSE(choices.empty());
    auto logprobs_map = std::any_cast<std::map<std::string, std::any>>(choices[0].at("logprobs"));
    auto token_logprobs = std::any_cast<std::vector<double>>(logprobs_map.at("token_logprobs"));
    EXPECT_EQ(token_logprobs[0], 0.0);
    EXPECT_EQ(token_logprobs[1], -1.0);
    EXPECT_EQ(token_logprobs[2], -2.0);
}