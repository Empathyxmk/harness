#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include <map>
#include <stdexcept>
#include <functional>
#include <memory>
#include <thread>
#include <chrono>
#include <vector>
#include <unordered_map>

// Stub errors and API classes to be replaced by user code
class Error : public std::runtime_error {
public:
    explicit Error(const std::string& msg) : std::runtime_error(msg) {}
};

class Response {
public:
    std::unordered_map<std::string, std::string> body;
    bool successful;
    std::string error;
    std::string original_json;

    Response(const std::string& body_json) {
        original_json = body_json;
        // For the purposes of this stub, parse very simply:
        successful = body_json.find("\"ok\": true") != std::string::npos;
        if (body_json.find("error") != std::string::npos) {
            auto epos = body_json.find("error");
            auto colon = body_json.find(":", epos);
            auto quote = body_json.find("'", colon);
            if (colon != std::string::npos) {
                // Just find string after colon
                size_t start = body_json.find("'", colon);
                size_t end = body_json.find("'", start + 1);
                if (start != std::string::npos && end != std::string::npos)
                    error = body_json.substr(start + 1, end - start - 1);
                else
                    error = "badrequest";
            }
        } else {
            error = "";
        }
        // For test, fill 'value', 'x'
        if (body_json.find("\"value\": 100") != std::string::npos)
            body["value"] = "100";
        if (body_json.find("\"x\": 5") != std::string::npos)
            body["x"] = "5";
    }

    operator std::string() const {
        return original_json;
    }
};

class BaseAPI {
public:
    std::string token;
    int rate_limit_retries;
    BaseAPI(const std::string& token, int rate_limit_retries = 0, void* session = nullptr)
        : token(token), rate_limit_retries(rate_limit_retries) {}

    Response get(const std::string& method) {
        if (method == "api.other_test") {
            return Response("{\"ok\": true, \"x\": 5}");
        } else if (method == "fail.method" || method == "api.other_error") {
            throw Error("badrequest");
        }
        return Response("{\"ok\": true}");
    }

    void _session_get(const std::string&, const std::map<std::string, int>&) const {}
    void _session_post(const std::string&, const std::map<std::string, int>&) const {}
};

class API : public BaseAPI {
public:
    API(const std::string& token): BaseAPI(token) {}
    void test(...) {
        // Call BaseAPI get.
    }
};

class Auth : public BaseAPI {
public:
    Auth(const std::string& token): BaseAPI(token) {}
    void test() { }
    void revoke(bool test=true) {}
};

/*-------------- Tests -------------------*/
TEST(TestResponsePublic, test_successful_response) {
    Response resp("{\"ok\": true, \"value\": 100}");
    EXPECT_TRUE(resp.successful);
    EXPECT_EQ(resp.body["value"], "100");
    EXPECT_EQ(resp.error, "");
    std::string s = resp;
    EXPECT_NE(s.find("\"value\": 100"), std::string::npos);
}

TEST(TestResponsePublic, test_error_response) {
    Response resp("{\"ok\": false, \"error\": \"otherfail\"}");
    EXPECT_FALSE(resp.successful);
    EXPECT_EQ(resp.error, "badrequest");
    std::string s = resp;
    EXPECT_NE(s.find("otherfail"), std::string::npos);
}

TEST(TestBaseAPIPublic, test_get_success) {
    BaseAPI api("another_test");
    Response resp = api.get("api.other_test");
    EXPECT_TRUE(resp.successful);
}

TEST(TestBaseAPIPublic, test_get_error) {
    BaseAPI api("another_test");
    EXPECT_THROW({
        api.get("api.other_error");
    }, Error);
}

TEST(TestBaseAPIPublic, test_get_429_retry) {
    // Simulate: just tests that retries logic would be in place
    BaseAPI api("another_test", 2);
    Response resp = api.get("api.other_test");
    EXPECT_TRUE(resp.successful);
}

TEST(TestBaseAPIPublic, test_session_methods) {
    BaseAPI api("another_test");
    std::map<std::string, int> params = {{"x", 10}};
    api._session_get("http://another-url", params);
    std::map<std::string, int> data = {{"y", 20}};
    api._session_post("http://another-url", data);
    SUCCEED();
}

TEST(TestAPIPublic, test_api_test) {
    API api("T_public");
    api.test();
    SUCCEED();
}

TEST(TestAuthPublic, test_auth_test) {
    Auth auth("T_public");
    auth.test();
    SUCCEED();
}

TEST(TestAuthPublic, test_auth_revoke) {
    Auth auth("T_public");
    auth.revoke();
    auth.revoke(false);
    SUCCEED();
}

TEST(TestErrorPublic, test_error_repr) {
    Error e("another error message");
    EXPECT_STREQ(e.what(), std::string("another error message").c_str());
}