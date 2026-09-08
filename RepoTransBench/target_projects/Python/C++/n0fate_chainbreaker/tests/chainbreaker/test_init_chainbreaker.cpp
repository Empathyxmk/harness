#include <gtest/gtest.h>
#include <string>
#include <memory>
#include <type_traits>

class DummyDbBlob {
public:
    unsigned char Salt[8] = {0};
};

class DummyChainbreaker {
public:
    std::string _unlock_password;
    DummyDbBlob dbblob;
    bool _generated = false;
    std::unique_ptr<int> _unlock_key = nullptr;

    DummyChainbreaker() {
        _unlock_password = "pw";
        _generated = false;
        _unlock_key = nullptr;
    }

    std::string unlock_password() const {
        return _unlock_password;
    }
    void set_unlock_password(const std::string& value) {
        _unlock_password = value;
        _unlock_key = std::make_unique<int>(123);
        _generated = true;
    }

    static std::string logger;
    // simulate KeyError via throwing std::runtime_error
    void _get_table_from_type(int) { throw std::runtime_error("KeyError"); }
    std::string warned_msg;
    void dump_generic_passwords() {
        try { _get_table_from_type(0); }
        catch (...) { warned_msg = "[!] Generic Password Table is not available"; }
    }
    void dump_internet_passwords() {
        try { _get_table_from_type(0); }
        catch (...) { warned_msg = "[!] Internet Password Table is not available"; }
    }
};
std::string DummyChainbreaker::logger = "";

TEST(ChainbreakerTest, DummyKCAttrs) {
    DummyChainbreaker kc;
    kc.set_unlock_password("pw");
    ASSERT_TRUE(kc._generated);
    ASSERT_NE(kc._unlock_key, nullptr);
}

TEST(ChainbreakerTest, HasLogger) {
    ASSERT_TRUE(std::is_same<decltype(DummyChainbreaker::logger), std::string>::value);
}

TEST(ChainbreakerTest, DumpGenericPasswordsWarnsIfKeyError) {
    DummyChainbreaker kc;
    kc.warned_msg = "";
    kc.dump_generic_passwords();
    ASSERT_EQ(kc.warned_msg, "[!] Generic Password Table is not available");
}

TEST(ChainbreakerTest, DumpInternetPasswordsWarnsIfKeyError) {
    DummyChainbreaker kc;
    kc.warned_msg = "";
    kc.dump_internet_passwords();
    ASSERT_EQ(kc.warned_msg, "[!] Internet Password Table is not available");
}