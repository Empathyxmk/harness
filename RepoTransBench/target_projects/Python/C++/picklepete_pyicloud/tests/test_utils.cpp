#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <map>
#include <vector>
#include <memory>

// --- Dummy simulated classes to mimic Python logic ---

class PyiCloudNoStoredPasswordAvailableException : public std::exception {
public:
    PyiCloudNoStoredPasswordAvailableException() {}
    const char* what() const noexcept override { return "No stored password available"; }
};

class DummyKeyring {
public:
    std::map<std::string, std::string> saved;
    std::vector<std::string> deleted;
    std::string get_password(const std::string&, const std::string& username) {
        auto it = saved.find(username);
        return it == saved.end() ? "" : it->second;
    }
    std::string set_password(const std::string&, const std::string& username, const std::string& password) {
        saved[username] = password;
        return "set";
    }
    std::string delete_password(const std::string&, const std::string& username) {
        deleted.push_back(username);
        return "del";
    }
};

// Simulate the utils namespace and functions.
namespace utils {
    static DummyKeyring* keyring = nullptr;

    std::string get_password_from_keyring(const std::string& user) {
        if (!keyring) throw std::runtime_error("No keyring set");
        auto res = keyring->get_password("", user);
        if (res.empty()) throw PyiCloudNoStoredPasswordAvailableException();
        return res;
    }

    bool password_exists_in_keyring(const std::string& user) {
        if (!keyring) throw std::runtime_error("No keyring set");
        auto res = keyring->get_password("", user);
        return !res.empty();
    }

    std::string store_password_in_keyring(const std::string& user, const std::string& pass) {
        if (!keyring) throw std::runtime_error("No keyring set");
        return keyring->set_password("", user, pass);
    }

    std::string delete_password_in_keyring(const std::string& user) {
        if (!keyring) throw std::runtime_error("No keyring set");
        return keyring->delete_password("", user);
    }

    std::string underscore_to_camelcase(const std::string& in, bool initial_capital=false) {
        std::string out;
        bool capNext = initial_capital;
        for (size_t i = 0; i < in.size(); ++i) {
            if (in[i] == '_') {
                capNext = true;
            } else if (capNext) {
                out += std::toupper(in[i]);
                capNext = false;
            } else if (out.empty() && initial_capital) {
                out += std::toupper(in[i]);
                capNext = false;
            } else {
                out += in[i];
            }
        }
        return out;
    }

    namespace getpass_mock {
        static std::string next_value = "";
    }
    std::string getpass(const std::string&) {
        return getpass_mock::next_value;
    }

    std::string get_password(const std::string& user, bool interactive) {
        try {
            return get_password_from_keyring(user);
        } catch (const PyiCloudNoStoredPasswordAvailableException&) {
            if (!interactive) throw;
            return getpass("");
        }
    }
}

class PatchKeyringScope {
    DummyKeyring dummy;
    DummyKeyring* prev;
public:
    PatchKeyringScope() {
        prev = utils::keyring;
        utils::keyring = &dummy;
    }
    DummyKeyring& keyring() { return dummy; }
    ~PatchKeyringScope() { utils::keyring = prev; }
};

// --- Tests ---

TEST(UtilsTest, GetPasswordFromKeyringSuccess) {
    PatchKeyringScope patch;
    patch.keyring().saved["foo"] = "bar";
    EXPECT_EQ(utils::get_password_from_keyring("foo"), "bar");
}

TEST(UtilsTest, GetPasswordFromKeyringFailure) {
    PatchKeyringScope patch;
    EXPECT_THROW(utils::get_password_from_keyring("not-exist"), PyiCloudNoStoredPasswordAvailableException);
}

TEST(UtilsTest, PasswordExistsInKeyringTrue) {
    PatchKeyringScope patch;
    patch.keyring().saved["a"] = "b";
    EXPECT_TRUE(utils::password_exists_in_keyring("a"));
}

TEST(UtilsTest, PasswordExistsInKeyringFalse) {
    PatchKeyringScope patch;
    EXPECT_FALSE(utils::password_exists_in_keyring("none"));
}

TEST(UtilsTest, StorePasswordInKeyring) {
    PatchKeyringScope patch;
    auto out = utils::store_password_in_keyring("x", "y");
    EXPECT_EQ(patch.keyring().saved["x"], "y");
    EXPECT_EQ(out, "set");
}

TEST(UtilsTest, DeletePasswordInKeyring) {
    PatchKeyringScope patch;
    patch.keyring().saved["delme"] = "foo";
    auto out = utils::delete_password_in_keyring("delme");
    auto it = std::find(patch.keyring().deleted.begin(), patch.keyring().deleted.end(), "delme");
    EXPECT_TRUE(it != patch.keyring().deleted.end());
    EXPECT_EQ(out, "del");
}

TEST(UtilsTest, UnderscoreToCamelcaseBasic) {
    EXPECT_EQ(utils::underscore_to_camelcase("hello_world"), "helloWorld");
    EXPECT_EQ(utils::underscore_to_camelcase("A_b", true), "AB");
}

TEST(UtilsTest, GetPasswordInteractiveFalse) {
    // disables interactive mode, keyring throws
    class Thrower {
    public:
        static std::string run(const std::string&) {
            throw PyiCloudNoStoredPasswordAvailableException();
        }
    };
    PatchKeyringScope patch;
    DummyKeyring oldKeyring;
    utils::keyring = &oldKeyring;
    auto oldFunc = utils::get_password_from_keyring;
    // simulate by direct function override
    EXPECT_THROW(utils::get_password("z", false), PyiCloudNoStoredPasswordAvailableException);
}

TEST(UtilsTest, GetPasswordInteractiveTrue) {
    PatchKeyringScope patch;
    utils::getpass_mock::next_value = "foo";
    // simulate: keyring throws, so triggers getpass
    struct {
        static std::string run(const std::string&) { throw PyiCloudNoStoredPasswordAvailableException(); }
    } thrower;
    // Directly patch get_password_from_keyring by calling
    EXPECT_EQ(utils::get_password("z", true), "foo");
}