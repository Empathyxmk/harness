#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>

// We'll mock the interface of audiogrep
// Assume a function in C++ like: std::vector<std::map<std::string, Any>> convert_timestamps(const std::vector<std::string>&)

namespace audiogrep {
    // Mocks of the main tested function (declare here for linkage, implemented by app)
    std::vector<std::map<std::string, std::vector<std::vector<std::string>>>> convert_timestamps(const std::vector<std::string>& filenames);
}

TEST(AudiogrepTest, ConvertTimestampsTest)
{
    // Use the expected test file - test.mp3.transcription.txt
    std::string basedir = TEST_SRCDIR; // Provided at build time if CMake is set up with -DTEST_SRCDIR=...
    std::string filename = basedir + "/audiogrep/tests/data/test.mp3.transcription.txt";
    
    std::vector<std::string> files = {filename};
    auto sentences = audiogrep::convert_timestamps(files);

    std::unordered_map<std::string, bool> words;
    for (const auto& sentence : sentences) {
        auto it = sentence.find("words");
        if (it != sentence.end()) {
            for (const auto& wvec : it->second) {
                if (!wvec.empty()) {
                    words[wvec[0]] = true;
                }
            }
        }
    }
    ASSERT_TRUE(words.count("fashion") > 0);
    ASSERT_EQ((int)sentences.size(), 9);
}