#include <gtest/gtest.h>
#include <string>
#include <stdexcept>
#include <map>

// Stubs for API
namespace configuration {
    struct Configuration {
        std::string api_root;
        int retries = 0;
        Configuration(const std::string& root, int r) : api_root(root), retries(r) {}
    };

    class Factory {
    public:
        Factory(const std::string& root, int retries) : root_(root), retries_(retries) {}
        Configuration create() const { return Configuration(root_, retries_); }
    private:
        std::string root_;
        int retries_;
    };
}
namespace data {
    struct JsonApiResponse {
        static JsonApiResponse from_data(const std::map<std::string, std::string>&) { return JsonApiResponse(); }
        bool operator==(const JsonApiResponse&) const { return true; }
    };
}
namespace request_factory {
    struct ApiConnectionError : public std::exception {};
    class ApiRequestFactory {
    public:
        ApiRequestFactory(const configuration::Configuration& config)
            : config_(config), call_count(0) {}
        struct Response { data::JsonApiResponse content; };
        Response get(const std::string&) {
            ++call_count;
            if (simulate_timeout && call_count <= timeouts_before_success) {
                throw std::runtime_error("Timeout");
            }
            if (simulate_connection_error && call_count <= errors_before_fail) {
                throw ApiConnectionError();
            }
            return Response{data::JsonApiResponse::from_data(result_payload)};
        }

        void setTimeoutBehavior(int fail_count, std::map<std::string, std::string> result) {
            simulate_timeout = true;
            timeouts_before_success = fail_count;
            result_payload = result;
        }
        void setConnectionErrorBehavior(int fail_count) {
            simulate_connection_error = true;
            errors_before_fail = fail_count;
        }

        configuration::Configuration config_;
        int call_count = 0;
        bool simulate_timeout = false;
        int timeouts_before_success = 0;
        bool simulate_connection_error = false;
        int errors_before_fail = 0;
        std::map<std::string, std::string> result_payload;
    };
}

TEST(PublicRequestFactoryTest, test_get_public) {
    auto config = configuration::Factory("mockapi", 3).create();
    request_factory::ApiRequestFactory factory(config);
    factory.result_payload = { {"message", "created"} };
    auto response = factory.get("different_endpoint");
    EXPECT_EQ(response.content, data::JsonApiResponse::from_data({{"message", "created"}}));
}

TEST(PublicRequestFactoryTest, test_retrying_public) {
    auto config = configuration::Factory("mockapi", 3).create();
    request_factory::ApiRequestFactory factory(config);
    factory.setTimeoutBehavior(2, { {"message", "created"} });
    auto response = factory.get("another_endpoint");
    EXPECT_EQ(response.content, data::JsonApiResponse::from_data({ {"message", "created"} }));
}

TEST(PublicRequestFactoryTest, test_reraises_public) {
    auto config = configuration::Factory("mockapi", 3).create();
    request_factory::ApiRequestFactory factory(config);
    factory.setTimeoutBehavior(3, { {"message", "created"} });
    EXPECT_THROW({
        factory.get("fail_endpoint");
    }, std::runtime_error);
}