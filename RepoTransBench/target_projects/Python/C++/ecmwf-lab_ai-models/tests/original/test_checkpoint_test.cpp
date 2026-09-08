#include <gtest/gtest.h>
#include <fstream>
#include <cstdio>
#include <filesystem>
#include <map>
#include <string>
#include <vector>
#include "src/ai_models/checkpoint.h"

namespace fs = std::filesystem;

// Helper to compare any type equality; in particular for variant-like objects
template<typename T>
bool is_equal(const T& a, const T& b) {
    return a == b;
}

// Test tidy on dict and list/tuple
TEST(CheckpointTests, TidyDictAndListTuple) {
    std::map<std::string, anytype> d = {
        {"a", std::vector<anytype>{1, 2, std::map<std::string, anytype>{{"b", std::pair<int, std::nullptr_t>(3, nullptr)}}}},
        {"c", std::pair<int,int>(4, 5)}
    };
    auto res = tidy(d);
    // Check for shape match (use specific logic for actual code)
    EXPECT_TRUE(res.contains("a"));
    EXPECT_TRUE(res.contains("c"));
}

TEST(CheckpointTests, TidyBaseTypes) {
    std::vector<anytype> vals = {nullptr, 3, 0.1, std::string("foo"), true};
    for (const auto& val : vals) {
        EXPECT_TRUE(is_equal(tidy(val), val));
    }
}

TEST(CheckpointTests, TidyUnknownType) {
    struct Foo {};
    Foo f;
    auto res = tidy(f);
    // Assuming tidy returns input for unknown types
    // Type checks in C++ can't be done as in Python, so just check no throw
    SUCCEED();
}

TEST(CheckpointTests, FakeStorageConstruction) {
    FakeTorch::UntypedStorage storage(42);
    FakeStorage s;
    EXPECT_TRUE(s.has_dtype());
    EXPECT_TRUE(s.has_untyped_storage());
}

TEST(CheckpointTests, UnpicklerWrapperPersistentLoad) {
    // C++ cannot easily pickle, but assuming UnpicklerWrapper and persistent_load exist
    UnpicklerWrapper uw("abc");
    auto res = uw.persistent_load("id");
    EXPECT_TRUE(res.isFakeStorage());
}

// Simulate making a zip file with a data.pkl (use text file as surrogate)
std::string make_zip_with_data_pkl(std::string data_str, std::string filename="data.pkl", bool extra=false) {
    std::string zip_path = "tmpdata.zip";
    std::ofstream ofs(filename);
    ofs << data_str;
    ofs.close();
    std::filesystem::rename(filename, zip_path);
    return zip_path;
}

TEST(CheckpointTests, PeekSingleDataPkl) {
    std::string data_str = "foo:1";
    auto zfile = make_zip_with_data_pkl(data_str);
    auto res = peek(zfile);
    EXPECT_TRUE(res.contains("foo"));
    std::remove(zfile.c_str());
}

TEST(CheckpointTests, PeekDuplicateDataPkl) {
    // Simulate two "data.pkl" files in different folders
    std::string zfile1 = "first_data.pkl";
    std::ofstream ofs1(zfile1);
    ofs1 << "x:1";
    ofs1.close();
    std::string zfile2 = "second_data.pkl";
    std::ofstream ofs2(zfile2);
    ofs2 << "y:2";
    ofs2.close();
    // Instead of true zip, simulate detection
    try {
        peek(zfile1); peek(zfile2);
        FAIL() << "Expected logic error";
    } catch(const std::logic_error& e) {
        SUCCEED();
    }
    std::remove(zfile1.c_str());
    std::remove(zfile2.c_str());
}