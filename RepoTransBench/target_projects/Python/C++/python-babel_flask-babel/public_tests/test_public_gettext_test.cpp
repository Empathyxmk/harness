#include <gtest/gtest.h>
#include <string>
#include "babel_flask_babel/Babel.h"

TEST(TestPublicGettext, BasicTranslation) {
    BabelApp app;
    Babel b(&app, "ja");
    BabelRequestContext ctx(app);
    std::string rv = b.gettext("Hi %(name)s!", {{"name", "Taro"}});
    EXPECT_TRUE(!rv.empty());
    EXPECT_NE(rv.find("Taro"), std::string::npos);
}

TEST(TestPublicGettext, NGettext) {
    BabelApp app;
    Babel b(&app, "de_DE");
    BabelRequestContext ctx(app);
    std::string rv_sing = b.ngettext("There is %(num)d mouse", "There are %(num)d mice", 1);
    EXPECT_NE(rv_sing.find("mouse"), std::string::npos);
    std::string rv_plur = b.ngettext("There is %(num)d mouse", "There are %(num)d mice", 5);
    EXPECT_NE(rv_plur.find("mice"), std::string::npos);
}

TEST(TestPublicGettext, LazyGettext) {
    BabelApp app;
    Babel b(&app);
    BabelRequestContext ctx(app);
    auto lazy_hello = BabelLazyGettext("Welcome, %(guest)s!");
    std::string s = lazy_hello % std::map<std::string, std::string>{{"guest", "Kenta"}};
    EXPECT_NE(s.find("Kenta"), std::string::npos);
}

TEST(TestPublicGettext, GettextWithDomain) {
    BabelApp app;
    app.config["BABEL_DOMAIN"] = "myapp";
    Babel b(&app, "de_DE");
    BabelRequestContext ctx(app);
    std::string val = b.gettext("Good night");
    EXPECT_TRUE(!val.empty());
    EXPECT_NE(val.find("Good"), std::string::npos);
}