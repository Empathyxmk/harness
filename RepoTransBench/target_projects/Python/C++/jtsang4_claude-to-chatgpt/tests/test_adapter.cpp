#include <gtest/gtest.h>
#include <unordered_map>
#include <string>
#include <vector>
#include "claude_to_chatgpt/adapter.h"
#include "claude_to_chatgpt/models.h"

// Mocks & helpers
class ClaudeAdapterTest : public ::testing::Test {
protected:
    ClaudeAdapter ca;

    ClaudeAdapterTest() : ca("http://test-url") {}
};

// Test get_api_key with header present and fallback
TEST_F(ClaudeAdapterTest, GetApiKeyFromHeaders) {
    std::unordered_map<std::string, std::string> headers = {{"authorization", "Bearer secret-key"}};
    EXPECT_EQ(ca.get_api_key(headers), "secret-key");
    // Fallback with ENV-like
    ca.claude_api_key = "backup-from-env";
    std::unordered_map<std::string, std::string> headers2;
    EXPECT_EQ(ca.get_api_key(headers2), "backup-from-env");
}

// Test message to prompt role conversion
TEST(ClaudeAdapterStatics, ConvertMessagesToPromptRoles) {
    ClaudeAdapter ca("url");
    std::vector<Message> messages = {
        {"user", "hello"},
        {"assistant", "hi!"},
        {"system", "sysmsg"}
    };
    std::string prompt = ca.convert_messages_to_prompt(messages);
    EXPECT_NE(prompt.find("\n\nHuman: hello"), std::string::npos);
    EXPECT_NE(prompt.find("\n\nAssistant: hi!"), std::string::npos);
    EXPECT_NE(prompt.find("\n\nHuman: hello"), std::string::npos); // user/system role both map 'Human'
    EXPECT_EQ(prompt.substr(prompt.size()-10), "Assistant:");
}

// openai_to_claude_params, patching methods
TEST(ClaudeAdapterStatics, OpenAIToClaudeParamsAll) {
    ClaudeAdapter ca;
    // Patch: convert_messages_to_prompt to always return PROMPT!
    ca.convert_messages_to_prompt_patch = [](const std::vector<Message>&) { return "PROMPT!"; };
    OpenAIParams oai{
        "gpt-3.5-turbo-0613",
        {},
        512,
        {"THE END"},
        0.3,
        true
    };
    model_map["gpt-3.5-turbo-0613"] = "claude-2";
    ClaudeParams params = ca.openai_to_claude_params(oai);
    EXPECT_EQ(params.model, "claude-2");
    EXPECT_EQ(params.prompt, "PROMPT!");
    EXPECT_EQ(params.max_tokens_to_sample, 512);
    ASSERT_EQ(params.stop_sequences.size(), 1);
    EXPECT_EQ(params.stop_sequences[0], "THE END");
    EXPECT_DOUBLE_EQ(params.temperature, 0.3);
    EXPECT_TRUE(params.stream);
}

// Partial parameters falling back (missing model)
TEST(ClaudeAdapterStatics, OpenAIToClaudeParamsPartial) {
    ClaudeAdapter ca;
    ca.convert_messages_to_prompt_patch = [](const std::vector<Message>&) { return "PROMPT!"; };
    OpenAIParams oai{
        "non-existent",
        {},
        -1,
        {},
        0.0,
        false
    };
    model_map.erase("non-existent");
    ClaudeParams params = ca.openai_to_claude_params(oai);
    EXPECT_EQ(params.model, "claude-2");
    EXPECT_EQ(params.prompt, "PROMPT!");
    EXPECT_EQ(params.max_tokens_to_sample, 100000);
}

// Test ClaudeToChatGPT response: stream
TEST(ClaudeAdapterStatics, ClaudeToChatGptResponseStream) {
    ClaudeAdapter ca;
    std::string test_completion = "Some completion text";
    std::string test_stop_reason = "stop_sequence";
    ca.num_tokens_from_string_patch = [](const std::string&) { return 5; };
    ResponseStream resp = ca.claude_to_chatgpt_response_stream({test_completion, test_stop_reason});
    EXPECT_EQ(resp.choices[0].delta_content, test_completion);
    EXPECT_EQ(resp.choices[0].finish_reason, stop_reason_map.at(test_stop_reason));
    EXPECT_EQ(resp.usage.completion_tokens, 5);
}

// Test ClaudeToChatGPT response: no stop given
TEST(ClaudeAdapterStatics, ClaudeToChatGptResponseNoStop) {
    ClaudeAdapter ca;
    std::string test_completion = "Some completion text";
    ca.num_tokens_from_string_patch = [](const std::string&) { return 5; };
    Response resp = ca.claude_to_chatgpt_response({test_completion});
    EXPECT_EQ(resp.choices[0].message_content, test_completion);
    EXPECT_EQ(resp.choices[0].finish_reason, "");
    EXPECT_EQ(resp.usage.completion_tokens, 5);
}

// Test message prompt formatting
TEST(ClaudeAdapterStatics, ConvertMessagesToPromptCorrectFormat) {
    ClaudeAdapter ca;
    std::vector<Message> messages = {{"user", "hi"}};
    std::string result = ca.convert_messages_to_prompt(messages);
    EXPECT_TRUE(result.find("\n\nHuman: hi") == 0);
    EXPECT_TRUE(result.size() >= 10 && result.substr(result.size() - 10) == "Assistant: ");
}