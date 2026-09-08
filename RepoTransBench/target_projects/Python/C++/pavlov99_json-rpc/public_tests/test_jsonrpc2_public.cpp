#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include "jsonrpc/jsonrpc2.h"
#include <memory>
#include <string>
#include <vector>
#include <map>

using nlohmann::json;

// Helper types and construction macros for batch
using std::string;
using std::vector;
using std::map;
using std::make_shared;
using std::shared_ptr;

// Assume these C++ classes were implemented similarly to their Python counterparts:

// JSONRPC20Request
// - Constructor: method (string), params (json), _id (string/int/null), is_notification (bool=false)
// - Fields: data (json), json (string), args (tuple, as vector<json>), etc.

// JSONRPC20Response
// - Constructor: result (json), error (json/null), _id (string/int/null)
// - Fields: data (json), json (string)

TEST(TestJSONRPC20RequestPublic, test_valid_request_object) {
    JSONRPC20Request req("publicMethod2", json::array({88, 22}), 99);
    EXPECT_EQ(req.data["method"], "publicMethod2");
    EXPECT_EQ(req.data["params"], json::array({88, 22}));
    EXPECT_EQ(req.data["id"], 99);
    EXPECT_EQ(req.data["jsonrpc"], "2.0");
}

TEST(TestJSONRPC20RequestPublic, test_notification) {
    JSONRPC20Request req("eventNotify", json::array({42}), nullptr, true);
    auto& data = req.data;
    EXPECT_EQ(data["method"], "eventNotify");
    EXPECT_EQ(data["params"], json::array({42}));
    EXPECT_TRUE(data.find("id") == data.end());
    EXPECT_EQ(data["jsonrpc"], "2.0");
}

TEST(TestJSONRPC20RequestPublic, test_params_types_list_and_dict) {
    JSONRPC20Request req("f2", json::array({13, 21}), 2);
    EXPECT_EQ(req.data["params"], json::array({13, 21}));
    JSONRPC20Request req2("f3", json({{"key", 51}, {"val", 999}}), "Gamma");
    EXPECT_EQ(req2.data["params"], json({{"key", 51}, {"val", 999}}));
}

TEST(TestJSONRPC20RequestPublic, test_params_none_is_ok) {
    // Accepts params=nullptr (so params not present)
    JSONRPC20Request req("has_none_params", nullptr, 1);
    EXPECT_TRUE(typeid(req).hash_code() == typeid(JSONRPC20Request).hash_code());
}

TEST(TestJSONRPC20RequestPublic, test_params_invalid_type) {
    EXPECT_THROW({
        JSONRPC20Request req("wrongtype", "notalistordict", "a");
    }, std::invalid_argument);
    EXPECT_THROW({
        JSONRPC20Request req("wrongtype", 21, "w");
    }, std::invalid_argument);
    EXPECT_THROW({
        JSONRPC20Request req("wrongtype", 42.13, "z");
    }, std::invalid_argument);
}

TEST(TestJSONRPC20RequestPublic, test_method_invalid_type) {
    EXPECT_THROW({
        JSONRPC20Request req(json(333), json::array(), nullptr);
    }, std::invalid_argument);
    EXPECT_THROW({
        JSONRPC20Request req(json::array({"m2"}), json::array(), nullptr);
    }, std::invalid_argument);
}

TEST(TestJSONRPC20RequestPublic, test_id_types) {
    ASSERT_NO_THROW({
        JSONRPC20Request req("fooPublic", json::array({10}), "alfa");
    });
    ASSERT_NO_THROW({
        JSONRPC20Request req("fooPublic", json::array({322}), 99);
    });
    ASSERT_NO_THROW({
        JSONRPC20Request req("fooPublic", json::array({1}), nullptr);
    });
    EXPECT_THROW({
        JSONRPC20Request req("fooPublic", json::array({42}), 5.55);
    }, std::invalid_argument);
    EXPECT_THROW({
        JSONRPC20Request req("fooPublic", json::array({23}), json::array({"not", "id"}));
    }, std::invalid_argument);
    EXPECT_THROW({
        JSONRPC20Request req("fooPublic", json::array({17}), json::array({"tuple"}));
    }, std::invalid_argument);
}

TEST(TestJSONRPC20RequestPublic, test_json_output) {
    JSONRPC20Request req("sumFun", json::array({9, 101}), 101);
    auto parsed = json::parse(req.to_json());
    EXPECT_EQ(parsed, req.data);
    EXPECT_EQ(parsed["method"], "sumFun");
    EXPECT_EQ(parsed["params"], json::array({9, 101}));
    EXPECT_EQ(parsed["id"], 101);
    EXPECT_EQ(parsed["jsonrpc"], "2.0");
}

TEST(TestJSONRPC20RequestPublic, test_notification_id) {
    JSONRPC20Request req("logevt", json::array(), "should_be_ignored", true);
    EXPECT_TRUE(req.data.find("id") == req.data.end());
}

TEST(TestJSONRPC20RequestPublic, test_args) {
    JSONRPC20Request req1("multi", json::array({7, 5}));
    EXPECT_EQ(req1.args.size(), 2);
    EXPECT_EQ(req1.args[0], 7);
    EXPECT_EQ(req1.args[1], 5);

    JSONRPC20Request req2("named", json({{"x", 1000}, {"y", 47}}));
    EXPECT_EQ(req2.args.size(), 0); // Named call translates to empty args tuple
}

