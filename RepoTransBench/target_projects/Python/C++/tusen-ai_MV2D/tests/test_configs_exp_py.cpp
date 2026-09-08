#include <gtest/gtest.h>
#include "mv2d_config.h"

TEST(ConfigsExpPy, ConfigLoads) {
    std::vector<std::string> configs = {
        "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep72.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.json"
    };
    for (const auto& config_path : configs) {
        MV2DConfig config;
        ASSERT_TRUE(load_mv2d_config(config_path, config));
        ASSERT_GT(config.class_names.size(), 0);
        // Mock up fields for C++ since _base_ not mapped: just check that config loaded
    }
}