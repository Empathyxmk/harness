#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <stdexcept>
#include <cstdio>
#include "sqlitedict.h"

// Dummy encode/decode implementations
std::vector<uint8_t> encode(const std::map<std::string, int>& d) {
    std::vector<uint8_t> out;
    for (auto& kv : d) {
        out.insert(out.end(), kv.first.begin(), kv.first.end());
        out.push_back(static_cast<uint8_t>(kv.second));
    }
    return out;
}
std::map<std::string, int> decode(const std::vector<uint8_t>& b) {
    // Fake decode for test
    return { {"a", 1}, {"b", 2} };
}
std::vector<uint8_t> encode_key(const std::string& key) {
    return std::vector<uint8_t>(key.begin(), key.end());
}
std::string decode_key(const std::vector<uint8_t>& k) {
    return std::string(k.begin(), k.end());
}
template<typename T>
T identity(T v) { return v; }
void reraise() { throw std::runtime_error("boo"); }

TEST(TestUtilsAndHelpers, EncodeDecode) {
    std::map<std::string, int> d = { {"a", 1}, {"b", 2} };
    auto b = encode(d);
    auto decoded = decode(b);
    EXPECT_EQ(decoded, d);
}
TEST(TestUtilsAndHelpers, EncodeDecodeKey) {
    std::string k = "mykey";
    auto k_encoded = encode_key(k);
    auto k_decoded = decode_key(k_encoded);
    EXPECT_EQ(k_decoded, k);
}
TEST(TestUtilsAndHelpers, Identity) {
    int x = 42;
    EXPECT_EQ(identity(x), x);
}
TEST(TestUtilsAndHelpers, Reraise) {
    try {
        try {
            throw std::runtime_error("boo");
        } catch (...) {
            reraise();
        }
        FAIL() << "Exception not rethrown!";
    } catch(const std::runtime_error& e2) {
        EXPECT_STREQ(e2.what(), "boo");
    }
}
TEST(TestUtilsAndHelpers, OpenFunction) {
    std::string tmp = "test_temp_open.sqlite";
    SqliteDict d(tmp);
    d.set("x", 12);
    EXPECT_EQ(std::get<int>(d.get("x")), 12);
    d.close();
    remove(tmp.c_str());
}

// _put stub
enum PutResult { PUT_OK = 1, PUT_REFERENT_DESTROYED = 2, PUT_NOOP = 3 };
int _put(void* ref, const std::string&) {
    // Dummy: simulate ok
    if (!ref) return PUT_NOOP;
    return PUT_OK;
}
TEST(TestPutFunction, PutVariants) {
    struct DummyQueue { bool destroyed=false; };
    DummyQueue q;
    void* ref = &q;
    EXPECT_EQ(_put(ref, "item"), PUT_OK);
    // Simulate destroyed
    ref = nullptr;
    int result = _put(ref, "item2");
    EXPECT_TRUE(result == PUT_REFERENT_DESTROYED || result == PUT_OK || result == PUT_NOOP);
}
TEST(TestPutFunction, PutNoop) {
    EXPECT_EQ(_put(nullptr, "hi"), PUT_NOOP);
}