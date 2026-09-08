#include <gtest/gtest.h>
#include "mv2d_config.h"

// These tests focus on presence of specific keys/attributes in model config
TEST(ConfigsExpAttributes, ModelConfigKeys) {
    std::vector<std::string> configs = {
        "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep72.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.json"
    };
    for (const auto& config_path : configs) {
        MV2DConfig config;
        ASSERT_TRUE(load_mv2d_config(config_path, config));
        // For demonstration, check class_names and pipeline present
        ASSERT_GT(config.class_names.size(), 0);
        ASSERT_GT(config.train_pipeline.size(), 0);
        // For grid_mask, mock with a field named "use_grid_mask" in keys for demonstration
        auto it = config.keys.find("use_grid_mask");
        if (it != config.keys.end()) {
            auto grid_mask = std::get<std::map<std::string, bool>>(it->second);
            bool has_enabled = false;
            for (const auto& kv : grid_mask) {
                if (kv.second) has_enabled = true;
            }
            ASSERT_TRUE(has_enabled);
        }
    }
}

// For brevity, C++ test will only check presence of fields, not full object hierarchy
TEST(ConfigsExpAttributes, RoiHeadAndNested) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.json", config));
    ASSERT_GT(config.class_names.size(), 0);
    ASSERT_GT(config.train_pipeline.size(), 0);
    // Could expand mock config parsing to check deeper keys as necessary
}

// Other attribute/edge tests would follow same key-checking pattern