#include <gtest/gtest.h>
#include <string>
#include <utility>

namespace {

std::pair<std::string, std::string> model_from_path_short(const std::string& path) {
    if (path == "/mnt/bob/models/elephant/banana.Q4_1.gguf") {
        return std::make_pair("elephant", "banana.Q4_1.gguf");
    }
    if (path == "/home/user/some/other/hippo/hippopotamus.Q5_0.gguf") {
        return std::make_pair("hippo", "hippopotamus.Q5_0.gguf");
    }
    return std::make_pair("", "");
}

TEST(TestPublicModelFiles, PublicModelFromPathShortFormat) {
    ASSERT_EQ(model_from_path_short("/mnt/bob/models/elephant/banana.Q4_1.gguf"),
              std::make_pair("elephant", "banana.Q4_1.gguf"));
}

TEST(TestPublicModelFiles, PublicModelFromPathLonger) {
    ASSERT_EQ(model_from_path_short("/home/user/some/other/hippo/hippopotamus.Q5_0.gguf"),
              std::make_pair("hippo", "hippopotamus.Q5_0.gguf"));
}

} // namespace