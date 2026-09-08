#include <gtest/gtest.h>
#include "mv2d_config.h"

TEST(PublicConfigsExpAttributes, ModelConfigKeys) {
    std::vector<std::string> configs = {
        "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.json"
    };
    for (const auto& config_path : configs) {
        MV2DConfig config;
        ASSERT_TRUE(load_mv2d_config(config_path, config));
        ASSERT_GT(config.class_names.size(), 0);
        ASSERT_GT(config.train_pipeline.size(), 0);
        // grid_mask: ensure at least one enabled (simulate)
        auto it = config.keys.find("use_grid_mask");
        if (it != config.keys.end()) {
            auto grid_mask = std::get<std::map<std::string, bool>>(it->second);
            bool any_enabled = false;
            for (const auto& kv : grid_mask) {
                if (kv.second) any_enabled = true;
            }
            ASSERT_TRUE(any_enabled);
        }
    }
}