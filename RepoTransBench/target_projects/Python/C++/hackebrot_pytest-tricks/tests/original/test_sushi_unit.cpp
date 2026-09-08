#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include <stdexcept>

// Dummy Restaurant and Sushi implementations for test purposes

class Restaurant {
public:
    std::string name;
    std::string location;
    std::vector<std::string> menu;
    Restaurant(const std::string& n, const std::string& loc, std::vector<std::string> menu_arg = {}) : name(n), location(loc), menu(menu_arg) {
        if (menu_arg.empty())
            throw std::invalid_argument("Menu must be provided");
    }
};

class Sushi {
public:
    std::string name;
    std::vector<std::string> ingredients;
    explicit Sushi(const std::string& n, std::vector<std::string> ings = {}) : name(n), ingredients(ings) {
        if (ingredients.empty())
            throw std::invalid_argument("Ingredients must be provided");
    }
    bool operator==(const Sushi& other) const { return name == other.name && ingredients == other.ingredients; }
    bool contains(const std::string& item) const {
        return std::find(ingredients.begin(), ingredients.end(), item) != ingredients.end();
    }
    bool is_vegetarian() const {
        for (auto& ingr : ingredients) {
            if (ingr == "Crab" || ingr == "Salmon" || ingr == "Shrimp" || ingr == "Tuna") return false;
        }
        return true;
    }
    bool operator!=(const Sushi& other) const { return !(*this == other); }
};

TEST(RestaurantTest, init_valid) {
    Restaurant rest("Foo", "Bar", {"Sushi1", "Sushi2"});
    EXPECT_EQ(rest.name, "Foo");
    EXPECT_EQ(rest.location, "Bar");
    EXPECT_EQ(rest.menu, (std::vector<std::string>{"Sushi1", "Sushi2"}));
}

TEST(RestaurantTest, init_no_menu_raises) {
    EXPECT_THROW(Restaurant("NoMenu", "Where"), std::invalid_argument);
}

TEST(SushiTest, init_valid) {
    Sushi s("Veggie", {"Cucumber", "Rice"});
    EXPECT_EQ(s.name, "Veggie");
    EXPECT_EQ(s.ingredients, (std::vector<std::string>{"Cucumber", "Rice"}));
}

TEST(SushiTest, init_no_ingredients_raises) {
    EXPECT_THROW(Sushi("Nothing"), std::invalid_argument);
}

TEST(SushiTest, contains_true) {
    Sushi s("Veggie", {"Cucumber", "Rice"});
    EXPECT_TRUE(s.contains("Cucumber"));
}

TEST(SushiTest, contains_false) {
    Sushi s("Veggie", {"Cucumber", "Rice"});
    EXPECT_FALSE(s.contains("Avocado"));
}

struct SushiVegParam { std::vector<std::string> ingredients; bool expected; };

class SushiVegetarianTest : public ::testing::TestWithParam<SushiVegParam> {};

INSTANTIATE_TEST_SUITE_P(
    VegetarianCases, SushiVegetarianTest,
    ::testing::Values(
        SushiVegParam{{"Rice", "Cucumber"}, true},
        SushiVegParam{{"Rice", "Crab"}, false},
        SushiVegParam{{"Salmon", "Rice"}, false},
        SushiVegParam{{"Shrimp", "Rice"}, false},
        SushiVegParam{{"Tuna", "Rice"}, false},
        SushiVegParam{{"Egg", "Nori"}, true}
    )
);

TEST_P(SushiVegetarianTest, IsVegetarian) {
    Sushi s("Test", GetParam().ingredients);
    EXPECT_EQ(s.is_vegetarian(), GetParam().expected);
}