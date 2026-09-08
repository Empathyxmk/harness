#include <gtest/gtest.h>
#include <map>

// Dummy automation public API
namespace automation_module {
    std::map<std::string, int> get_progress(int progress_id) {
        return {{"progress", 42}};
    }
}

TEST(PublicAutomationTest, GetProgressDifferentData) {
    int progress_id = 7;
    auto response = automation_module::get_progress(progress_id);
    ASSERT_TRUE(response.find("progress") != response.end());
    ASSERT_TRUE(response.at("progress") != 0);
}