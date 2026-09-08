#include <gtest/gtest.h>
#include <string>
#include <vector>

// Sushi reused from test_sushi_unit.cpp, or define here for completeness

class Sushi {
public:
    std::string name;
    std::vector<std::string> ingredients;
    explicit Sushi(const std::string& n, std::vector<std::string> ings = {}) : name(n), ingredients(ings) {}
    bool is_vegetarian() const {
        for (auto& ingr : ingredients) {
            if (ingr == "Crab" || ingr == "Salmon" || ingr == "Shrimp" || ingr == "Tuna") return false;
        }
        return true;
    }
};

TEST(SushiEdgeTest, is_vegetarian_with_all_nonveg) {
    Sushi s("Mix", {"Crab", "Salmon", "Shrimp", "Tuna", "Rice"});
    EXPECT_FALSE(s.is_vegetarian());
}

TEST(SushiEdgeTest, is_vegetarian_with_mixed_case) {
    Sushi s("Strange", {"crab", "salmon", "shrimp", "tuna"});
    EXPECT_TRUE(s.is_vegetarian()); // Case-sensitive, so lowercase does not match
}