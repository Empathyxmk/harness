#include <gtest/gtest.h>
#include <string>
#include <map>

// Dummy brk_module public API for translation
struct BrkResult {
    std::string status;
    std::string method;
    std::string url;
    std::string id;
};

BrkResult add_break_point(const std::string& url, const std::string& method) {
    return {"OK", method, url, ""};
}
BrkResult remove_break_point(const std::string& id) {
    return {"REMOVED", "", "", id};
}

TEST(PublicBrkTest, AddBreakPointDiffData) {
    std::string url = "http://public.example.com/login";
    std::string method = "POST";
    BrkResult response = add_break_point(url, method);
    ASSERT_EQ(response.status, "OK");
    ASSERT_EQ(response.method, method);
    ASSERT_EQ(response.url.substr(0, 18), "http://public.");
}

TEST(PublicBrkTest, RemoveBreakPointDiffData) {
    std::string brk_id = "customBrk2";
    BrkResult response = remove_break_point(brk_id);
    ASSERT_EQ(response.status, "REMOVED");
    ASSERT_EQ(response.id, brk_id);
}