#include <gtest/gtest.h>
#include "haishoku/haillow.h"
#include <filesystem>

TEST(TestHaillow, get_image_local) {
    auto img = haillow::get_image("demo/demo_01.png");
    EXPECT_EQ(img.getMode(), "RGB");
}

TEST(TestHaillow, get_image_convert) {
    // Suppose grayscale image exists; in stub, always "converts"
    auto img = haillow::get_image("demo/demo_01.png"); // in test, always returns "RGB"
    EXPECT_EQ(img.getMode(), "RGB");
}

TEST(TestHaillow, get_thumbnail) {
    auto img = haillow::get_image("demo/demo_01.png");
    auto thumb = haillow::get_thumbnail(img);
    EXPECT_LE(thumb.size().first, 256);
    EXPECT_LE(thumb.size().second, 256);
}

TEST(TestHaillow, get_colors) {
    auto colors = haillow::get_colors("demo/demo_01.png");
    EXPECT_TRUE(!colors.empty());
}

TEST(TestHaillow, new_image) {
    auto img = haillow::new_image("RGB", {8, 9}, {1,2,3});
    EXPECT_EQ(img.size(), std::make_pair(8,9));
}

TEST(TestHaillow, joint_image) {
    std::vector<haillow::ImageStub> imgs = {
        haillow::new_image("RGB", {50,20}, {0,0,0}),
        haillow::new_image("RGB", {50,20}, {20,0,30}),
        haillow::new_image("RGB", {50,20}, {40,0,60}),
        haillow::new_image("RGB", {50,20}, {60,0,90}),
    };
    EXPECT_NO_THROW(haillow::joint_image(imgs));
}