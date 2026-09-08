#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <stdexcept>
#include <algorithm>
#include <memory>
#include <set>

// ------------------ Minimal stub/mock API integration harness ------------------
// This simulates a realistic "blackbox" API, as integration tests might interact with.

namespace tiddl {

// Let's use the same ApiClient from the unit test, but with expanded methods for integration.
class ApiClient {
public:
    struct Resource {
        std::string name;
        int id;
        Resource(const std::string& n, int i) : name(n), id(i) {}
        bool operator==(const Resource& other) const { return id == other.id && name == other.name; }
    };

    std::string current_user;
    bool authenticated = false;
    int resource_next_id = 1;
    std::vector<Resource> resources;

    ApiClient() = default;

    void login(const std::string& username, const std::string& password) {
        if (username == "user" && password == "pass123") {
            authenticated = true;
            current_user = username;
        } else {
            throw std::invalid_argument("Authentication failed");
        }
    }

    void logout() {
        authenticated = false;
        current_user = "";
    }

    Resource create_resource(const std::string& name) {
        if (!authenticated) throw std::runtime_error("Not authenticated");
        Resource r(name, resource_next_id++);
        resources.push_back(r);
        return r;
    }

    std::vector<Resource> list_resources() const {
        if (!authenticated) throw std::runtime_error("Not authenticated");
        return resources;
    }

    Resource get_resource(int id) const {
        if (!authenticated) throw std::runtime_error("Not authenticated");
        for (const auto& r : resources)
            if (r.id == id) return r;
        throw std::out_of_range("Resource not found");
    }

    void delete_resource(int id) {
        if (!authenticated) throw std::runtime_error("Not authenticated");
        auto it = std::remove_if(resources.begin(), resources.end(), [id](const Resource& r) { return r.id == id; });
        if (it == resources.end()) throw std::out_of_range("Resource not found");
        resources.erase(it, resources.end());
    }
};

} // end namespace tiddl

// --------------------------- Integration Tests -------------------------------

using namespace tiddl;

TEST(ApiIntegration, AuthRequiredForAllOps) {
    ApiClient client;
    EXPECT_THROW(client.create_resource("shouldfail"), std::runtime_error);
    EXPECT_THROW(client.list_resources(), std::runtime_error);
    EXPECT_THROW(client.get_resource(1), std::runtime_error);
    EXPECT_THROW(client.delete_resource(1), std::runtime_error);
}

TEST(ApiIntegration, HappyPath_CRUD) {
    ApiClient client;
    client.login("user", "pass123");

    // Create a resource
    auto r1 = client.create_resource("alpha");
    EXPECT_EQ(r1.name, "alpha");
    EXPECT_GT(r1.id, 0);

    // List includes the new resource
    auto lst1 = client.list_resources();
    ASSERT_EQ(lst1.size(), 1);
    EXPECT_EQ(lst1[0].name, "alpha");
    EXPECT_EQ(lst1[0].id, r1.id);

    // Get by id
    auto geted = client.get_resource(r1.id);
    EXPECT_EQ(geted, r1);

    // Create another resource
    auto r2 = client.create_resource("beta");
    EXPECT_EQ(r2.name, "beta");
    auto lst2 = client.list_resources();
    ASSERT_EQ(lst2.size(), 2);
    std::set<std::string> names;
    for (const auto& r : lst2) names.insert(r.name);
    EXPECT_TRUE(names.count("alpha"));
    EXPECT_TRUE(names.count("beta"));

    // Delete resource
    client.delete_resource(r1.id);
    auto lst3 = client.list_resources();
    ASSERT_EQ(lst3.size(), 1);
    EXPECT_EQ(lst3[0].name, "beta");
    // verify get_resource throws for deleted id
    EXPECT_THROW(client.get_resource(r1.id), std::out_of_range);

    // Delete the last one, check empty
    client.delete_resource(r2.id);
    EXPECT_TRUE(client.list_resources().empty());
}

TEST(ApiIntegration, CannotLoginWithBadCredentials) {
    ApiClient client;
    EXPECT_THROW(client.login("user", "wrongpw"), std::invalid_argument);
    EXPECT_THROW(client.login("unknown", "pass123"), std::invalid_argument);
    EXPECT_FALSE(client.authenticated);
    // Try an operation, confirm throws
    EXPECT_THROW(client.create_resource("fail"), std::runtime_error);
}

TEST(ApiIntegration, LogoutDisablesAllOpsUntilLoginAgain) {
    ApiClient c;
    c.login("user", "pass123");
    auto r = c.create_resource("res");
    c.logout();
    EXPECT_FALSE(c.authenticated);
    EXPECT_THROW(c.create_resource("doesntmatter"), std::runtime_error);
    EXPECT_THROW(c.list_resources(), std::runtime_error);

    // Logging in again should work, but old resources are gone since user "reset"
    c.login("user", "pass123");
    EXPECT_TRUE(c.list_resources().empty());
}

TEST(ApiIntegration, GetOrDeleteNonexistentResourceThrows) {
    ApiClient c;
    c.login("user", "pass123");
    EXPECT_THROW(c.get_resource(99), std::out_of_range);
    EXPECT_THROW(c.delete_resource(77), std::out_of_range);
    EXPECT_TRUE(c.list_resources().empty());
}

// Sad cases with edge parameters
TEST(ApiIntegration, EdgeCase_DuplicateNamesAllowedButDifferentIds) {
    ApiClient c;
    c.login("user", "pass123");

    auto r1 = c.create_resource("dup");
    auto r2 = c.create_resource("dup");
    EXPECT_NE(r1.id, r2.id);
    EXPECT_EQ(r1.name, r2.name);

    auto v = c.list_resources();
    ASSERT_EQ(v.size(), 2);
    EXPECT_EQ(v[0].name, "dup");
    EXPECT_EQ(v[1].name, "dup");
}