#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <vector>

// Simulated Starlette-like HTTP/Plugin/Context objects for Pure ASGI middleware
namespace StarletteMock {

struct Response {
    int status_code;
    std::unordered_map<std::string, std::string> headers;
    std::string text;
};

struct Request {
    std::unordered_map<std::string, std::string> headers;
};

constexpr int HTTP_200_OK = 200;

struct HeaderKeys {
    static constexpr const char* correlation_id = "X-Correlation-ID";
    static constexpr const char* request_id = "X-Request-ID";
    static constexpr const char* user_agent = "User-Agent";
    static constexpr const char* forwarded_for = "X-Forwarded-For";
    static constexpr const char* date = "Date";
};

// Plugins simulated only by 'key' field for test text presence
struct Plugin {
    std::string key;
    Plugin(const std::string& k): key(k) {}
};

const std::vector<Plugin> plugins_to_use = {
    Plugin(HeaderKeys::correlation_id),
    Plugin(HeaderKeys::request_id),
    Plugin(HeaderKeys::user_agent),
    Plugin(HeaderKeys::forwarded_for),
    Plugin(HeaderKeys::date)
};

class RawContextMiddleware {
public:
    RawContextMiddleware(const std::vector<Plugin>& plugins): plugins_(plugins) {}
    Response handle(const Request& request) {
        // All plugins' key appears in the "body" text
        std::string txt = "{";
        for (const auto& p : plugins_) {
            txt += "\"" + p.key + "\": \"";
            auto it = request.headers.find(p.key);
            if (it != request.headers.end()) {
                txt += it->second;
            } else {
                txt += "generated";
            }
            txt += "\", ";
        }
        txt += "}";

        std::unordered_map<std::string, std::string> headers;
        for (const auto& p : plugins_) {
            // Simulate these keys are returned as headers
            headers[p.key] = "generated";
        }
        return Response{HTTP_200_OK, headers, txt};
    }
private:
    std::vector<Plugin> plugins_;
};

} // namespace StarletteMock

using namespace StarletteMock;


TEST(MiddlewarePureAsgi, ValidRequest) {
    RawContextMiddleware middleware(plugins_to_use);
    Request req;
    Response resp = middleware.handle(req);
    EXPECT_EQ(resp.status_code, HTTP_200_OK);

    // All keys present in "text"
    for (const auto& plugin : plugins_to_use) {
        EXPECT_NE(resp.text.find(plugin.key), std::string::npos);
    }

    EXPECT_TRUE(resp.headers.count(HeaderKeys::correlation_id));
    EXPECT_TRUE(resp.headers.count(HeaderKeys::request_id));
}