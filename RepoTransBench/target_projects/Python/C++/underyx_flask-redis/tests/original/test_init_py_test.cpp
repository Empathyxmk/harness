#include <gtest/gtest.h>
#include <string>
#include <vector>

// Simulate the constants of __init__.py
namespace flask_redis_metadata {
    const std::string __version__ = "1.2.3";
    const std::string __title__ = "flask-redis";
    const std::string __description__ = "A Flask extension for Redis.";
    const std::string __url__ = "https://github.com/underyx/flask-redis";
    const std::string __uri__ = __url__;
    const std::string __author__ = "underyx";
    const std::string __email__ = "underyx@example.com";
    const std::string __license__ = "MIT";
    const std::string __copyright__ = "Copyright 2020 underyx";
    const std::vector<std::string> __all__ = {"FlaskRedis"};
    class FlaskRedis {};
}

TEST(TestInitPy, test_metadata_constants) {
    using namespace flask_redis_metadata;
    EXPECT_FALSE(__version__.empty());
    EXPECT_EQ(__title__, "flask-redis");
    EXPECT_FALSE(__description__.empty());
    EXPECT_EQ(__url__.substr(0,8), "https://");
    EXPECT_EQ(__uri__, __url__);
    EXPECT_FALSE(__author__.empty());
    EXPECT_NE(__email__.find('@'), std::string::npos);
    EXPECT_FALSE(__license__.empty());
    EXPECT_NE(__copyright__.find("Copyright"), std::string::npos);
}

TEST(TestInitPy, test_all_list) {
    using namespace flask_redis_metadata;
    bool found = false;
    for(const auto &item : __all__) {
        if (item == "FlaskRedis")
            found = true;
    }
    EXPECT_TRUE(found);
}