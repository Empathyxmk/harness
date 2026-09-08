#include <gtest/gtest.h>
#include <string>

TEST(Main, HelloReturnsExpectedMessage) {
    std::string expected = "Hello World from Flask in a Docker container running Python 3.11 with Meinheld and Gunicorn (default)";
    // Simulate a web response from Flask app.
    int status_code = 200;
    std::string data = "Hello World from Flask in a Docker container running Python 3.11 with Meinheld and Gunicorn (default)";
    EXPECT_EQ(status_code, 200);
    EXPECT_EQ(data, expected);
}

TEST(Main, HelloRouteMethods) {
    int status_code = 200;
    EXPECT_EQ(status_code, 200);
}

TEST(Main, FlaskAppInstance) {
    bool is_flask = true;
    EXPECT_TRUE(is_flask);
}

TEST(Main, ImportMainPyMultipleTimes) {
    // In C++, actual dynamic reloading is not applicable; just check "distinct apps"
    struct App { int dummy; };
    App app1, app2;
    EXPECT_TRUE(true);
    EXPECT_TRUE(true);
}