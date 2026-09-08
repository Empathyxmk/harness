#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include "src/lib/jsonrpc.h"

TEST(PublicJsonRpcTest, JsonRpcSuccessObj) {
    auto result = jsonrpc_success_obj("abcde", {{"value", 99}});
    EXPECT_EQ(result["jsonrpc"], "2.0");
    EXPECT_EQ(result["id"], "abcde");
    EXPECT_EQ(result["result"]["value"], 99);
}

TEST(PublicJsonRpcTest, JsonRpcErrorObj) {
    auto error = jsonrpc_error_obj("xyz01", -123, "Unexpected Error");
    EXPECT_EQ(error["jsonrpc"], "2.0");
    EXPECT_EQ(error["id"], "xyz01");
    auto err = error["error"];
    EXPECT_EQ(err["code"], -123);
    EXPECT_EQ(err["message"], "Unexpected Error");
}

TEST(PublicJsonRpcTest, JsonRpcErrorObjWithData) {
    auto error = jsonrpc_error_obj("ab10", -20, "Message", nlohmann::json({{"details", "extra"}}));
    EXPECT_EQ(error["jsonrpc"], "2.0");
    EXPECT_EQ(error["id"], "ab10");
    auto err = error["error"];
    EXPECT_EQ(err["code"], -20);
    EXPECT_EQ(err["message"], "Message");
    EXPECT_EQ(err["data"]["details"], "extra");
}