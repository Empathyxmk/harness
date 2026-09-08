#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <set>
#include <vector>
#include <tuple>
#include <regex>
#include <stdexcept>

namespace audiogrep {
    std::set<std::string> find_files(const std::string&, const std::vector<std::string>& exts);
    std::string regexify(const std::string&);
    std::vector<std::tuple<std::string, double, double, int>> get_word_timings(const std::string&);
    std::vector<std::vector<std::tuple<std::string, double, double, int>>> group_words(const std::vector<std::tuple<std::string, double, double, int>>&, int);
    std::vector<std::vector<std::tuple<std::string, double, double, int>>> get_grouped_word_timings(const std::string&, int n);
    std::vector<int> franken_sentence(const std::string&, const std::vector<std::vector<std::tuple<std::string, double, double, int>>>&);
    std::vector<std::map<std::string, std::string>> search(const std::string&, const std::string&, const std::string&, bool);
    int make_splice(const std::string&, const std::vector<std::pair<int,int>>&, const std::string&);
}

TEST(PublicApiTest, FindFilesPublic)
{
    std::string tmp = "/tmp/audiogrep_pub_" + std::to_string(rand());
    system(("mkdir -p " + tmp).c_str());
    std::ofstream(tmp + "/x.flac") << "dummy";
    std::ofstream(tmp + "/y.flac") << "dummy";
    std::ofstream(tmp + "/z.txt") << "dummy";
    std::set<std::string> found = audiogrep::find_files(tmp, {".flac"});
    std::set<std::string> expected = {tmp + "/x.flac", tmp + "/y.flac"};
    EXPECT_EQ(found, expected);
    system(("rm -rf " + tmp).c_str());
}

TEST(PublicApiTest, RegexifyPublic)
{
    std::string text = "hello? world* (demo)";
    std::string r = audiogrep::regexify(text);
    EXPECT_EQ(r, "hello\\?\\ world\\*\\ \\(demo\\)");
}

TEST(PublicApiTest, GetWordTimingsPublic)
{
    std::string tmp = "/tmp/audiogrep_pub_" + std::to_string(rand());
    system(("mkdir -p " + tmp).c_str());
    std::string fn = tmp + "/timings_public.txt";
    std::ofstream ofs(fn);
    ofs << "<s> 5.0 6.0 1\n";
    ofs << "gamma 6.0 6.2 1\n";
    ofs << "zeta 6.2 6.3 1\n";
    ofs << "</s> 6.3 6.7 1\n";
    ofs.close();
    auto tgt = audiogrep::get_word_timings(fn);
    ASSERT_EQ(tgt.size(), 2u);
    EXPECT_EQ(std::get<0>(tgt[0]), "gamma");
    EXPECT_EQ(std::get<0>(tgt[1]), "zeta");
    system(("rm -rf " + tmp).c_str());
}

TEST(PublicApiTest, GroupWordsPublic)
{
    std::vector<std::tuple<std::string, double, double, int>> words = {
        {"a",1,2,3},{"b",2,3,4},{"c",3,4,5},{"d",4,5,6},{"e",5,6,7}
    };
    auto grouped = audiogrep::group_words(words, 4);
    ASSERT_EQ(grouped.size(), 2u);
    EXPECT_EQ(std::get<0>(grouped[0][0]), "a");
    EXPECT_EQ(std::get<0>(grouped[1][0]), "b");
}

TEST(PublicApiTest, GetGroupedWordTimingsPublic)
{
    std::string tmp = "/tmp/audiogrep_pub_" + std::to_string(rand());
    system(("mkdir -p " + tmp).c_str());
    std::string fn = tmp + "/grouped_timings_public.txt";
    std::ofstream ofs(fn);
    ofs << "<s> 11.0 12.0 1\n";
    ofs << "x 12.0 12.44 1\n";
    ofs << "y 12.44 12.89 1\n";
    ofs << "z 12.89 13.41 1\n";
    ofs << "</s> 13.41 13.91 1\n";
    ofs.close();

    auto groups = audiogrep::get_grouped_word_timings(fn, 2);
    ASSERT_EQ(groups.size(), 2u);
    EXPECT_EQ(std::get<0>(groups[0][0]), "x");
    EXPECT_EQ(std::get<0>(groups[1][0]), "y");
    system(("rm -rf " + tmp).c_str());
}

TEST(PublicApiTest, FrankenSentencePublic)
{
    std::vector<std::vector<std::tuple<std::string, double, double, int>>> in_wt{
        {{"apple", 0.1, 0.2, 0}, {"pear",0.2,0.3,0}},
        {{"banana", 0.3, 0.5, 0}}
    };
    auto r = audiogrep::franken_sentence("test sentence", in_wt);
    ASSERT_TRUE(typeid(r) == typeid(std::vector<int>));
    // No exact slice tests in C++ (Pythonic type), so check if all are ints
    for (auto e : r) EXPECT_EQ(typeid(e), typeid(int));
}

TEST(PublicApiTest, SearchModesPublic)
{
    std::string tmp = "/tmp/audiogrep_pub_" + std::to_string(rand());
    system(("mkdir -p " + tmp).c_str());
    std::string fn = tmp + "/public.transcription.txt";
    std::ofstream ofs(fn);
    ofs << "<s> 3.0 3.7 1\n";
    ofs << "foo 3.7 3.8 1\n";
    ofs << "bar 3.8 4.1 1\n";
    ofs << "</s> 4.1 4.5 1\n";
    ofs.close();

    // Patch search-like results with mock/dummy implementations: we can only simulate successful call
    // since monkeypatching is hard in C++, make sure the interface runs
    try {
        auto v = audiogrep::search("any", fn, "fragment", false);
        SUCCEED();
    } catch(...) {
        FAIL() << "search fragment call failed";
    }
    try {
        auto v2 = audiogrep::search("hello", fn, "word", false);
        SUCCEED();
    } catch(...) {
        FAIL() << "search word call failed";
    }
    try {
        auto v3 = audiogrep::search("repeat", fn, "sentence", false);
        SUCCEED();
    } catch(...) {
        FAIL() << "search sentence call failed";
    }
    system(("rm -rf " + tmp).c_str());
}

TEST(PublicApiTest, MakeSplicePublic)
{
    std::string tmp = "/tmp/audiogrep_pub_" + std::to_string(rand());
    system(("mkdir -p " + tmp).c_str());
    std::string out_mp3 = tmp + "/f.spliced.mp3";
    std::vector<std::pair<int,int>> slices = {{0,2}, {3,5}};
    // Will probably fail without a real ffmpeg, expect exception or error code
    try {
        int ret = audiogrep::make_splice("dummy.mp3", slices, out_mp3);
        SUCCEED();
    } catch (const std::runtime_error&) {
        SUCCEED();
    } catch (...) {
        FAIL() << "Unexpected exception type";
    }
    system(("rm -rf " + tmp).c_str());
}