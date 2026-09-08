#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <vector>
#include "claude_to_chatgpt/adapter.h"
#include "claude_to_chatgpt/models.h"

// Similar structure to original, but with alternate values.

TEST(PublicClaudeAdapterTest, GetApiKeyFromHeaders) {
    ClaudeAdapter ca("http://another-url");
    std::unordered_map<std::string, std::string> headers = {{"authorization", "Bearer another-key"}};
    EXPECT_EQ(ca.get_api_key(headers), "another-key");
    ca.claude_api_key = "second-env-key";
    std::unordered_map<std::string, std::string> headers2;
    EXPECT_EQ(ca.get_api_key(headers2), "second-env-key");
}

TEST(PublicClaudeAdapterTest, ConvertMessagesToPromptRolesPublic) {
    ClaudeAdapter ca("public_url");
    std::vector<Message> messages = {
        {"user", "How are you?"},
        {"assistant", "I'm fine, thank you."},
        {"system", "System message here"}
    };
    std::string prompt = ca.convert_messages_to_prompt(messages);
    EXPECT_NE(prompt.find("\n\nHuman: How are you?"), std::string::npos);
    EXPECT_NE(prompt.find("\n\nAssistant: I'm fine, thank you."), std::string::npos);
    EXPECT_NE(prompt.find("\n\nHuman: How are you?"), std::string::npos);
    EXPECT_EQ(prompt.substr(prompt.size()-10), "Assistant:");
}

TEST(PublicClaudeAdapterTest, OpenAIToClaudeParamsAllPublic) {
    ClaudeAdapter ca;
    ca.convert_messages_to_prompt_patch = [](const std::vector<Message>&) { return "DIFFERENT_PROMPT"; };
    OpenAIParams oai{
        "gpt-4-0314",
        {},
        1024,
        {"STOP_NOW"},
        0.55,
        false
    };
    model_map["gpt-4-0314"] = "claude-v1";
    ClaudeParams params = ca.openai_to_claude_params(oai);
    EXPECT_EQ(params.model, "claude-v1");
    EXPECT_EQ(params.prompt, "DIFFERENT_PROMPT");
    EXPECT_EQ(params.max_tokens_to_sample, 1024);
    ASSERT_EQ(params.stop_sequences.size(), 1);
    EXPECT_EQ(params.stop_sequences[0], "STOP_NOW");
    EXPECT_DOUBLE_EQ(params.temperature, 0.55);
    EXPECT_FALSE(params.stream);
}

TEST(PublicClaudeAdapterTest, OpenAIToClaudeParamsPartialPublic) {
    ClaudeAdapter ca;
    ca.convert_messages_to_prompt_patch = [](const std::vector<Message>&) { return "ALT_PROMPT"; };
    OpenAIParams oai{
        "absent-model",
        {},
        -1,
        {},
        0.0,
        false
    };
    model_map.erase("absent-model");
    ClaudeParams params = ca.openai_to_claude_params(oai);
    EXPECT_EQ(params.model, "claude-2");
    EXPECT_EQ(params.prompt, "ALT_PROMPT");
    EXPECT_EQ(params.max_tokens_to_sample, 100000);
}

TEST(PublicClaudeAdapterTest, ClaudeToChatGptResponseStreamPublic) {
    ClaudeAdapter ca;
    std::string completion = "Different completion";
    std::string stop_reason = "max_tokens";
    ca.num_tokens_from_string_patch = [](const std::string&) { return 10; };
    ResponseStream resp = ca.claude_to_chatgpt_response_stream({completion, stop_reason});
    EXPECT_EQ(resp.choices[0].delta_content, completion);
    EXPECT_EQ(resp.choices[0].finish_reason, stop_reason_map.at(stop_reason));
    EXPECT_EQ(resp.usage.completion_tokens, 10);
}

TEST(PublicClaudeAdapterTest, ClaudeToChatGptResponseNoStopPublic) {
    ClaudeAdapter ca;
    std::string completion = "A different completion text";
    ca.num_tokens_from_string_patch = [](const std::string&) { return 7; };
    Response resp = ca.claude_to_chatgpt_response({completion});
    EXPECT_EQ(resp.choices[0].message_content, completion);
    EXPECT_EQ(resp.choices[0].finish_reason, "");
    EXPECT_EQ(resp.usage.completion_tokens, 7);
}

TEST(PublicClaudeAdapterTest, ConvertMessagesToPromptCorrectFormatPublic) {
    ClaudeAdapter ca;
    std::vector<Message> messages = {{"user", "What's up?"}};
    std::string result = ca.convert_messages_to_prompt(messages);
    EXPECT_TRUE(result.find("\n\nHuman: What's up?") == 0);
    EXPECT_TRUE(result.size() >= 10 && result.substr(result.size() - 10) == "Assistant: ");
}