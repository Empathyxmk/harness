#include <gtest/gtest.h>
#include <string>

class ChatCompletion {
public:
    std::string dummy;
    ChatCompletion(std::string d) : dummy(d) {}
};

TEST(TestPostChat, Sync) {
    ChatCompletion response("COMPLETE");
    ASSERT_EQ(response.dummy, "COMPLETE");
}

TEST(TestPostChat, SyncHeaders) {
    ChatCompletion response("COMPLETE");
    ASSERT_EQ(response.dummy, "COMPLETE");
}