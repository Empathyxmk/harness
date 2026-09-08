#include <gtest/gtest.h>
#include <chrono>
#include <any>
#include <stdexcept>
#include <string>
#include <vector>
#include <optional>
#include "owncloud_stub.h"

// TestResponseError
class FakeResInt {
public:
    int status_code;
    std::vector<uint8_t> content;
    FakeResInt(int c, const std::vector<uint8_t>& v) : status_code(c), content(v) {}
    FakeResInt(int c) : status_code(c), content() {}
};

class FakeResStr {
public:
    int status_code;
    std::string content;
    FakeResStr(int c, const std::string& s) : status_code(c), content(s) {}
    FakeResStr(int c) : status_code(c), content("") {}
};

// TestResponseError
TEST(TestResponseError, test_init_with_int) {
    oc::ResponseError err(404, "MyErr");
    EXPECT_EQ(err.status_code, 404);
    EXPECT_EQ(err.str(), "MyErr error: 404");
}

TEST(TestResponseError, test_init_with_response) {
    FakeResInt res(400, {'r','e','s','b','o','d','y'});
    oc::ResponseError err(res, "OCS");
    EXPECT_EQ(err.status_code, 400);
    ASSERT_TRUE(std::holds_alternative<std::vector<uint8_t>>(err.get_resource_body()));
    auto body = std::get<std::vector<uint8_t>>(err.get_resource_body());
    EXPECT_EQ(body, std::vector<uint8_t>({'r','e','s','b','o','d','y'}));
    EXPECT_TRUE(err.str().find("HTTP error: 400 (OCS)") == std::string::npos);
}

TEST(TestResponseError, test_init_with_response_strcontent) {
    FakeResStr res(501, "Some string");
    oc::ResponseError err(res, "Txt");
    EXPECT_EQ(err.status_code, 501);
    ASSERT_TRUE(std::holds_alternative<std::string>(err.get_resource_body()));
    EXPECT_EQ(std::get<std::string>(err.get_resource_body()), "Some string");
    EXPECT_TRUE(err.str().find("Some string") != std::string::npos);
}

TEST(TestResponseError, test_repr_and_branching) {
    oc::ResponseError rr(401);
    EXPECT_EQ(rr.str(), "HTTP error: 401");
    class FakeResNoContent { public: int status_code = 500; };
    FakeResNoContent fres;
    oc::ResponseError err2(fres);
    EXPECT_TRUE(std::holds_alternative<std::nullptr_t>(err2.get_resource_body()));
    EXPECT_TRUE(err2.str().find("HTTP error: 500") != std::string::npos);
}

// TestOCSResponseError
TEST(TestOCSResponseError, test_ocs_xml_msg) {
    FakeResInt fres(500, {'<','r','o','o','t','>','<','m','e','s','s','a','g','e','>','f','a','i','l','m','s','g','<','/','m','e','s','s','a','g','e','>','<','/','r','o','o','t','>'});
    oc::OCSResponseError err(fres);
    EXPECT_TRUE(err.str().find("failmsg") != std::string::npos);
    ASSERT_TRUE(std::holds_alternative<std::vector<uint8_t>>(err.get_resource_body()));
    EXPECT_EQ(std::get<std::vector<uint8_t>>(err.get_resource_body()), fres.content);
}

TEST(TestOCSResponseError, test_ocs_xml_invalid) {
    FakeResInt fres(400, {'n','o','t','<','x','m','l'});
    oc::OCSResponseError err(fres);
    EXPECT_TRUE(err.str().find("OCS response error") != std::string::npos);
    ASSERT_TRUE(std::holds_alternative<std::vector<uint8_t>>(err.get_resource_body()));
    EXPECT_EQ(std::get<std::vector<uint8_t>>(err.get_resource_body()), fres.content);
}

TEST(TestOCSResponseError, test_ocs_none) {
    struct Fake { std::optional<int> status_code; std::optional<std::vector<uint8_t>> content; };
    Fake fres{std::nullopt, std::nullopt};
    oc::OCSResponseError err(fres);
    EXPECT_TRUE(std::holds_alternative<std::nullptr_t>(err.get_resource_body()));
}

