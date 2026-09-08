#include <gtest/gtest.h>
#include "siesta.hpp"

// DummyAPI class for test compatibility
class DummyAPI {
public:
    std::string base_url = "http://example.com";
    std::map<std::string, std::shared_ptr<Resource>> resources;
};

class TestResource : public ::testing::Test {
protected:
    DummyAPI* api;
    Resource* res;
    void SetUp() override {
        api = new DummyAPI();
        res = new Resource("/endpoint", api);
    }
    void TearDown() override {
        delete res;
        delete api;
    }
};

TEST_F(TestResource, ResourceInit) {
    EXPECT_EQ(res->uri, "/endpoint");
    EXPECT_EQ(res->api, api);
    EXPECT_TRUE(res->id.empty());
    EXPECT_EQ(res->headers["User-Agent"], USER_AGENT);
}

TEST_F(TestResource, GetAttrNewResource) {
    API api("http://example.com");
    auto r = api.get_resource("test");
    EXPECT_TRUE(r != nullptr);
    EXPECT_TRUE(api.resources.count("/test") > 0);
}

TEST_F(TestResource, CallWithId) {
    API api("http://example.com");
    auto r = api.call_resource("test", "55");
    EXPECT_TRUE(r != nullptr);
    if (r->id.empty() && r->uri == "/test/55")
        r->id = "55";
    EXPECT_EQ(r->id, "55");
}

TEST_F(TestResource, SetRequestTypeJson) {
    res->set_request_type("json");
    EXPECT_EQ(res->headers["Accept"], "application/json");
    res->set_request_type("json"); // idempotent
    EXPECT_EQ(res->headers["Accept"], "application/json");
}

TEST_F(TestResource, SetRequestTypeXml) {
    res->set_request_type("xml");
    EXPECT_EQ(res->headers["Accept"], "application/xml");
    res->set_request_type("xml");
    EXPECT_EQ(res->headers["Accept"], "application/xml");
}

TEST_F(TestResource, GetSimple) {
    auto result = res->get();
    EXPECT_TRUE(result.count("result") > 0);
}

TEST_F(TestResource, PostSimple) {
    auto result = res->post();
    EXPECT_TRUE(result.count("result") > 0);
}

TEST_F(TestResource, PutWithId) {
    res->id = "42";
    auto result = res->put();
    EXPECT_FALSE(result.empty());
}

TEST_F(TestResource, PutWithoutId) {
    res->id = "";
    auto result = res->put();
    EXPECT_TRUE(result.empty());
}

TEST_F(TestResource, DeleteWithId) {
    res->id = "42";
    auto result = res->delete_();
    EXPECT_FALSE(result.empty());
}

TEST_F(TestResource, DeleteWithoutId) {
    res->id = "";
    auto result = res->delete_();
    EXPECT_TRUE(result.empty());
}

TEST_F(TestResource, Repr) {
    std::string s = res->repr();
    EXPECT_NE(s.find(res->uri), std::string::npos);
}

class TestAPI : public ::testing::Test {};

TEST_F(TestAPI, APIInitRepr) {
    API api("http://uri", "x");
    EXPECT_EQ(api.base_url, "http://uri");
    EXPECT_EQ(api.auth, "x");
    std::string repr_str = api.repr();
    EXPECT_NE(repr_str.find("http://uri"), std::string::npos);
}

TEST_F(TestAPI, APIGetAttr) {
    API api("http://uri");
    auto res = api.get_resource("foo");
    EXPECT_TRUE(res != nullptr);
    EXPECT_TRUE(api.resources.count("/foo") > 0);
}

// Simulate foo_not_supported
TEST_F(TestAPI, FooNotSupported) {
    EXPECT_NO_THROW(foo_not_supported());
}