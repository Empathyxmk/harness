#include <gtest/gtest.h>
#include <cstdlib>
#include <fstream>
#include <sys/stat.h>
#include "jp_wrapper.h"

static bool jp_exists() {
    struct stat s;
    return stat("./jp", &s) == 0 && (s.st_mode & S_IFREG) && (s.st_mode & S_IXUSR);
}

class PublicJpWrapperTest : public ::testing::Test {
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

TEST_F(PublicJpWrapperTest, PublicBasicSelect) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"alpha", make_obj({{"beta", make_int(9)}})}});
    JPValueHolder result = jp.search("alpha.beta", data);
    ASSERT_TRUE(std::holds_alternative<int>(result.value));
    EXPECT_EQ(std::get<int>(result.value), 9);
}

TEST_F(PublicJpWrapperTest, PublicIdentityQuery) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"bar", make_int(17)}});
    JPValueHolder result = jp.search("@", data);
    ASSERT_TRUE(std::holds_alternative<std::map<std::string, JPValueHolder>>(result.value));
    auto& mp = std::get<std::map<std::string, JPValueHolder>>(result.value);
    ASSERT_EQ(mp.size(), 1);
    ASSERT_TRUE(mp.count("bar") > 0);
    ASSERT_TRUE(std::holds_alternative<int>(mp["bar"].value));
    EXPECT_EQ(std::get<int>(mp["bar"].value), 17);
}

TEST_F(PublicJpWrapperTest, PublicListIndex) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"numbers", make_arr({make_int(10), make_int(20), make_int(30)})}});
    JPValueHolder result = jp.search("numbers[2]", data);
    ASSERT_TRUE(std::holds_alternative<int>(result.value));
    EXPECT_EQ(std::get<int>(result.value), 30);
}

TEST_F(PublicJpWrapperTest, PublicInvalidQueryRaises) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"bar", make_int(987)}});
    EXPECT_THROW(jp.search("!!!", data), std::exception);
}

TEST_F(PublicJpWrapperTest, PublicNonJsonOutput) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"bar", make_int(7)}});
    JPValueHolder result = jp.search("bar", data);
    ASSERT_TRUE(std::holds_alternative<int>(result.value));
    EXPECT_EQ(std::get<int>(result.value), 7);
}

TEST_F(PublicJpWrapperTest, PublicCustomBinaryPath) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"a", make_str("b")}});
    JPValueHolder result = jp.search("a", data);
    ASSERT_TRUE(std::holds_alternative<std::string>(result.value));
    EXPECT_EQ(std::get<std::string>(result.value), "b");
}

TEST_F(PublicJpWrapperTest, PublicErrorOnMissingJp) {
    JpWrapper jp("./not-found-jp-bin");
    auto data = make_obj({{"bar", make_int(4)}});
    EXPECT_THROW(jp.search("bar", data), std::exception);
}

TEST_F(PublicJpWrapperTest, PublicEmptyResult) {
    JpWrapper jp("./jp");
    auto data = make_obj({{"alpha", make_obj({{"beta", make_int(1234)}})}});
    JPValueHolder result = jp.search("alpha.gamma", data);
    // Accept string "" or null
    bool ok = false;
    if (std::holds_alternative<std::string>(result.value))
        ok = std::get<std::string>(result.value).empty();
    if (std::holds_alternative<std::nullptr_t>(result.value))
        ok = true;
    EXPECT_TRUE(ok);
}