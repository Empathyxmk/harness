#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
struct RouterOsApi {
    RouterOsApi(void*, const std::string&, const std::string&) {}
};
TEST(TestLoginRouterOsApiPublic, test_no_login_field) {
    EXPECT_THROW({ RouterOsApi(nullptr, "", ""); }, std::exception);
}
TEST(TestLoginRouterOsApiPublic, test_str_repr) {
    RouterOsApi api(reinterpret_cast<void*>(1), "myuser", "mypass");
    std::string repr = "RouterOsApi(user='myuser')";
    EXPECT_NE(repr.find("myuser"), std::string::npos);
}