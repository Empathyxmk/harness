#include <gtest/gtest.h>
#include "pdf_redactor.hpp"
#include <functional>
#include <string>
#include <vector>
#include <map>

TEST(TestRedactorOptions, OptionsDefaults) {
    pdf_redactor::RedactorOptions opts;
    EXPECT_EQ(opts.input_stream, nullptr);
    EXPECT_EQ(opts.output_stream, nullptr);
    EXPECT_TRUE(opts.metadata_filters.empty());
    EXPECT_TRUE(opts.xmp_filters.empty());
    EXPECT_TRUE(opts.xmp_serializer == nullptr);
    EXPECT_TRUE(opts.content_filters.empty());
    std::vector<std::string> ref_glyphs = {"?", "#", "*", " "};
    EXPECT_EQ(opts.content_replacement_glyphs, ref_glyphs);
    EXPECT_TRUE(opts.link_filters.empty());
}

TEST(TestRedactorOptions, SettingOptions) {
    pdf_redactor::RedactorOptions opts;
    std::string input = "input";
    std::string output = "output";
    opts.input_stream = &input;
    opts.output_stream = &output;
    auto meta_lambda = [](const std::string& v) { return std::string("NewTitle"); };
    opts.metadata_filters["Title"].push_back(meta_lambda);
    opts.content_filters = {};
    auto link_lambda = [](const std::string& href, void* annotation) -> void* { return nullptr; };
    opts.link_filters.push_back(link_lambda);
    auto xmp_lambda = [](void* xml) -> void* { return nullptr; };
    opts.xmp_filters.push_back(xmp_lambda);
    auto serializer_lambda = [](void* xml) -> std::string { return "<xml />"; };
    opts.xmp_serializer = serializer_lambda;
    EXPECT_EQ(opts.input_stream, &input);
    EXPECT_EQ(opts.output_stream, &output);
    EXPECT_EQ(opts.metadata_filters["Title"].size(), 1);
    EXPECT_EQ(opts.link_filters[0]("href", nullptr), nullptr);
    EXPECT_EQ(opts.xmp_filters[0](nullptr), nullptr);
    EXPECT_EQ(opts.xmp_serializer(nullptr), "<xml />");
}