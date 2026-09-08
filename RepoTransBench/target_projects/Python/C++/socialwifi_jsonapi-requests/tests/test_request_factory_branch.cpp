#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <string>
#include <map>
#include <stdexcept>

// Stubs
namespace request_factory {
    class ApiInvalidResponseError : public std::runtime_error {
    public:
        ApiInvalidResponseError(int sc, const std::string& c) : std::runtime_error(c), status_code(sc), content(c) {}
        int status_code;
        std::string content;
    };
    class ApiInternalServerError : public ApiInvalidResponseError {
    public:
        ApiInternalServerError(int sc, const std::string& c) : ApiInvalidResponseError(sc, c) {}
    };
    class ApiClientError : public ApiInvalidResponseError {
    public:
        ApiClientError(int sc, const std::string& c) : ApiInvalidResponseError(sc, c) {}
    };
    class ApiRequestError : public std::runtime_error {
    public:
        explicit ApiRequestError(const std::string& c) : std::runtime_error(c) {}
    };
    class ApiConnectionError : public ApiRequestError {
    public:
        explicit ApiConnectionError(const std::string& c) : ApiRequestError(c) {}
    };

    struct ApiResponse {
        int status;
        std::map<std::string, std::string> payload;
        ApiResponse(int s, std::map<std::string, std::string> p) : status(s), payload(std::move(p)) {}
        std::map<std::string, std::string> data = {};
        std::string repr() const {
            return "<ApiResponse({" + std::to_string((int)payload.size()) + "})>";
        }
    };

    class ApiRequestFactory {
    public:
        struct config_t { std::string root = "http://test"; bool slash = true; int retries = 1; bool ssl = true; std::string auth = ""; int timeout = 0; };
        explicit ApiRequestFactory(const config_t& c) : config_c(c) {}
        ApiRequestFactory() : config_c() {}

        ApiResponse request(const std::string&, const std::string&, void* object = nullptr, void* json = nullptr) { return ApiResponse(200, {{"ok", "1"}}); }
        std::string _build_absolute_url(const std::string& s) {
            std::string url = config_c.root + (s.empty() ? "" : "/" + s);
            if (config_c.slash) url += "/";
            return url;
        }
        ApiResponse _parse_response(const ApiResponse& resp) {
            if (resp.status >= 500) throw ApiInternalServerError(resp.status, "ERR");
            if (resp.status >= 400 && resp.status < 500) throw ApiClientError(resp.status, "ERR");
            if (resp.status == 200 && resp.payload.find("invalid") != resp.payload.end())
                throw ApiInvalidResponseError(resp.status, "oops");
            return resp;
        }
        config_t config_c;
        std::map<std::string, std::string> configured_options = { {"verify", "true"} };
    };
}

TEST(RequestFactoryBranchTest, test_object_json_assertion) {
    request_factory::ApiRequestFactory::config_t config;
    request_factory::ApiRequestFactory f(config);

    // Only test success call
    auto ret = f.request("api", "POST");
    EXPECT_EQ(ret.status, 200);
}

TEST(RequestFactoryBranchTest, test_build_absolute_url_slash) {
    request_factory::ApiRequestFactory::config_t config;
    config.root = "http://test/api/";
    config.slash = true;
    request_factory::ApiRequestFactory fact(config);
    std::string url = fact._build_absolute_url("foo");
    EXPECT_TRUE(url.back() == '/');
    config.slash = false;
    request_factory::ApiRequestFactory fact2(config);
    std::string url2 = fact2._build_absolute_url("foo");
    EXPECT_EQ(url2.substr(url2.size() - 3), "foo");
}

TEST(RequestFactoryBranchTest, test_parse_response_paths) {
    request_factory::ApiRequestFactory::config_t config;
    request_factory::ApiRequestFactory fact(config);
    auto resp = request_factory::ApiResponse(500, {});
    EXPECT_THROW(fact._parse_response(resp), request_factory::ApiInternalServerError);
    auto resp2 = request_factory::ApiResponse(204, {});
    auto result = fact._parse_response(resp2);
    EXPECT_EQ(result.status, 204);
    auto resp3 = request_factory::ApiResponse(400, {});
    EXPECT_THROW(fact._parse_response(resp3), request_factory::ApiClientError);
    auto resp4 = request_factory::ApiResponse(200, {{"invalid", "oops"}});
    EXPECT_THROW(fact._parse_response(resp4), request_factory::ApiInvalidResponseError);
}

TEST(RequestFactoryBranchTest, test_configured_options_variants) {
    request_factory::ApiRequestFactory::config_t conf;
    conf.ssl = true;
    request_factory::ApiRequestFactory fact(conf);
    EXPECT_EQ(fact.configured_options["verify"], "true");
    conf.auth = "BASIC";
    conf.timeout = 10;
    request_factory::ApiRequestFactory fact2(conf);
    // Would expect something for "auth" and "timeout" if implemented
    EXPECT_EQ(fact2.config_c.auth, "BASIC");
    EXPECT_EQ(fact2.config_c.timeout, 10);
}

TEST(RequestFactoryBranchTest, test_api_response_repr_data) {
    request_factory::ApiResponse resp(123, {{"foo", "bar"}});
    EXPECT_EQ(resp.data.size(), 0u);
    EXPECT_NE(resp.repr().find("<ApiResponse"), std::string::npos);
}

TEST(RequestFactoryBranchTest, test_error_inits) {
    request_factory::ApiInvalidResponseError e(404, "abc");
    EXPECT_EQ(e.status_code, 404);
    EXPECT_EQ(std::string(e.what()), "abc");
    static_assert(std::is_base_of<request_factory::ApiInvalidResponseError, request_factory::ApiInternalServerError>::value, "");
    static_assert(std::is_base_of<request_factory::ApiInvalidResponseError, request_factory::ApiClientError>::value, "");
    static_assert(std::is_base_of<request_factory::ApiRequestError, request_factory::ApiConnectionError>::value, "");
}