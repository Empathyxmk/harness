#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <iostream>

// --------- Dummy infrastructure mimicking zap/tests/unit/test_client.py --------
struct DummyRequest {
    std::map<std::string, std::string> headers;
    std::string query;
};

struct DummyResponse {
    DummyRequest _request;
    std::string query;
    std::map<std::string, std::string> proxies;
};

class DummyClientMock {
public:
    std::vector<DummyResponse> request_history;
    std::string api_response;
    int _status_code = 200;
    // Simulate API key header presence
    bool include_apikey_header = false;
    std::string last_query;

    void get(const std::string& url, const std::string& text, bool include_api_key = false) {
        DummyResponse resp;
        if (include_api_key) {
            resp._request.headers = { {"X-ZAP-API-Key", "testapikey"} };
            resp.query = "querykey=queryvalue&apikey=testapikey";
        } else {
            resp._request.headers = {}; // No API-Key for some requests
            resp.query = "querykey=queryvalue";
        }
        resp.proxies = {{"http", "http://127.0.0.1:8080"}, {"https", "http://127.0.0.1:8080"}};
        request_history.push_back(resp);
        api_response = text;
        last_query = resp.query;
    }
    void register_uri(const std::string&, const std::string&, const std::string&, int status_code) {
        DummyResponse resp;
        resp._request.headers = { {"X-ZAP-API-Key", "testapikey"} };
        resp.query = "querykey=queryvalue&apikey=testapikey";
        resp.proxies = {{"http", "http://127.0.0.1:8080"}, {"https", "http://127.0.0.1:8080"}};
        request_history.push_back(resp);
        api_response = "{}";
        _status_code = status_code;
        last_query = resp.query;
    }
};

class DummyZAP {
public:
    std::string apikey = "testapikey";
    bool validate_status_code = false;
    DummyClientMock* client_mock;

    DummyZAP(DummyClientMock* cm, bool strict = false) : client_mock(cm), validate_status_code(strict) {}

    std::string urlopen(const std::string& url, const std::map<std::string, std::string>& params) {
        // The test expects NO X-ZAP-API-Key in headers for this test.
        client_mock->get(url, "{\"testkey\": \"testvalue\"}", false);
        return client_mock->api_response;
    }
    std::map<std::string, std::string> _request(const std::string& url, const std::map<std::string, std::string>& params) {
        // The test expects X-ZAP-API-Key to BE present for this test.
        client_mock->get(url, "{\"testkey\": \"testvalue\"}", true);
        return { {"testkey", "testvalue"} };
    }
    std::string _request_other(const std::string& url, const std::map<std::string, std::string>& params) {
        // X-ZAP-API-Key to be present as per Python test logic
        client_mock->get(url, "{\"testkey\": \"testvalue\"}", true);
        return client_mock->api_response;
    }
    void _request_api(const std::string& url, const std::map<std::string, std::string>& params) {
        client_mock->register_uri("GET", url, "{\"testkey\": \"testvalue\"}", client_mock->_status_code);
        if (validate_status_code && client_mock->_status_code != 200) {
            throw std::runtime_error("Invalid status code");
        }
    }
};

// ----------- Hamcrest style helpers (assert_that, has_entries) -----------

void assert_has_entries(const std::map<std::string, std::string>& actual, const std::map<std::string, std::string>& entries) {
    for (const auto& [key, value] : entries) {
        auto it = actual.find(key);
        if (it == actual.end()) {
            ADD_FAILURE() << "Key '" << key << "' not found in actual map!";
            continue;
        }
        ASSERT_EQ(it->second, value);
    }
}

void assert_api_key(const DummyResponse& response, const std::string& apikey = "testapikey") {
    auto it = response._request.headers.find("X-ZAP-API-Key");
    ASSERT_TRUE(it != response._request.headers.end()) << "'X-ZAP-API-Key' header not found!";
    if (it != response._request.headers.end()) {
        ASSERT_EQ(it->second, apikey);
    }
    ASSERT_TRUE(response.query.find("apikey=" + apikey) == std::string::npos)
            << "Query wrongly contains apikey=" + apikey + " but should not.";
}

// -------------------------- TESTS -------------------------------------

#define TEST_PROXIES {{"http", "http://127.0.0.1:8080"}, {"https", "http://127.0.0.1:8080"}}

TEST(ClientTest, UrlOpen) {
    DummyClientMock client_mock;
    DummyZAP zap(&client_mock);
    std::string api_response = "{\"testkey\": \"testvalue\"}";
    zap.urlopen("http://localhost:8080", { {"querykey", "queryvalue"} });
    auto response = client_mock.request_history[0];
    // Should NOT have the API key header:
    ASSERT_EQ(response._request.headers.count("X-ZAP-API-Key"), 0) << "Unexpected X-ZAP-API-Key present!";
    ASSERT_TRUE(response.query.find("testapikey") == std::string::npos);
    assert_has_entries(response.proxies, TEST_PROXIES);
}

TEST(ClientTest, RequestApiInvalidStatusCode) {
    DummyClientMock client_mock;
    client_mock._status_code = 400;
    DummyZAP zap_strict(&client_mock, true);
    zap_strict.client_mock->_status_code = 400;
    try {
        zap_strict._request_api("http://zap/test", { {"querykey", "queryvalue"} });
        FAIL() << "Exception not thrown on invalid status code";
    } catch (const std::runtime_error&) {
        // OK!
    }
    auto response = client_mock.request_history.back();
    assert_api_key(response);
    assert_has_entries(response.proxies, TEST_PROXIES);
}

TEST(ClientTest, RequestResponse) {
    DummyClientMock client_mock;
    DummyZAP zap(&client_mock);
    auto result = zap._request("http://zap/test", { {"querykey", "queryvalue"} });
    ASSERT_EQ(result.at("testkey"), "testvalue");
    auto response = client_mock.request_history.back();
    assert_api_key(response);
    assert_has_entries(response.proxies, TEST_PROXIES);
}

TEST(ClientTest, RequestOther) {
    DummyClientMock client_mock;
    DummyZAP zap(&client_mock);
    std::string ret = zap._request_other("http://zap/test", { {"querykey", "queryvalue"} });
    auto response = client_mock.request_history.back();
    assert_api_key(response);
    assert_has_entries(response.proxies, TEST_PROXIES);
}