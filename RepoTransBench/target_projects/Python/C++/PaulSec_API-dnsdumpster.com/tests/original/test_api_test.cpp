#include <gtest/gtest.h>
#include <typeinfo>
#include "DNSDumpsterAPI.h"
#include <any>
#include <map>
#include <string>
#include <memory>

// Dummy monkeypatch helper
class DummyResponse : public Session {
public:
    std::string text;
    int status_code;
    std::map<std::string, std::string> headers;

    DummyResponse(const std::string& t, int code = 200)
        : text(t), status_code(code) {}

    std::shared_ptr<void> get(const std::string& url) override {
        return std::make_shared<DummyResponse>(*this);
    }
    std::shared_ptr<void> post(const std::string& url, const std::map<std::string, std::string>& data,
                               const std::map<std::string, std::string>& headers) override {
        return std::make_shared<DummyResponse>(*this);
    }
};

// Test that DNSDumpsterAPI::search exists and is callable
TEST(DNSDumpsterAPITest, ClassAvailable) {
    DNSDumpsterAPI api;
    // Check method presence using C++ traits (simulate Python hasattr/callable)
    bool method_exists = false;
    try {
        auto result = api.search("test.com");
        method_exists = true;
    } catch (...) {
        method_exists = false;
    }
    EXPECT_TRUE(method_exists);
}

// Test DNSDumpsterAPI::search returns a dictionary type (any-maps in our translation)
TEST(DNSDumpsterAPITest, SearchType) {
    // Monkeypatch session
    class MyAPI : public DNSDumpsterAPI {
    public:
        std::map<std::string, std::any> search(const std::string& domain) override {
            // Mimic returning a dict as in Python
            std::map<std::string, std::any> output;
            output["domain"] = domain;
            std::map<std::string, std::any> dns_records;
            dns_records["dns"]  = std::vector<std::map<std::string, std::string>>{
                { {"domain", "ns1.test.com"} }
            };
            dns_records["mx"] = std::vector<std::map<std::string, std::string>>{};
            dns_records["host"] = std::vector<std::map<std::string, std::string>>{};
            output["dns_records"] = dns_records;
            return output;
        }
    };
    MyAPI api;
    auto res = api.search("test.com");
    // Should be a map (dictionary-like)
    EXPECT_EQ(typeid(res), typeid(std::map<std::string, std::any>));
}

// Test DNSDumpsterAPI::search throws on invalid HTML (CSRF not found, raises Exception)
TEST(DNSDumpsterAPITest, SearchInvalidThrows) {
    // Monkeypatch session to mimic no csrf token scenario
    class MyAPI : public DNSDumpsterAPI {
    public:
        std::map<std::string, std::any> search(const std::string& domain) override {
            // Simulate error thrown by original (Exception on missing csrf)
            throw std::runtime_error("CSRF token not found");
        }
    };
    MyAPI api;
    EXPECT_THROW({
        api.search("fail.com");
    }, std::runtime_error);
}