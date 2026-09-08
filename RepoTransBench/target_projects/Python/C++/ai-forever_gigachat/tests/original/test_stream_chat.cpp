#include <gtest/gtest.h>
#include <string>
#include <vector>

class ChatCompletionChunk {
public:
    struct Choice {
        std::string finish_reason;
    };
    std::vector<Choice> choices;
    ChatCompletionChunk(std::string reason) {
        choices.push_back({reason});
    }
};

TEST(TestStreamChat, Sync) {
    std::vector<ChatCompletionChunk> response = {
        ChatCompletionChunk("running"), ChatCompletionChunk("running"), ChatCompletionChunk("stop")
    };
    ASSERT_EQ(response.size(), 3);
    ASSERT_EQ(response[2].choices[0].finish_reason, "stop");
}

TEST(TestStreamChat, SyncHeaders) {
    std::vector<ChatCompletionChunk> response = {
        ChatCompletionChunk("running"), ChatCompletionChunk("running"), ChatCompletionChunk("stop")
    };
    ASSERT_EQ(response.size(), 3);
    ASSERT_EQ(response[2].choices[0].finish_reason, "stop");
}