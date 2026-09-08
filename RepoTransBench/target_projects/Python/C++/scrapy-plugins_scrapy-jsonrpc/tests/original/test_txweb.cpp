#include <gtest/gtest.h>
#include <string>
#include <map>

#include "src/lib/txweb.h"

// DummyRequest simulates the request object with headers
class DummyRequest {
public:
    std::map<std::string, std::string> _headers;
    void setHeader(const std::string& k, const std::string& v) {
        _headers[k] = v;
    }
};

TEST(TxWebTest, JsonResourceRenderObjectSetsHeadersAndReturnsJson) {
    JsonResource jr;
    nlohmann::json obj = {{"foo", "bar"}};
    DummyRequest dr;
    std::string res = jr.render_object(obj, dr);

    EXPECT_TRUE(typeid(res) == typeid(std::string));
    std::string trimmed = res;
    // strip leading/trailing whitespaces (simulate .strip())
    trimmed.erase(0, trimmed.find_first_not_of(" \t\r\n"));
    trimmed.erase(trimmed.find_last_not_of(" \t\r\n") + 1);

    EXPECT_TRUE(trimmed.front() == '{' && trimmed.back() == '}');

    EXPECT_EQ(dr._headers["Content-Type"], "application/json");
    EXPECT_EQ(dr._headers["Access-Control-Allow-Origin"], "*");
    EXPECT_EQ(dr._headers["Access-Control-Allow-Methods"], "GET, POST, PATCH, PUT, DELETE");
    EXPECT_EQ(dr._headers["Access-Control-Allow-Headers"], " X-Requested-With");
    EXPECT_EQ(std::stoi(dr._headers["Content-Length"]), static_cast<int>(res.size()));
}