// TestShareInfo and helpers 
TEST(TestShareInfo, test_getters) {
    std::map<std::string, std::any> info{
        {"id", std::string("123")},
        {"share_type", std::string("1")},
        {"permissions", std::string("3")},
        {"share_with", std::string("user1")},
        {"share_with_displayname", std::string("User One")},
        {"stime", std::string("1777777700")},
        {"expiration", std::string("2024-12-31")},
        {"path", std::string("/some.txt")}
    };
    oc::ShareInfo share(info);
    EXPECT_EQ(share.get_id(), 123);
    EXPECT_EQ(share.get_share_type(), 1);
    EXPECT_EQ(share.get_share_with(), "user1");
    EXPECT_EQ(share.get_share_with_displayname(), "User One");
    EXPECT_EQ(share.get_path(), "/some.txt");
    EXPECT_EQ(share.get_expiration(), "2024-12-31");
    EXPECT_TRUE(std::chrono::system_clock::time_point::clock::is_steady); // Not precise, but type-safety
}

TEST(TestShareInfo, test_int_conversion) {
    std::map<std::string, std::any> info{
        {"id", 123},
        {"permissions", std::string("")},
        {"share_type", nullptr},
        {"stime", std::string("1777777700")},
        {"expiration", nullptr}
    };
    oc::ShareInfo share(info);
    EXPECT_EQ(share._get_int("id").value(), 123);
    EXPECT_FALSE(share._get_int("permissions").has_value());
    EXPECT_FALSE(share._get_int("share_type").has_value());
    EXPECT_TRUE(std::chrono::system_clock::time_point::clock::is_steady);
}

TEST(TestShareInfo, test_missing_attrs) {
    oc::ShareInfo share({});
    EXPECT_EQ(share.get_share_with(), "");
    EXPECT_EQ(share.get_share_with_displayname(), "");
    EXPECT_EQ(share.get_path(), "");
}

TEST(TestShareInfo, test_del_attrs_removed) {
    std::map<std::string, std::any> input_info {
        {"id", std::string("1")},
        {"storage", std::string("xxx")},
        {"mail_send", 1},
        {"item_type", std::string("foo")},
        {"item_source", 42},
        {"file_source", 15},
        {"parent", nullptr},
        {"other", std::string("ok")},
        {"stime", std::string("1000")},
    };
    oc::ShareInfo share(input_info);
    share.del_attrs();
    EXPECT_TRUE(share.share_info.count("item_type") == 0);
    EXPECT_TRUE(share.share_info.count("parent") == 0);
    EXPECT_TRUE(share.share_info.count("id") == 1);
}

TEST(TestShareInfo, test_contains_and_getitem) {
    oc::ShareInfo share({
        {"id", 99},
        {"foo", std::string("bar")}
    });
    EXPECT_TRUE(share.contains("id"));
    EXPECT_EQ(std::any_cast<std::string>(share["foo"]), "bar");
}

TEST(TestUtils, test_escape_unescape) {
    std::string p = "/a b/abc.txt";
    std::string out = oc::escape_path(p);
    EXPECT_NE(out.find("%20"), std::string::npos);
    EXPECT_EQ(oc::unescape_path(out), p);
}

TEST(TestUtils, test_to_unicode_bytes) {
    std::vector<uint8_t> b{'a','b','c'};
    EXPECT_EQ(oc::to_unicode(b), "abc");
    EXPECT_EQ(oc::to_unicode("xyz"), "xyz");
}

TEST(TestUtils, test_to_bytes) {
    EXPECT_EQ(oc::to_bytes("xyz"), std::vector<uint8_t>({'x','y','z'}));
    const std::vector<uint8_t> v{'x','y','z'};
    EXPECT_EQ(oc::to_bytes(v), v);
}

TEST(TestUtils, test_strip_trailing_slash) {
    EXPECT_EQ(oc::strip_trailing_slash("foo/"), "foo");
    EXPECT_EQ(oc::strip_trailing_slash("/bar/"), "/bar");
    EXPECT_EQ(oc::strip_trailing_slash("/"), "/");
    EXPECT_FALSE(oc::strip_trailing_slash(std::optional<std::string>()).has_value());
}