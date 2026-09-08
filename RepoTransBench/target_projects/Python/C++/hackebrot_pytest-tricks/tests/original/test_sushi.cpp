#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <algorithm>

// Dummy restaurant, menu, sushi, etc. for simulating test context similar to original Python fixtures.

struct Sushi {
    std::string name;
    std::vector<std::string> ingredients;
    Sushi(const std::string& n, std::vector<std::string> ings): name(n), ingredients(ings) {}
    bool is_vegetarian() const {
        for (const auto& ingr : ingredients)
            if (ingr == "Crab" || ingr == "Salmon" || ingr == "Shrimp" || ingr == "Tuna") return false;
        return true;
    }
};

struct Restaurant {
    std::string name;
    std::vector<std::string> menu;
    Restaurant() : name("Fooshi Bar"),
        menu({"Kappa Maki", "Tamagoyaki", "Inarizushi", "Edamame", "Miso Soup"})
    {}
};

static Sushi sushi_from_name(const std::string& n) {
    if (n == "Kappa Maki")
        return Sushi(n, {"Cucumber", "Rice", "Nori"});
    if (n == "Tamagoyaki")
        return Sushi(n, {"Fried egg", "Rice", "Nori"});
    if (n == "Inarizushi")
        return Sushi(n, {"Fried tofu", "Rice"});
    return Sushi(n, {"Rice"});
}

class SushiServeTest : public ::testing::TestWithParam<std::pair<std::string, std::string>> {};

INSTANTIATE_TEST_SUITE_P(
    VegetarianSushiCases,
    SushiServeTest,
    ::testing::Combine(
        ::testing::Values("Kappa Maki", "Tamagoyaki", "Inarizushi"),
        ::testing::Values("Edamame", "Miso Soup")
    ),
    [](const testing::TestParamInfo<SushiServeTest::ParamType>& info) {
        return info.param.first + "_" + info.param.second;
    }
);

TEST_P(SushiServeTest, FooshiServesVegetarianSushi) {
    Restaurant fooshi_bar;
    std::string sushi_name = GetParam().first;
    std::string side_dish = GetParam().second;
    Sushi sushi = sushi_from_name(sushi_name);
    EXPECT_TRUE(sushi.is_vegetarian());
    EXPECT_NE(std::find(fooshi_bar.menu.begin(), fooshi_bar.menu.end(), sushi.name), fooshi_bar.menu.end());
    EXPECT_NE(std::find(fooshi_bar.menu.begin(), fooshi_bar.menu.end(), side_dish), fooshi_bar.menu.end());
}

TEST(SushiBasic, SushiMembers) {
    Sushi sushi("any", {"X"});
    EXPECT_FALSE(sushi.name.empty());
    EXPECT_FALSE(sushi.ingredients.empty());
}