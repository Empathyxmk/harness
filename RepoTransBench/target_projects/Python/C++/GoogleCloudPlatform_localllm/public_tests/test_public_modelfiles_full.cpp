#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <algorithm>

namespace {

std::vector<std::string> public_find_llmfiles(const std::string&) {
    // Simulate test directory contents
    return {"lion.Q4_0.gguf", "giraffe.Q8_0.gguf"};
}

bool is_llmfile(const std::string& fname) {
    return fname.size() > 5 && fname.substr(fname.size()-5) == ".gguf";
}

TEST(TestPublicModelFilesFull, PublicFindLlmFiles) {
    std::string test_dir = "/tmp/some-llm-model-dir";
    auto output = public_find_llmfiles(test_dir);
    ASSERT_TRUE(std::any_of(output.begin(), output.end(), [](const std::string& f){return f.find(".gguf") != std::string::npos;}));
    std::string joined;
    for (const auto& x : output) joined += x;
    ASSERT_NE(joined.find("lion.Q4_0.gguf"), std::string::npos);
}

TEST(TestPublicModelFilesFull, PublicIsLlmfile) {
    ASSERT_TRUE(is_llmfile("rhino.Q7_0.gguf"));
    ASSERT_FALSE(is_llmfile("zebra.txt"));
}

} // namespace