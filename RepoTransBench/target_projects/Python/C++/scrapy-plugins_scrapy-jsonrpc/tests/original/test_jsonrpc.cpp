#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <stdexcept>
#include <string>
#include "src/lib/jsonrpc.h"

using json = nlohmann::json;

class DummyTarget {
public:
    int echo(const std::string& x) { return std::stoi(x); }
    int add(int a, int b) { return a + b; }
    void fail() { throw std::runtime_error("fail!"); }
};

json make_req(const std::string& method, std::optional<json> params = std::nullopt, int id = 1) {
    json d = {{"jsonrpc", "2.0"}, {"method", method}, {"id", id}};
    if (params.has_value())
        d["params"] = *params;
    return d.dump();
}

TEST(JsonRpcTest, JsonRpcResultAndErrorHelpers) {
    json result = jsonrpc_result(17, json::array({1,2}));
    EXPECT_EQ(result["jsonrpc"], "2.0");
    EXPECT_EQ(result["result"], json::array({1,2}));
    EXPECT_EQ(result["id"], 17);

    json e = jsonrpc_error(5, 1, "err", "trace");
    EXPECT_EQ(e["error"]["code"], 1);
    EXPECT_EQ(e["error"]["data"], "trace");
    EXPECT_EQ(e["id"], 5);
}

TEST(JsonRpcTest, JsonRpcServerCallSuccessListParams) {
    auto req = make_req("add", json::array({3,4}));
    auto result = jsonrpc_server_call(DummyTarget(), req);
    EXPECT_EQ(result["result"], 7);
}

TEST(JsonRpcTest, JsonRpcServerCallSuccessDictParams) {
    json params = {{"a", 10}, {"b", 7}};
    auto req = make_req("add", params);
    auto result = jsonrpc_server_call(DummyTarget(), req);
    EXPECT_EQ(result["result"], 17);
}

TEST(JsonRpcTest, JsonRpcServerCallSuccessEcho) {
    auto req = make_req("echo", json::array({"42"}));
    auto result = jsonrpc_server_call(DummyTarget(), req);
    EXPECT_EQ(result["result"], 42);
}

TEST(JsonRpcTest, JsonRpcServerCallInternalError) {
    auto req = make_req("fail");
    auto result = jsonrpc_server_call(DummyTarget(), req);
    EXPECT_EQ(result["error"]["code"], jsonrpc_errors::INTERNAL_ERROR);
    std::string msg = result["error"]["message"];
    EXPECT_NE(msg.find("fail!"), std::string::npos);
}

TEST(JsonRpcTest, JsonRpcServerCallParseError) {
    class BadDecoder {
    public:
        json decode(const std::string&) { throw std::runtime_error("parsefail"); }
    };
    BadDecoder decoder;
    auto res = jsonrpc_server_call(DummyTarget(), "badjson", &decoder);
    EXPECT_EQ(res["error"]["code"], jsonrpc_errors::PARSE_ERROR);
}

TEST(JsonRpcTest, JsonRpcServerCallInvalidRequest) {
    std::vector<json> bad = {
        json({{"jsonrpc", "2.0"}}),
        json({{"jsonrpc", "2.0"}, {"id", 1}}),
        json({{"jsonrpc", "2.0"}, {"method", "echo"}})
    };
    for (const auto& req_json : bad) {
        auto req = req_json.dump();
        auto res = jsonrpc_server_call(DummyTarget(), req);
        EXPECT_EQ(res["error"]["code"], jsonrpc_errors::INVALID_REQUEST);
    }
}

TEST(JsonRpcTest, JsonRpcServerCallMethodNotFound) {
    auto req = make_req("notfound");
    auto res = jsonrpc_server_call(DummyTarget(), req);
    EXPECT_EQ(res["error"]["code"], jsonrpc_errors::METHOD_NOT_FOUND);
}

// Tests for jsonrpc_client_call left as placeholders – would require net mocking in C++