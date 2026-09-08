#include <gtest/gtest.h>
#include <tiddl/exceptions.h>

// To match python: err = ApiError(status=404, subStatus=0, userMessage='not found', errorCode=999, message='msg')
TEST(ApiErrorTest, StrReprFields) {
    ApiError err(404, 0, "not found", 999, "msg");
    std::string errStr = err.what();
    std::string errRepr = err.repr();
    EXPECT_NE(errStr.find("msg"), std::string::npos);   // 'msg' in str
    EXPECT_NE(errRepr.find("not found"), std::string::npos);
    EXPECT_EQ(err.status, 404);
    EXPECT_EQ(err.errorCode, 999);
    EXPECT_EQ(err.subStatus, 0);
    EXPECT_EQ(err.userMessage, "not found");
    EXPECT_EQ(err.message, "msg");
}

TEST(ApiErrorTest, MissingFields) {
    ApiError err(401, 0, "", 0, "");
    EXPECT_EQ(err.status, 401);
    EXPECT_TRUE(err.subStatus == 0);
    std::string repr = err.repr();
    EXPECT_NE(repr.find("userMessage"), std::string::npos);
    // Should not throw
}

TEST(ApiErrorTest, OnlyStatus) {
    ApiError err(502, 0, "", 0, "");
    EXPECT_EQ(err.status, 502);
}

TEST(ApiErrorTest, WithKwargs) {
    std::unordered_map<std::string, std::any> extra = { {"foo", std::string("bar")}, {"custom", std::string("cval")} };
    ApiError err(123, 0, "", 0, "", extra);
    EXPECT_TRUE(err.extra.count("foo") && err.extra.count("custom"));
    EXPECT_EQ(std::any_cast<std::string>(err.extra["foo"]), "bar");
    EXPECT_EQ(std::any_cast<std::string>(err.extra["custom"]), "cval");
}