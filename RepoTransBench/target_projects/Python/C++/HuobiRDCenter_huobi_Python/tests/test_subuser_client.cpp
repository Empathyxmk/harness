#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <stdexcept>
#include <memory>

class DummySubuserClient {
public:
    std::string api_key, secret_key;
    DummySubuserClient(const std::string& api_key="", const std::string& secret_key="")
        : api_key(api_key), secret_key(secret_key) {}

    std::vector<std::map<std::string, std::string>> post_set_subuser_transferability(const std::string& sub_uids, bool transferability) {
        if (sub_uids.empty()) throw std::invalid_argument("sub_uids required");
        return {{ {"uid", sub_uids}, {"success", "1"}, {"transferability", transferability ? "1" : "0"} }};
    }
    std::vector<std::map<std::string, std::string>> post_set_subuser_transferability(const std::string& sub_uids, const std::string& transferability) {
        throw std::invalid_argument("transferability must be bool");
    }

    struct Result {
        std::string print_object() const { return "printed"; }
    };

    Result get_sub_user_deposit_history(int sub_uid) {
        if (sub_uid == 0) throw std::runtime_error("Not found");
        return Result{};
    }

    Result post_subuser_apikey_generate(const std::string& otp_token, int sub_uid, const std::string& note, const std::string& permission) {
        if (otp_token.empty() || note.empty()) throw std::invalid_argument("otp_token and note required");
        return Result{};
    }
};

class TestSubuserClientIntegration : public ::testing::Test {
protected:
    DummySubuserClient client;
    void SetUp() override {
        client = DummySubuserClient("test-key", "test-secret");
    }
};
TEST_F(TestSubuserClientIntegration, test_post_set_subuser_transferability_true) {
    auto res = client.post_set_subuser_transferability("1234", true);
    EXPECT_EQ(res[0].at("transferability"), "1");
    EXPECT_EQ(res[0].at("uid"), "1234");
}
TEST_F(TestSubuserClientIntegration, test_post_set_subuser_transferability_false) {
    auto res = client.post_set_subuser_transferability("999", false);
    EXPECT_EQ(res[0].at("transferability"), "0");
}
TEST_F(TestSubuserClientIntegration, test_post_set_subuser_transferability_invalid) {
    EXPECT_THROW(client.post_set_subuser_transferability("999", std::string("invalid")), std::invalid_argument);
}
TEST_F(TestSubuserClientIntegration, test_post_set_subuser_transferability_no_uid) {
    EXPECT_THROW(client.post_set_subuser_transferability("", true), std::invalid_argument);
}
TEST_F(TestSubuserClientIntegration, test_get_sub_user_deposit_history_ok) {
    auto res = client.get_sub_user_deposit_history(100);
    EXPECT_EQ(res.print_object(), "printed");
}
TEST_F(TestSubuserClientIntegration, test_get_sub_user_deposit_history_not_found) {
    EXPECT_THROW(client.get_sub_user_deposit_history(0), std::runtime_error);
}
TEST_F(TestSubuserClientIntegration, test_post_subuser_apikey_generate_success) {
    auto res = client.post_subuser_apikey_generate("otp", 123, "note", "readOnly");
    EXPECT_EQ(res.print_object(), "printed");
}
TEST_F(TestSubuserClientIntegration, test_post_subuser_apikey_generate_missing) {
    EXPECT_THROW(client.post_subuser_apikey_generate("", 123, "", "readOnly"), std::invalid_argument);
}
TEST_F(TestSubuserClientIntegration, test_init) {
    DummySubuserClient c;
    EXPECT_EQ(c.api_key, "");
    EXPECT_EQ(c.secret_key, "");
}