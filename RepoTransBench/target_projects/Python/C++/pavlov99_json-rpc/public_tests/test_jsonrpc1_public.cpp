#include <gtest/gtest.h>
#include <jsonrpc/jsonrpc1.h>
#include <string>
#include <vector>

class JSONRPC10Request {
public:
    std::string method;
    std::vector<int> params;
    int _id;
    // ...other fields as needed...

    JSONRPC10Request(std::string m, std::vector<int> p, int id = 0)
        : method(m), params(p), _id(id) {}
};

// Here is a sample public test case:
TEST(TestJSONRPC10RequestPublic, test_valid_request_object) {
    JSONRPC10Request req("add_public", {56, 34}, 101);
    EXPECT_EQ(req.method, "add_public");
    EXPECT_EQ(req.params[0], 56);
    EXPECT_EQ(req.params[1], 34);
    EXPECT_EQ(req._id, 101);
}

// More tests translated similarly...