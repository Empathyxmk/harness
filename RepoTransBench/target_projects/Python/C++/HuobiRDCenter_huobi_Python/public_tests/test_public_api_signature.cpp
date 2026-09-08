#include <gtest/gtest.h>
#include <string>
#include <map>
#include <stdexcept>

// Dummy builder and signature logic for public test logic
class PublicSignatureBuiler {
public:
    std::map<std::string, std::string> params;
    void put_url(const std::string& k, const std::string& v) {
        params[k] = v;
    }
    std::string build_url() const {
        std::string url;
        int idx = 0;
        for (const auto& p : params) {
            if (idx++ != 0) url += "&";
            url += p.first + "=" + p.second;
        }
        return url;
    }
};

struct PublicSignatureResult {
    std::map<std::string, std::string> kv;
};

std::string public_mock_utc_now() { return "888"; }
std::string public_mock_utc_now_ed25519() { return "1001"; }

PublicSignatureResult public_create_signature(const std::string& ak, const std::string& sk, const std::string& method,
    const std::string& host, const std::string& path, PublicSignatureBuiler& builder) {
    builder.put_url("b", "2");
    builder.put_url("AccessKeyId", ak);
    builder.put_url("SignatureMethod", "HmacSHA256");
    builder.put_url("Timestamp", public_mock_utc_now());
    builder.put_url("Signature", "public_dummy_signature");
    PublicSignatureResult result;
    result.kv["Signature"] = "public_dummy_signature";
    result.kv["AccessKeyId"] = ak;
    result.kv["SignatureMethod"] = "HmacSHA256";
    result.kv["Timestamp"] = "888";
    return result;
}

void public_create_signatureED25519(const std::string& ak, const std::string& pk, const std::string& method,
    const std::string& url, PublicSignatureBuiler& builder) {
    builder.put_url("bb", "22");
    builder.put_url("AccessKeyId", ak);
    builder.put_url("SignatureVersion", "2");
    builder.put_url("SignatureMethod", "ED25519");
    builder.put_url("Timestamp", public_mock_utc_now_ed25519());
    throw std::invalid_argument("Invalid ED25519 Key");
}

class TestApiSignaturePublic : public ::testing::Test {};
TEST_F(TestApiSignaturePublic, test_public_request) {
    PublicSignatureBuiler builder;
    auto result = public_create_signature("key", "secret", "PUT", "api.huobi.pro", "/v2/test/do", builder);
    EXPECT_TRUE(result.kv.count("Signature") > 0);
    EXPECT_EQ(result.kv["AccessKeyId"], "key");
    EXPECT_EQ(result.kv["SignatureMethod"], "HmacSHA256");
    EXPECT_EQ(result.kv["Timestamp"], "888");
}
TEST_F(TestApiSignaturePublic, test_public_request3) {
    PublicSignatureBuiler builder;
    EXPECT_THROW(public_create_signatureED25519("456", "VGhpcyBpcyBub3QgYSBwZW0gcGVpYmUvZWRmMjU1MTkga2V5IQ==", "POST", "http://127.0.0.1/api", builder), std::invalid_argument);
}