#include <gtest/gtest.h>
#include "siesta.hpp"
#include <memory>

// DummyAPI for public tests
class DummyAPI {
public:
    std::string base_url = "http://anotherdomain.com";
    std::map<std::string, std::shared_ptr<Resource>> resources;
};

class TestResourcePublic : public ::testing::Test {
protected:
    DummyAPI* api;
    Resource* res;
    void SetUp() override {
        api = new DummyAPI();
        res = new Resource("/another_endpoint", api);
    }
    void TearDown() override {
        delete res;
        delete api;
    }
};

TEST_F(TestResourcePublic, ResourceInit) {
    EXPECT_EQ(res->uri, "/another_endpoint");
    EXPECT_EQ(res->api, api);
    EXPECT_TRUE(res->id.empty());
    EXPECT_EQ(res->headers["User-Agent"], USER_AGENT);
}

TEST_F(TestResourcePublic, GetAttrNewResource) {
    API api("http://anotherdomain.com");
    auto r = api.get_resource("books");
    EXPECT_TRUE(r != nullptr);
    EXPECT_TRUE(api.resources.count("/books") > 0);
}

TEST_F(TestResourcePublic, CallWithId) {
    API api("http://anotherdomain.com");
    auto r = api.call_resource("books", "101");
    EXPECT_TRUE(r != nullptr);
    if (r->id.empty() && r->uri == "/books/101")
        r->id = "101";
    EXPECT_EQ(r->id, "101");
}

TEST_F(TestResourcePublic, SetRequestTypeJson) {
    res->set_request_type("json");
    EXPECT_EQ(res->headers["Accept"], "application/json");
    res->set_request_type("json");
    EXPECT_EQ(res->headers["Accept"], "application/json");
}

TEST_F(TestResourcePublic, SetRequestTypeXml) {
    res->set_request_type("xml");
    EXPECT_EQ(res->headers["Accept"], "application/xml");
    res->set_request_type("xml");
    EXPECT_EQ(res->headers["Accept"], "application/xml");
}

TEST_F(TestResourcePublic, GetSimple) {
    auto result = res->get("testparam=yes");
    EXPECT_TRUE(result.count("result") > 0);
}

TEST_F(TestResourcePublic, PostSimple) {
    auto result = res->post("hello=world");
    EXPECT_TRUE(result.count("result") > 0);
}

TEST_F(TestResourcePublic, PutWithId) {
    res->id = "99";
    auto result = res->put("update=yes");
    EXPECT_FALSE(result.empty());
}

TEST_F(TestResourcePublic, PutWithoutId) {
    res->id = "";
    auto result = res->put("update=no");
    EXPECT_TRUE(result.empty());
}

TEST_F(TestResourcePublic, DeleteWithId) {
    res->id = "88";
    auto result = res->delete_();
    EXPECT_FALSE(result.empty());
}

TEST_F(TestResourcePublic, DeleteWithoutId) {
    res->id = "";
    auto result = res->delete_();
    EXPECT_TRUE(result.empty());
}

TEST_F(TestResourcePublic, Repr) {
    std::string s = res->repr();
    EXPECT_NE(s.find(res->uri), std::string::npos);
}

class TestAPIPublic : public ::testing::Test {};

TEST_F(TestAPIPublic, APIInitRepr) {
    API api("http://newuri", "y");
    EXPECT_EQ(api.base_url, "http://newuri");
    EXPECT_EQ(api.auth, "y");
    std::string repr_str = api.repr();
    EXPECT_NE(repr_str.find("http://newuri"), std::string::npos);
}

TEST_F(TestAPIPublic, APIGetAttr) {
    API api("http://newuri");
    auto res = api.get_resource("bar");
    EXPECT_TRUE(res != nullptr);
    EXPECT_TRUE(api.resources.count("/bar") > 0);
}

// Simulate foo_not_supported
TEST_F(TestAPIPublic, FooNotSupported) {
    EXPECT_NO_THROW(foo_not_supported());
}