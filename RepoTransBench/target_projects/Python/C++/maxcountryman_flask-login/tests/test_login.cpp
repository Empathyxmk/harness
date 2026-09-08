#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include <memory>
#include <functional>
#include <exception>
#include <stdexcept>
#include <optional>
#include <iostream>

// Mocks for core flask-login logic: user, session, login behavior.

// User class which simulates authentication and activity status.
class MockUser {
public:
    int id;
    bool active;
    bool authenticated;
    bool anonymous;

    MockUser(int id_, bool active_=true, bool authenticated_=true, bool anonymous_=false)
        : id(id_), active(active_), authenticated(authenticated_), anonymous(anonymous_) {}

    std::string get_id() const { return std::to_string(id); }
    bool is_active() const { return active; }
    bool is_authenticated() const { return authenticated; }
    bool is_anonymous() const { return anonymous; }
};

class AnonymousUser : public MockUser {
public:
    AnonymousUser() : MockUser(-1, false, false, true) {}
};

class Session {
public:
    std::map<std::string, std::string> data;
    bool contains(const std::string& key) const {
        return data.find(key) != data.end();
    }
    std::string& operator[](const std::string& key) {
        return data[key];
    }
    void erase(const std::string& key) {
        data.erase(key);
    }
    void clear() {
        data.clear();
    }
};

struct Request {
    Session session;
    bool was_fresh = true;
};

// Simulated login manager.
class LoginManager {
public:
    std::function<std::shared_ptr<MockUser>(const std::string&)> user_loader;
    std::function<std::shared_ptr<MockUser>(const std::string&)> request_loader;
    std::string session_key = "user_id";
    std::function<void()> on_login;
    std::function<void()> on_logout;
    std::function<void()> on_refresh;

    LoginManager() { }

    void set_user_loader(std::function<std::shared_ptr<MockUser>(const std::string&)> f) {
        user_loader = f;
    }
    void set_request_loader(std::function<std::shared_ptr<MockUser>(const std::string&)> f) {
        request_loader = f;
    }
};

// Global state for this "test flask app"
struct MockFlaskApp {
    LoginManager login_manager;
    std::map<std::string, std::shared_ptr<MockUser>> users;
    Request request;
    std::optional<std::shared_ptr<MockUser>> current_user;
    std::string message;

    MockFlaskApp() {
        login_manager.session_key = "user_id";
        // By default, anonymous if not loaded.
        current_user.reset();

        login_manager.set_user_loader([this](const std::string& userid) -> std::shared_ptr<MockUser> {
            if(users.find(userid) != users.end()) {
                return users[userid];
            }
            return std::make_shared<AnonymousUser>();
        });
    }

    void add_user(int id, bool active=true, bool authenticated=true) {
        users[std::to_string(id)] = std::make_shared<MockUser>(id, active, authenticated, false);
    }

    void login_user(int id, bool fresh=true) {
        auto user = users[std::to_string(id)];
        request.session[login_manager.session_key] = std::to_string(id);
        current_user = user;
        request.was_fresh = fresh;
        if (login_manager.on_login) login_manager.on_login();
    }
    void logout_user() {
        request.session.erase(login_manager.session_key);
        current_user = std::make_shared<AnonymousUser>();
        if (login_manager.on_logout) login_manager.on_logout();
    }
    void refresh_user() {
        if(!current_user.has_value() || (*current_user)->is_anonymous()) throw std::runtime_error("fresh_login_required");
        request.was_fresh = true;
        if (login_manager.on_refresh) login_manager.on_refresh();
    }

    std::shared_ptr<MockUser> get_current_user() {
        if (!current_user.has_value()) {
            std::string user_id = request.session.contains(login_manager.session_key) ?
                                  request.session[login_manager.session_key] : "";
            if (user_id != "") {
                current_user = login_manager.user_loader(user_id);
            } else {
                current_user = std::make_shared<AnonymousUser>();
            }
        }
        return *current_user;
    }
};

//
// Unit Tests
//

class LoginTest : public ::testing::Test {
protected:
    MockFlaskApp app;

    void SetUp() override {
        app = MockFlaskApp();
        app.add_user(1, true, true);  // active authenticated
        app.add_user(2, true, false); // active *not* authenticated
        app.add_user(3, false, true); // inactive authenticated
        app.current_user.reset();
    }
};

TEST_F(LoginTest, LoginSetsSessionAndCurrentUser) {
    app.login_user(1);
    EXPECT_EQ(app.request.session[app.login_manager.session_key], "1");
    auto u = app.get_current_user();
    ASSERT_TRUE(u->is_authenticated());
    ASSERT_TRUE(u->is_active());
    ASSERT_FALSE(u->is_anonymous());
    EXPECT_EQ(u->get_id(), "1");
}

