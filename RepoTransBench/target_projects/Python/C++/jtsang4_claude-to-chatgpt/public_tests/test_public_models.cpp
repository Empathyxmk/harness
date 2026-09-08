#include <gtest/gtest.h>
#include <string>
#include "claude_to_chatgpt/models.h"

TEST(PublicModelsTest, ModelsListExists) {
    ASSERT_TRUE(models_list.size() > 0);
    for (const auto& m : models_list)
        ASSERT_TRUE(!m.empty());
}

TEST(PublicModelsTest, ModelMapExists) {
    ASSERT_TRUE(model_map.size() > 0);
    for (const auto& pair : model_map) {
        ASSERT_FALSE(pair.first.empty());
        ASSERT_FALSE(pair.second.empty());
    }
}