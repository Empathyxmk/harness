#include <gtest/gtest.h>
#include <map>
#include <string>
#include <vector>
#include "overholt/middleware.h"

using std::string;
using std::map;
using std::vector;

// DummyApp as a C++ callable
class DummyApp {
public:
    map<string, std::string> last_environ;
    std::vector<std::pair<string, string>> last_headers;

    std::vector<std::string> operator()(map<string, std::string>& environ, std::vector<std::pair<string, string>>& headers) {
        last_environ = environ;
        last_headers = headers;
        headers.push_back({"Content-Type", "text/plain"});
        return { "response" };
    }
};

static map<string, std::string> make_environ(
    const string& method = "POST",
    const string& query_string = "",
    const map<string, std::string>& extra_headers = {}) {

    map<string, std::string> environ;
    environ["REQUEST_METHOD"] = method;
    environ["QUERY_STRING"] = query_string;
    for (const auto& kv : extra_headers)
        environ[kv.first] = kv.second;
    return environ;
}

TEST(MiddlewareTest, MethodOverrideHeader) {
    DummyApp app;
    Overholt::HTTPMethodOverrideMiddleware middleware(&app);

    auto environ = make_environ("POST", "", {{"HTTP_X_HTTP_METHOD_OVERRIDE", "DELETE"}});
    vector<std::pair<string, string>> headers;
    std::vector<std::string> result = middleware(environ, headers);

    EXPECT_EQ(app.last_environ["REQUEST_METHOD"], "DELETE");
    EXPECT_TRUE(app.last_environ.find("CONTENT_LENGTH") != app.last_environ.end());
    ASSERT_EQ(result.size(), 1);
    EXPECT_EQ(result[0], "response");
    bool found = false;
    for (const auto& h : headers)
        if (h.first == "Content-Type" && h.second == "text/plain") found = true;
    EXPECT_TRUE(found);
}

TEST(MiddlewareTest, MethodOverrideQueryString) {
    DummyApp app;
    Overholt::HTTPMethodOverrideMiddleware middleware(&app);

    auto environ = make_environ("POST", "foo=bar&__METHOD__=PUT");
    vector<std::pair<string, string>> headers;
    std::vector<std::string> result = middleware(environ, headers);

    EXPECT_EQ(app.last_environ["REQUEST_METHOD"], "PUT");
    EXPECT_TRUE(app.last_environ.find("CONTENT_LENGTH") != app.last_environ.end());
    ASSERT_EQ(result.size(), 1);
    EXPECT_EQ(result[0], "response");
}

TEST(MiddlewareTest, NoOverride) {
    DummyApp app;
    Overholt::HTTPMethodOverrideMiddleware middleware(&app);

    auto environ = make_environ("GET");
    vector<std::pair<string, string>> headers;
    std::vector<std::string> result = middleware(environ, headers);
    EXPECT_EQ(app.last_environ["REQUEST_METHOD"], "GET");
    ASSERT_EQ(result.size(), 1);
    EXPECT_EQ(result[0], "response");
}

TEST(MiddlewareTest, OverrideWithCustom) {
    DummyApp app;
    Overholt::HTTPMethodOverrideMiddleware middleware(
        &app, "X-MY-HEADER", "__MY_METHOD__", {"PUT"});

    auto environ = make_environ("POST", "", {{"HTTP_X_MY_HEADER", "PUT"}});
    vector<std::pair<string, string>> headers;
    std::vector<std::string> result = middleware(environ, headers);

    EXPECT_EQ(app.last_environ["REQUEST_METHOD"], "PUT");
}

TEST(MiddlewareTest, OverrideNotAllowed) {
    DummyApp app;
    Overholt::HTTPMethodOverrideMiddleware middleware(&app, "X-HTTP-METHOD-OVERRIDE", "__METHOD__", {"POST"});

    auto environ = make_environ("POST", "", {{"HTTP_X_HTTP_METHOD_OVERRIDE", "PATCH"}});
    vector<std::pair<string, string>> headers;
    std::vector<std::string> result = middleware(environ, headers);

    EXPECT_EQ(app.last_environ["REQUEST_METHOD"], "POST");
}

TEST(MiddlewareTest, GetFromQuerystringReturnsNone) {
    DummyApp app;
    Overholt::HTTPMethodOverrideMiddleware middleware(&app);

    auto environ = make_environ("POST", "foo=bar");
    EXPECT_EQ(middleware._get_from_querystring(environ), "");
}