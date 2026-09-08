#include <gtest/gtest.h>
#include <fstream>
#include <map>
#include <string>
#include "src/ai_models/checkpoint.h"

TEST(PublicCheckpoint, CreateAndLoad) {
    std::map<std::string, double> data{{"epoch", 7}, {"val_loss", 0.024}};
    std::string file_path = "cpoint_pub.pt";
    save_checkpoint(data, file_path);
    auto loaded = load_checkpoint(file_path);
    EXPECT_EQ(loaded["epoch"], 7);
    EXPECT_DOUBLE_EQ(loaded["val_loss"], 0.024);
    EXPECT_NE(loaded, std::map<std::string, double>{{"epoch", 10}, {"val_loss", 0.01}});
    std::remove(file_path.c_str());
}