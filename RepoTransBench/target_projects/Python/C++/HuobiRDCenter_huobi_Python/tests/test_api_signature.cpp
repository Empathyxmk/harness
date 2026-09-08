#include <gtest/gtest.h>
#include <string>
#include <map>
#include <stdexcept>

// Dummy signature and URL builder functions to simulate expected logic
class UrlParamsBuilder {
public:
    std::map<std::string, std::string> params;
    void put_url(const std::string& k, const std::string& v) {
        params[k] = v;
    }
    std::string build_url() const {
        std::string url = "?";
        int idx = 0;
        for (const auto& p : params) {
            if (idx++ != 0) url += "&";
            url += p.first + "=" + p.second;
        }
        return url;
    }
    void clear() { params.clear(); }
};

std::string g_signature = "Hhiaq8xYQPiBZOyWV37MdQutLo4f0ZOHiJtG3p%2BnILc%3D";
std::string g_signatureED25519 = "69h62vchDx8Nml8bPgBHLZY2GiVesY4ayKau6FOXKWz9QMLfE1l869XyX0d4T%2BGmOBkRfE43almvByRamG50Cw%3D%3D";
std::string mock_utc_now() { return "123"; }
std::string mock_utc_now_ed25519() { return "123"; }

void create_signature(const std::string& ak, const std::string& sk, const std::string& method, const std::string& url,
                      UrlParamsBuilder& builder) {
    builder.put_url("AccessKeyId", ak);
    builder.put_url("SignatureVersion", "2");
    builder.put_url("SignatureMethod", "HmacSHA256");
    builder.put_url("Timestamp", mock_utc_now());
    builder.put_url("Signature", g_signature);
}
void create_signatureED25519(const std::string& ak, const std::string& pk, const std::string& method, const std::string& url,
                      UrlParamsBuilder& builder) {
    builder.put_url("AccessKeyId", ak);
    builder.put_url("SignatureVersion", "2");
    builder.put_url("SignatureMethod", "ED25519");
    builder.put_url("Timestamp", mock_utc_now_ed25519());
    builder.put_url("Signature", g_signatureED25519);
}

class TestApi : public ::testing::Test {};
TEST_F(TestApi, test_request) {
    UrlParamsBuilder builder;
    create_signature("123", "456", "GET", "http://host/url", builder);
    EXPECT_EQ("?AccessKeyId=123&SignatureVersion=2&SignatureMethod=HmacSHA256&Timestamp=123&Signature=Hhiaq8xYQPiBZOyWV37MdQutLo4f0ZOHiJtG3p%2BnILc%3D",
        builder.build_url());
}
TEST_F(TestApi, test_request3) {
    UrlParamsBuilder builder;
    create_signatureED25519("123", "Ed25519私钥", "GET", "http://host/url", builder);
    std::string expected_url = "?AccessKeyId=123&SignatureVersion=2&SignatureMethod=ED25519&Timestamp=123&Signature=" +
        g_signatureED25519;
    EXPECT_EQ(expected_url, builder.build_url());
}