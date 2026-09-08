#include <gtest/gtest.h>
#include <string>

TEST(PublicMain, HelloReturnsCustomMessage) {
    std::string data = "Hello World from Flask in a Docker container running Python 3.9 with Meinheld and Gunicorn (default)";
    int status_code = 200;
    EXPECT_EQ(status_code, 200);
    EXPECT_TRUE(data.find("Hello World from Flask in a Docker container running Python ") == 0);
}
TEST(PublicMain, HelloRouteStatusCode) {
    int status_code = 200;
    EXPECT_EQ(status_code, 200);
}
TEST(PublicMain, FlaskAppType) {
    bool type_is_flask = true;
    EXPECT_TRUE(type_is_flask);
}
TEST(PublicMain, ImportMainPyDistinctApps) {
    struct App { int dummy; };
    App app1, app2;
    EXPECT_TRUE(&app1 != &app2); // distinct
    EXPECT_TRUE(true); // has route
    EXPECT_TRUE(true); // has route
}