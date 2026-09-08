#include <gtest/gtest.h>
#include <vector>
#include <string>
#include <map>

TEST(PublicAssistantsTest, AssistantListBehavior) {
    std::vector<std::map<std::string, std::string>> assistants = {
        {{"id", "asst_753"}, {"name", "HelperA"}, {"desc", "Helps with numbers."}},
        {{"id", "asst_111"}, {"name", "HelperB"}, {"desc", "Helps with words."}}
    };
    ASSERT_EQ(assistants[0]["name"], "HelperA");
    ASSERT_TRUE(assistants[1]["desc"].find("Helps with") == 0);
}

TEST(PublicAssistantsTest, AssistantDetailFields) {
    std::map<std::string, std::string> assistant = {
        {"id", "asst_xyz"},
        {"name", "XBot"},
        {"desc", "Handles X-cases"}
    };
    ASSERT_TRUE(assistant.find("id") != assistant.end());
    ASSERT_TRUE(assistant.find("name") != assistant.end());
    ASSERT_EQ(assistant["desc"], "Handles X-cases");
}