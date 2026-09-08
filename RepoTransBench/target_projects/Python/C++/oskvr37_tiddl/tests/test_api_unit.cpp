#include <gtest/gtest.h>
#include <string>
#include <stdexcept>
#include <vector>
#include <algorithm>

// ------------------ Stub/mock core logic for API unit tests ------------------

namespace tiddl {

class ApiClient {
public:
    bool authenticated = false;
    std::vector<std::string> resource_list;
    ApiClient() : authenticated(false) {}

    void login(const std::string& username, const std::string& password) {
        if (username == "user" && password == "correctpass") {
            authenticated = true;
        } else {
            throw std::invalid_argument("Authentication failed");
        }
    }

    std::vector<std::string> list_resources() const {
        if (!authenticated) throw std::runtime_error("Not authenticated");
        return resource_list;
    }

    void add_resource(const std::string& resource) {
        if (!authenticated) throw std::runtime_error("Not authenticated");
        resource_list.push_back(resource);
    }

    void remove_resource(const std::string& resource) {
        if (!authenticated) throw std::runtime_error("Not authenticated");
        auto it = std::find(resource_list.begin(), resource_list.end(), resource);
        if (it != resource_list.end()) {
            resource_list.erase(it);
        } else {
            throw std::invalid_argument("Resource not found");
        }
    }
};

} // namespace tiddl

// ------------------- Actual Unit Tests ----------------------

using namespace tiddl;

TEST(ApiUnitTest, LoginSuccessAndFailure) {
    ApiClient client;

    // Good login
    EXPECT_NO_THROW(client.login("user", "correctpass"));
    EXPECT_TRUE(client.authenticated);

    // Already authenticated, another login (should succeed, no effect)
    EXPECT_NO_THROW(client.login("user", "correctpass"));
    EXPECT_TRUE(client.authenticated);

    // Bad login (throws)
    ApiClient client2;
    EXPECT_THROW(client2.login("user", "badpass"), std::invalid_argument);
    EXPECT_FALSE(client2.authenticated);
}

TEST(ApiUnitTest, ListResourcesRequiresAuth) {
    ApiClient c;
    // Not authenticated -> throws
    EXPECT_THROW(c.list_resources(), std::runtime_error);

    c.login("user", "correctpass");

    // After login, can list (empty at first)
    auto lst = c.list_resources();
    EXPECT_TRUE(lst.empty());
}

TEST(ApiUnitTest, AddAndRemoveResources) {
    ApiClient c;
    c.login("user", "correctpass");

    EXPECT_NO_THROW(c.add_resource("resA"));
    auto lst = c.list_resources();
    ASSERT_EQ(lst.size(), 1);
    EXPECT_EQ(lst[0], "resA");

    c.add_resource("resB");
    lst = c.list_resources();
    EXPECT_EQ(lst.size(), 2);
    EXPECT_EQ(lst[1], "resB");

    // Remove one
    EXPECT_NO_THROW(c.remove_resource("resA"));
    lst = c.list_resources();
    ASSERT_EQ(lst.size(), 1);
    EXPECT_EQ(lst[0], "resB");
}

TEST(ApiUnitTest, RemoveNonexistentResourceThrows) {
    ApiClient c;
    c.login("user", "correctpass");
    c.add_resource("resC");
    EXPECT_THROW(c.remove_resource("notfound"), std::invalid_argument);
}

TEST(ApiUnitTest, AddOrRemoveResourceWithoutAuthThrows) {
    ApiClient c;
    EXPECT_THROW(c.add_resource("ab"), std::runtime_error);
    EXPECT_THROW(c.remove_resource("ab"), std::runtime_error);
}

TEST(ApiUnitTest, ResourceListIndependentAcrossClients) {
    ApiClient c1, c2;
    c1.login("user", "correctpass");
    c2.login("user", "correctpass");

    c1.add_resource("AAA");
    c2.add_resource("BBB");
    auto a = c1.list_resources();
    auto b = c2.list_resources();
    EXPECT_EQ(a.size(), 1);
    EXPECT_EQ(a[0], "AAA");
    EXPECT_EQ(b.size(), 1);
    EXPECT_EQ(b[0], "BBB");
}