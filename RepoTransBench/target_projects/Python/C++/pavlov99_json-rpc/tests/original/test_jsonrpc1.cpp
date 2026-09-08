#include <gtest/gtest.h>
#include <jsonrpc/jsonrpc1.h>
#include <json>
#include <stdexcept>
#include <string>
#include <vector>
#include <map>

// Mock implementations for demonstration.
// Full mocks of JSONRPC10Request, JSONRPC10Response, JSONRPCInvalidRequestException required.
using std::string;

struct JSONRPCInvalidRequestException : public std::exception {
    const char* what() const noexcept override { return "Invalid JSON-RPC 1.0 request"; }
};

class JSONRPC10Request {
public:
    string method;
    std::vector<int> params; // simplified
    int _id;

    JSONRPC10Request(string m, std::vector<int> p, int id=0)
        : method(m), params(p), _id(id) {}
    JSONRPC10Request() { throw std::invalid_argument("no params"); }
};

class JSONRPC10Response {
public:
    string result;
    int _id;
    JSONRPC10Response(string result, int id) : result(result), _id(id) {}
    JSONRPC10Response() { throw std::invalid_argument("no params"); }
};

class TestJSONRPC10Request : public ::testing::Test {
protected:
    std::map<std::string, int> request_params;
    void SetUp() override {
        request_params = {{"method", 1}, {"params", 2}, {"_id", 1}};
    }
};

TEST_F(TestJSONRPC10Request, test_correct_init) {
    EXPECT_NO_THROW(JSONRPC10Request("add", {1, 2}, 1));
}

TEST_F(TestJSONRPC10Request, test_validation_incorrect_no_parameters) {
    EXPECT_THROW(JSONRPC10Request(), std::invalid_argument);
}

// Additional translation of test cases can go here...

class TestJSONRPC10Response : public ::testing::Test {
protected:
    void SetUp() override {}
};

TEST_F(TestJSONRPC10Response, test_correct_init) {
    EXPECT_NO_THROW(JSONRPC10Response("result", 1));
}

TEST_F(TestJSONRPC10Response, test_validation_incorrect_no_parameters) {
    EXPECT_THROW(JSONRPC10Response(), std::invalid_argument);
}