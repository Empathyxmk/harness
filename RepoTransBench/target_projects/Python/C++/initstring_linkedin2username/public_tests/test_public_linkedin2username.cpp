#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include "linkedin2username.h"

TEST(PublicLinkedin2Username, FLast) {
    auto out = f_last("Nina", "Simone");
    EXPECT_EQ(out, "nsimone");
}

TEST(PublicLinkedin2Username, FDotLast) {
    auto out = f_dot_last("Albert", "King");
    EXPECT_EQ(out, "a.king");
}

TEST(PublicLinkedin2Username, LastF) {
    auto out = last_f("Armstrong", "Louis");
    EXPECT_EQ(out, "armstrongl");
}

TEST(PublicLinkedin2Username, FirstDotLast) {
    auto out = first_dot_last("Bessie", "Smith");
    EXPECT_EQ(out, "bessie.smith");
}

TEST(PublicLinkedin2Username, FirstL) {
    auto out = first_l("Duke", "Ellington");
    EXPECT_EQ(out, "dukee");
}

TEST(PublicLinkedin2Username, FirstOnly) {
    auto out = first_only("Ella", "Fitzgerald");
    EXPECT_EQ(out, "ella");
}

TEST(PublicLinkedin2Username, CleanName) {
    EXPECT_EQ(clean_name(" Ray   Charles Jr."), "ray charles jr");
    EXPECT_EQ(clean_name("Dinah (CEO) Washington"), "dinah washington");
    EXPECT_EQ(clean_name("Count Basie."), "count basie");
}

TEST(PublicLinkedin2Username, SplitName) {
    auto out1 = split_name("Ruth Brown");
    EXPECT_EQ(out1, std::make_tuple("ruth", "brown", ""));
    auto out2 = split_name("Roy Orbison (VP)");
    EXPECT_EQ(out2, std::make_tuple("roy", "orbison", ""));
    auto out3 = split_name("Mr. Charles");
    EXPECT_EQ(out3, std::make_tuple("charles", "", ""));
}

TEST(PublicLinkedin2Username, FindEmployees) {
    std::vector<std::map<std::string, std::string>> employees = {
        {{"name", "Oscar Peterson"}},
        {{"name", "Sarah Vaughan"}},
        {{"name", "Mahalia Jackson"}}
    };

    // Assume find_employees echoes list if data is correct
    std::vector<std::map<std::string, std::string>> found = find_employees("dummy", employees);
    EXPECT_EQ(found, employees);
}