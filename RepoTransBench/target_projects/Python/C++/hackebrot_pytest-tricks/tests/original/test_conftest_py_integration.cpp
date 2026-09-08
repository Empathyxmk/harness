#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <memory>
#include <algorithm>

class Restaurant {
public:
    std::string name;
    std::string location;
    std::vector<std::string> menu;
    Restaurant(const std::string& n, const std::string& loc, std::vector<std::string> menu_arg) : name(n), location(loc), menu(menu_arg) {}
};

class Sushi {
public:
    std::string name;
    std::vector<std::string> ingredients;
    Sushi(const std::string& n, std::vector<std::string> ings) : name(n), ingredients(ings) {}
};

Restaurant fooshi_bar() {
    return Restaurant("Fooshi Bar", "Buenos Aires", {"Ebi Nigiri", "Edamame", "Inarizushi", "Kappa Maki", "Miso Soup", "Sake Nigiri", "Tamagoyaki"});
}

std::map<std::string, std::vector<std::string>> recipes() {
    return {
        {"California Roll", {"Rice", "Cucumber", "Avocado", "Crab"}},
        {"Ebi Nigiri", {"Shrimp", "Rice"}},
        {"Inarizushi", {"Fried tofu", "Rice"}},
        {"Kappa Maki", {"Cucumber", "Rice", "Nori"}},
        {"Maguro Nigiri", {"Tuna", "Rice", "Nori"}},
        {"Sake Nigiri", {"Salmon", "Rice", "Nori"}},
        {"Tamagoyaki", {"Fried egg", "Rice", "Nori"}},
        {"Tsunamayo Maki", {"Tuna", "Mayonnaise"}}
    };
}

TEST(ConftestIntegration, fooshi_bar_fixture) {
    Restaurant rest = fooshi_bar();
    EXPECT_EQ(rest.name, "Fooshi Bar");
    EXPECT_NE(std::find(rest.menu.begin(), rest.menu.end(), "Ebi Nigiri"), rest.menu.end());
    EXPECT_EQ(rest.location, "Buenos Aires");
    EXPECT_NE(std::find(rest.menu.begin(), rest.menu.end(), "Tamagoyaki"), rest.menu.end());
}

TEST(ConftestIntegration, recipes_fixture) {
    auto recs = recipes();
    EXPECT_EQ(recs.count("Ebi Nigiri"), 1u);
    EXPECT_EQ(recs["California Roll"], (std::vector<std::string>{"Rice", "Cucumber", "Avocado", "Crab"}));
}

class SushiParamsTest : public ::testing::TestWithParam<std::string> {};
INSTANTIATE_TEST_SUITE_P(SushiIndirectParam,
        SushiParamsTest, ::testing::Values("California Roll", "Ebi Nigiri", "Tamagoyaki"));

TEST_P(SushiParamsTest, sushi_fixture_param) {
    auto recs = recipes();
    auto name = GetParam();
    Sushi s(name, recs[name]);
    EXPECT_TRUE(!s.ingredients.empty());
    EXPECT_TRUE(std::find(
        std::vector<std::string>{"California Roll", "Ebi Nigiri", "Tamagoyaki"}.begin(),
        std::vector<std::string>{"California Roll", "Ebi Nigiri", "Tamagoyaki"}.end(),
        s.name) != std::vector<std::string>{"California Roll", "Ebi Nigiri", "Tamagoyaki"}.end()
    );
}