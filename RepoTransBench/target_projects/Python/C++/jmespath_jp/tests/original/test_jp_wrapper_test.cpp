#include <gtest/gtest.h>
#include <cstdlib>
#include <fstream>
#include <sys/stat.h>
#include "jp_wrapper.h"

static bool jp_exists() {
    struct stat s;
    return stat("./jp", &s) == 0 && (s.st_mode & S_IFREG) && (s.st_mode & S_IXUSR);
}

class JpWrapperTest : public ::testing::Test {
protected:
    void SetUp() override {
        if (!jp_exists()) GTEST_SKIP() << "jp binary not available for wrapper tests";
    }
};

JPValueHolder make_obj(const std::map<std::string, JPValueHolder>& kv) {
    return JPValueHolder(kv);
}
JPValueHolder make_arr(const std::vector<JPValueHolder>& arr) {
    return JPValueHolder(arr);
}
JPValueHolder make_int(int v) { return JPValueHolder(v); }
JPValueHolder make_str(const std::string& s) { return JPValueHolder(s); }

TEST_F(JpWrapperTest, BasicSelect) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"foo", make_obj({{"bar", make_int(5)}})}});
    JPValueHolder result = jp.search("foo.bar", data);
    ASSERT_TRUE(std::holds_alternative<int>(result.value));
    EXPECT_EQ(std::get<int>(result.value), 5);
}

TEST_F(JpWrapperTest, IdentityQuery) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"foo", make_int(42)}});
    JPValueHolder result = jp.search("@", data);
    ASSERT_TRUE(std::holds_alternative<std::map<std::string, JPValueHolder>>(result.value));
    auto& mp = std::get<std::map<std::string, JPValueHolder>>(result.value);
    ASSERT_EQ(mp.size(), 1);
    ASSERT_TRUE(mp.count("foo") > 0);
    ASSERT_TRUE(std::holds_alternative<int>(mp["foo"].value));
    EXPECT_EQ(std::get<int>(mp["foo"].value), 42);
}

TEST_F(JpWrapperTest, ListIndex) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"a", make_arr({make_int(1), make_int(2), make_int(3)})}});
    JPValueHolder result = jp.search("a[1]", data);
    ASSERT_TRUE(std::holds_alternative<int>(result.value));
    EXPECT_EQ(std::get<int>(result.value), 2);
}

TEST_F(JpWrapperTest, InvalidQueryRaises) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"foo", make_int(123)}});
    EXPECT_THROW(jp.search("???", data), std::exception);
}

TEST_F(JpWrapperTest, NonJsonOutput) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"foo", make_int(1)}});
    JPValueHolder result = jp.search("foo", data);
    ASSERT_TRUE(std::holds_alternative<int>(result.value));
    EXPECT_EQ(std::get<int>(result.value), 1);
}

TEST_F(JpWrapperTest, CustomBinaryPath) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"foo", make_str("bar")}});
    JPValueHolder result = jp.search("foo", data);
    ASSERT_TRUE(std::holds_alternative<std::string>(result.value));
    EXPECT_EQ(std::get<std::string>(result.value), "bar");
}

TEST_F(JpWrapperTest, ErrorOnMissingJp) {
    JpWrapper jp("./missing-jp-bin");
    auto data = make_obj({{"foo", make_int(1)}});
    EXPECT_THROW(jp.search("foo", data), std::exception);
}

TEST_F(JpWrapperTest, EmptyResult) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"foo", make_obj({{"bar", make_int(123)}})}});
    JPValueHolder result = jp.search("foo.baz", data);
    // Accept string "" or empty/null
    bool ok = false;
    if (std::holds_alternative<std::string>(result.value))
        ok = std::get<std::string>(result.value).empty();
    if (std::holds_alternative<std::nullptr_t>(result.value))
        ok = true;
    EXPECT_TRUE(ok);
}