// ---- Response Tests ----

TEST(TestJSONRPC20ResponsePublic, test_valid_response) {
    JSONRPC20Response resp("done", nullptr, 88);
    EXPECT_NO_THROW({
        JSONRPC20Response resp("done", nullptr, 88);
    });

    EXPECT_THROW({
        JSONRPC20Response resp2(nullptr, json("failReason"), "badid2");
    }, std::invalid_argument);

    json err_dict = {{"code", 7}, {"message", "Error7"}};
    EXPECT_NO_THROW({
        JSONRPC20Response resp3(nullptr, err_dict, "errtest200");
    });
}

TEST(TestJSONRPC20ResponsePublic, test_json_output) {
    JSONRPC20Response resp("result_val", nullptr, 123);
    auto parsed = json::parse(resp.to_json());
    EXPECT_EQ(parsed, resp.data);
    EXPECT_EQ(parsed["result"], "result_val");
    EXPECT_TRUE(parsed.find("error") == parsed.end());
    EXPECT_EQ(parsed["id"], 123);
    EXPECT_EQ(parsed["jsonrpc"], "2.0");

    json err_d = {{"code", 1001}, {"message", "Fail error"}};
    JSONRPC20Response resp2(nullptr, err_d, "failid");
    auto parsed2 = json::parse(resp2.to_json());
    EXPECT_EQ(parsed2["result"], nullptr);
    EXPECT_EQ(parsed2["error"], err_d);
    EXPECT_EQ(parsed2["id"], "failid");
    EXPECT_EQ(parsed2["jsonrpc"], "2.0");
}

TEST(TestJSONRPC20ResponsePublic, test_init_invalid) {
    EXPECT_THROW({
        JSONRPC20Response noargs;
    }, std::invalid_argument);
}

// ---- Batch Request Tests ----

TEST(TestJSONRPC20BatchRequestPublic, test_batch_request) {
    std::vector<JSONRPC20Request> items {
        JSONRPC20Request("applep", json::array({11, 32}), 1401),
        JSONRPC20Request("bananap", json({{"x", 45}}), "str901"),
        JSONRPC20Request("cucumberp", json::array(), nullptr)
    };
    JSONRPC20BatchRequest batch(items);
    auto data = batch.data;
    ASSERT_EQ(data.size(), 3);
    EXPECT_EQ(data[0]["method"], "applep");
    EXPECT_EQ(data[1]["method"], "bananap");
    EXPECT_EQ(data[2]["method"], "cucumberp");
}

TEST(TestJSONRPC20BatchRequestPublic, test_batch_request_json) {
    std::vector<JSONRPC20Request> items {
        JSONRPC20Request("funkey", json::array({99}), "sid1337"),
        JSONRPC20Request("bazbaz", json::array(), nullptr)
    };
    JSONRPC20BatchRequest batch(items);
    EXPECT_EQ(json::parse(batch.to_json()), batch.data);
}

TEST(TestJSONRPC20BatchRequestPublic, test_invalid_type) {
    EXPECT_THROW({
        std::vector<json> wrongvec { json("not_a_request"), json("object") };
        JSONRPC20BatchRequest batch(wrongvec); // should error
    }, std::invalid_argument);

    EXPECT_THROW({
        JSONRPC20Request req("should_fail", json::array({12}));
        JSONRPC20BatchRequest batch(req); // Not vector!
    }, std::invalid_argument);
}

// ---- Batch Response Tests ----

TEST(TestJSONRPC20BatchResponsePublic, test_batch_response) {
    std::vector<JSONRPC20Response> items {
        JSONRPC20Response("tangerine", nullptr, 134),
        JSONRPC20Response(nullptr, json({{"code", 4}, {"message", "peach"}}), "id1313")
    };
    JSONRPC20BatchResponse batch(items);
    auto data = batch.data;
    ASSERT_EQ(data.size(), 2);
    EXPECT_EQ(data[0]["result"], "tangerine");
    EXPECT_EQ(data[1]["error"], json({{"code", 4}, {"message", "peach"}}));
}

TEST(TestJSONRPC20BatchResponsePublic, test_batch_response_json) {
    std::vector<JSONRPC20Response> items {
        JSONRPC20Response("fooout", nullptr, "h321"),
        JSONRPC20Response(nullptr, json({{"code", 88}, {"message", "errormsg"}}), nullptr)
    };
    JSONRPC20BatchResponse batch(items);
    EXPECT_EQ(json::parse(batch.to_json()), batch.data);
}

TEST(TestJSONRPC20BatchResponsePublic, test_invalid_type) {
    EXPECT_THROW({
        std::vector<json> wrongvec { json("not_a_response"), json("object") };
        JSONRPC20BatchResponse batch(wrongvec); // should error
    }, std::invalid_argument);

    EXPECT_THROW({
        JSONRPC20Response resp("fail_batch", nullptr, 42);
        JSONRPC20BatchResponse batch(resp); // Not vector!
    }, std::invalid_argument);
}