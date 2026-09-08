#include <gtest/gtest.h>
#include "claude_to_chatgpt/models.h"

// Ensure models_list is a std::vector
TEST(ModelsTest, ModelsListExists) {
    EXPECT_TRUE((std::is_same<decltype(models_list), std::vector<std::string>>::value));
}

// Ensure model_map is a std::unordered_map or std::map
TEST(ModelsTest, ModelMapExists) {
    EXPECT_TRUE((std::is_same<decltype(model_map), std::unordered_map<std::string, std::string>>::value));
}