TEST_F(LoginTest, LogoutClearsSessionAndSetsAnonymous) {
    app.login_user(1);
    app.logout_user();
    EXPECT_FALSE(app.request.session.contains(app.login_manager.session_key));
    auto u = app.get_current_user();
    ASSERT_TRUE(u->is_anonymous());
    ASSERT_FALSE(u->is_authenticated());
    ASSERT_FALSE(u->is_active());
}

TEST_F(LoginTest, OnlyActiveUsersMayLogIn) {
    // Try login with inactive user
    // Override user_loader to forbid inactive login
    app.login_manager.set_user_loader([this](const std::string& userid) -> std::shared_ptr<MockUser> {
        auto it = app.users.find(userid);
        if (it != app.users.end() && it->second->is_active())
            return it->second;
        return std::make_shared<AnonymousUser>();
    });
    app.login_user(3);
    auto u = app.get_current_user();
    // Should not allow inactive login
    EXPECT_TRUE(u->is_anonymous());
}

TEST_F(LoginTest, AnonymousUserDefaultsWhenNotLoggedIn) {
    auto u = app.get_current_user();
    ASSERT_TRUE(u->is_anonymous());
}

TEST_F(LoginTest, UserIsFreshAtLoginButNotAfterSessionStale) {
    app.login_user(1, true);
    EXPECT_TRUE(app.request.was_fresh);
    // Simulate session reload where it is not "fresh"
    app.request.was_fresh = false;
    EXPECT_FALSE(app.request.was_fresh);
}

TEST_F(LoginTest, RefreshUserSetsFresh) {
    app.login_user(1, false);
    EXPECT_FALSE(app.request.was_fresh);
    app.refresh_user();
    EXPECT_TRUE(app.request.was_fresh);
}

TEST_F(LoginTest, RefreshNonLoggedInThrows) {
    app.current_user = std::make_shared<AnonymousUser>();
    EXPECT_THROW(app.refresh_user(), std::runtime_error);
}

TEST_F(LoginTest, OnLoginSignalCalled) {
    bool called = false;
    app.login_manager.on_login = [&]() { called = true; };
    app.login_user(1);
    EXPECT_TRUE(called);
}

TEST_F(LoginTest, OnLogoutSignalCalled) {
    bool called = false;
    app.login_manager.on_logout = [&]() { called = true; };
    app.login_user(1);
    app.logout_user();
    EXPECT_TRUE(called);
}

TEST_F(LoginTest, OnRefreshSignalCalled) {
    bool called = false;
    app.login_manager.on_refresh = [&]() { called = true; };
    app.login_user(1, false);
    app.refresh_user();
    EXPECT_TRUE(called);
}

TEST_F(LoginTest, SessionDoesNotLeakOtherKeys) {
    app.login_user(1);
    app.request.session["foo"] = "bar";
    app.logout_user();
    EXPECT_FALSE(app.request.session.contains("foo")); // logout_user only erases session for login
}

// Simulate endpoint protection logic
class EndpointProtector {
public:
    static bool login_required(const MockFlaskApp& app) {
        auto u = app.get_current_user();
        return (u->is_authenticated() && u->is_active());
    }
};

TEST_F(LoginTest, LoginRequiredBlocksAnonymous) {
    EXPECT_FALSE(EndpointProtector::login_required(app));
}

TEST_F(LoginTest, LoginRequiredAllowsLoggedIn) {
    app.login_user(1);
    EXPECT_TRUE(EndpointProtector::login_required(app));
}

TEST_F(LoginTest, LoginRequiredBlocksInactiveUser) {
    // Overwrite user_loader to allow fetching inactive but return them
    app.login_manager.set_user_loader([this](const std::string& userid) -> std::shared_ptr<MockUser> {
        auto it = app.users.find(userid);
        if(it != app.users.end()) return it->second;
        return std::make_shared<AnonymousUser>();
    });
    app.login_user(3);
    EXPECT_FALSE(EndpointProtector::login_required(app));
}

// Fresh login required simulation
class FreshProtector {
public:
    static bool fresh_login_required(const MockFlaskApp& app) {
        return app.request.was_fresh;
    }
};

TEST_F(LoginTest, FreshLoginRequiredBlocksStale) {
    app.login_user(1, false);
    EXPECT_FALSE(FreshProtector::fresh_login_required(app));
    app.refresh_user();
    EXPECT_TRUE(FreshProtector::fresh_login_required(app));
}

// Simulated unauthorized handler
TEST_F(LoginTest, UnauthorizedHandlerSetsMessage) {
    app.message = "";
    auto unauthorized = [&]() {
        app.message = "unauthorized!";
    };
    unauthorized();
    ASSERT_EQ(app.message, "unauthorized!");
}