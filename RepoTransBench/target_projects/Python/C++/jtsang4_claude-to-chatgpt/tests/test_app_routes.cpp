#include <gtest/gtest.h>
#include <string>
#include "claude_to_chatgpt/app.h"

TEST(AppRoutesTest, V1ModelsRoute) {
    auto resp = app_get_v1_models();
    EXPECT_EQ(resp.status_code, 200);
    EXPECT_EQ(resp.object, "list");
    EXPECT_TRUE(resp.data_is_list);
}

// Async test is synchronous here for C++ stub/mock purposes.
TEST(AppRoutesTest, ChatCompletionNonStream) {
    DummyAdapter adapter;
    set_global_adapter(&adapter);
    auto resp = app_post_v1_chat_completions({"gpt-3.5-turbo-0613", {}, false});
    EXPECT_EQ(resp.status_code, 200);
    EXPECT_TRUE(resp.body_is_object);
}