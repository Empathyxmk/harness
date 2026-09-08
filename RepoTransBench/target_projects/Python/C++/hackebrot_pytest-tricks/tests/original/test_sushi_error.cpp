#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <vector>

class Restaurant {
public:
    Restaurant(const std::string& n, const std::string& location, std::vector<std::string> menu = {}) {
        if (menu.empty()) throw std::invalid_argument("Menu must be provided");
    }
};

class Sushi {
public:
    Sushi(const std::string& n, std::vector<std::string> ingredients = {}) {
        if (ingredients.empty()) throw std::invalid_argument("Ingredients must be provided");
    }
};

TEST(RestaurantTest, empty_menu_list_raises) {
    EXPECT_THROW(Restaurant("Foo", "Bar", {}), std::invalid_argument);
}

TEST(SushiTest, empty_ingredients_list_raises) {
    EXPECT_THROW(Sushi("Foo", {}), std::invalid_argument);
}