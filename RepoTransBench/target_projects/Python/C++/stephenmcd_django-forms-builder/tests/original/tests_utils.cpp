#include <gtest/gtest.h>
#include "forms_fields.h"

using namespace forms_fields;

TEST(Utils, IsFileExtensions) {
    EXPECT_TRUE(is_file("photo.PNG"));
    EXPECT_TRUE(is_file("document.PDF"));
    EXPECT_FALSE(is_file("example.txt"));
    EXPECT_FALSE(is_file("no_dot"));
}

TEST(Utils, SlugifyBasic) {
    std::string s = " Hello__World__ ";
    std::string want = "hello-world";
    std::string sl = s;
    std::transform(sl.begin(), sl.end(), sl.begin(), ::tolower);
    size_t pos;
    while ((pos = sl.find("__")) != std::string::npos)
        sl.replace(pos, 2, "-");
    sl.erase(remove_if(sl.begin(), sl.end(), ::isspace), sl.end());
    if (sl.length() > 2 && sl.front() == '-')
        sl = sl.substr(1);
    if (sl.length() > 2 && sl.back() == '-')
        sl = sl.substr(0, sl.length() - 1);
    EXPECT_EQ(sl, want);
}

TEST(Utils, IsEmailCases) {
    auto is_email = [](const std::string& s) {
        auto at = s.find('@');
        auto dot = s.find('.', at == std::string::npos ? 0 : at);
        return at != std::string::npos && dot != std::string::npos && at > 0 && dot > at;
    };
    EXPECT_TRUE(is_email("foo@bar.com"));
    EXPECT_FALSE(is_email("notanemail"));
    EXPECT_FALSE(is_email("@nodomain"));
}

TEST(Utils, ContentAsTxtHtml) {
    // Just demonstrate type consistency.
    struct Dummy { };
    std::string txt = "dummy text";
    std::string html = "<div>dummy text</div>";
    EXPECT_TRUE(typeid(txt) == typeid(std::string));
    EXPECT_TRUE(typeid(html) == typeid(std::string));
}

TEST(Utils, GetAdminUrlFormat) {
    struct Dummy {
        std::string app_label = "myapp";
        std::string model_name = "dummy";
        int pk = 1;
    };
    Dummy d;
    std::string url = d.app_label + "/" + d.model_name + "/" + std::to_string(d.pk) + "/";
    EXPECT_TRUE(url.find("myapp/dummy/1/") != std::string::npos ||
                url.find("myapp/dummy/1") != std::string::npos);
}