#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <regex>

namespace flask_redis_metadata_public {
    const std::string __version__ = "2.0.1";
    const std::string __title__ = "Flask-Redis";
    const std::string __description__ = "Yet another redis extension for Flask web apps.";
    const std::string __url__ = "https://flask-redis.public";
    const std::string __uri__ = __url__;
    const std::string __author__ = "Somebody";
    const std::string __email__ = "somebody@flaskredis.com";
    const std::string __license__ = "BSD";
    const std::string __copyright__ = "Copyright 2024 FlaskRedis OSS";
    const std::vector<std::string> __all__ = {"FlaskRedis"};
}

TEST(TestPublicInitPy, test_public_dunder_constants_distinct) {
    using namespace flask_redis_metadata_public;
    EXPECT_TRUE(!__version__.empty());
    EXPECT_EQ(__title__, "Flask-Redis");
    EXPECT_NE(__description__.find("redis"), std::string::npos);
    EXPECT_TRUE(__url__.rfind("https://", 0) == 0);
    EXPECT_TRUE(__uri__.rfind("https://", 0) == 0);
    EXPECT_NE(__email__.find("@"), std::string::npos);
    EXPECT_NE(__copyright__.find("opyright"), std::string::npos);
    EXPECT_TRUE(typeid(__all__).name() != nullptr);
    bool found = false;
    for(const auto &item : __all__) {
        if(item == "FlaskRedis") found = true;
    }
    EXPECT_TRUE(found);
}

TEST(TestPublicInitPy, test_public_title_unique) {
    using namespace flask_redis_metadata_public;
    EXPECT_EQ(__title__, "Flask-Redis");
    EXPECT_TRUE(__author__.size() > 3);
}

TEST(TestPublicInitPy, test_public_version_style) {
    using namespace flask_redis_metadata_public;
    std::regex rx(R"(^\d+\.\d+\.\d+)");
    EXPECT_TRUE(std::regex_search(__version__, rx));
}