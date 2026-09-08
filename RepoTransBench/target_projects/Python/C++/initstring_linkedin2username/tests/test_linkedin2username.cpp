#include <gtest/gtest.h>
#include <string>
#include <set>
#include <map>
#include <vector>
#include <fstream>
#include <nlohmann/json.hpp> // For JSON parsing if required
#include "linkedin2username.h"

// TEST_NAMES as in Python test
static const std::map<int, std::string> TEST_NAMES = {
    {1, "John Smith"},
    {2, "John Davidson-Smith"},
    {3, "John-Paul Smith-Robinson"},
    {4, "José Gonzáles"},
    {5, "🙂 Emoji Folks 🙂"}
};

TEST(NameMutatorFull, FLast) {
    NameMutator mut1(TEST_NAMES.at(1));
    EXPECT_EQ(mut1.f_last(), std::set<std::string>{"jsmith"});

    NameMutator mut2(TEST_NAMES.at(2));
    EXPECT_EQ(mut2.f_last(), (std::set<std::string>{"jsmith", "jdavidson"}));

    NameMutator mut3(TEST_NAMES.at(3));
    EXPECT_EQ(mut3.f_last(), (std::set<std::string>{"jsmith", "jrobinson"}));

    NameMutator mut4(TEST_NAMES.at(4));
    EXPECT_EQ(mut4.f_last(), std::set<std::string>{"jgonzales"});

    NameMutator mut5(TEST_NAMES.at(5));
    EXPECT_EQ(mut5.f_last(), std::set<std::string>{"efolks"});
}

TEST(NameMutatorFull, FDotLast) {
    NameMutator mut1(TEST_NAMES.at(1));
    EXPECT_EQ(mut1.f_dot_last(), std::set<std::string>{"j.smith"});

    NameMutator mut2(TEST_NAMES.at(2));
    EXPECT_EQ(mut2.f_dot_last(), (std::set<std::string>{"j.smith", "j.davidson"}));

    NameMutator mut3(TEST_NAMES.at(3));
    EXPECT_EQ(mut3.f_dot_last(), (std::set<std::string>{"j.smith", "j.robinson"}));

    NameMutator mut4(TEST_NAMES.at(4));
    EXPECT_EQ(mut4.f_dot_last(), std::set<std::string>{"j.gonzales"});

    NameMutator mut5(TEST_NAMES.at(5));
    EXPECT_EQ(mut5.f_dot_last(), std::set<std::string>{"e.folks"});
}

TEST(NameMutatorFull, LastF) {
    NameMutator mut1(TEST_NAMES.at(1));
    EXPECT_EQ(mut1.last_f(), std::set<std::string>{"smithj"});

    NameMutator mut2(TEST_NAMES.at(2));
    EXPECT_EQ(mut2.last_f(), (std::set<std::string>{"smithj", "davidsonj"}));

    NameMutator mut3(TEST_NAMES.at(3));
    EXPECT_EQ(mut3.last_f(), (std::set<std::string>{"smithj", "robinsonj"}));

    NameMutator mut4(TEST_NAMES.at(4));
    EXPECT_EQ(mut4.last_f(), std::set<std::string>{"gonzalesj"});

    NameMutator mut5(TEST_NAMES.at(5));
    EXPECT_EQ(mut5.last_f(), std::set<std::string>{"folkse"});
}

TEST(NameMutatorFull, FirstDotLast) {
    NameMutator mut1(TEST_NAMES.at(1));
    EXPECT_EQ(mut1.first_dot_last(), std::set<std::string>{"john.smith"});

    NameMutator mut2(TEST_NAMES.at(2));
    EXPECT_EQ(mut2.first_dot_last(), (std::set<std::string>{"john.smith", "john.davidson"}));

    NameMutator mut3(TEST_NAMES.at(3));
    EXPECT_EQ(mut3.first_dot_last(), (std::set<std::string>{"john.smith", "john.robinson"}));

    NameMutator mut4(TEST_NAMES.at(4));
    EXPECT_EQ(mut4.first_dot_last(), std::set<std::string>{"jose.gonzales"});

    NameMutator mut5(TEST_NAMES.at(5));
    EXPECT_EQ(mut5.first_dot_last(), std::set<std::string>{"emoji.folks"});
}

TEST(NameMutatorFull, FirstL) {
    NameMutator mut1(TEST_NAMES.at(1));
    EXPECT_EQ(mut1.first_l(), std::set<std::string>{"johns"});

    NameMutator mut2(TEST_NAMES.at(2));
    EXPECT_EQ(mut2.first_l(), (std::set<std::string>{"johns", "johnd"}));

    NameMutator mut3(TEST_NAMES.at(3));
    EXPECT_EQ(mut3.first_l(), (std::set<std::string>{"johns", "johnr"}));

    NameMutator mut4(TEST_NAMES.at(4));
    EXPECT_EQ(mut4.first_l(), std::set<std::string>{"joseg"});

    NameMutator mut5(TEST_NAMES.at(5));
    EXPECT_EQ(mut5.first_l(), std::set<std::string>{"emojif"});
}

TEST(NameMutatorFull, First) {
    NameMutator mut1(TEST_NAMES.at(1));
    EXPECT_EQ(mut1.first(), std::set<std::string>{"john"});

    NameMutator mut2(TEST_NAMES.at(2));
    EXPECT_EQ(mut2.first(), std::set<std::string>{"john"});

    NameMutator mut3(TEST_NAMES.at(3));
    EXPECT_EQ(mut3.first(), std::set<std::string>{"john"});

    NameMutator mut4(TEST_NAMES.at(4));
    EXPECT_EQ(mut4.first(), std::set<std::string>{"jose"});

    NameMutator mut5(TEST_NAMES.at(5));
    EXPECT_EQ(mut5.first(), std::set<std::string>{"emoji"});
}

TEST(NameMutatorFull, CleanName) {
    NameMutator mut("xxx");
    EXPECT_EQ(mut.clean_name("  🙂Ànèôõö    ßï🙂  "), "aneooo ssi");

    std::string name = "Dr. Hannibal Lecter, PhD.";
    EXPECT_EQ(mut.clean_name(name), "hannibal lecter");

    name = "Mr. Fancy Pants MD, PhD, MBA";
    EXPECT_EQ(mut.clean_name(name), "fancy pants");

    name = "Mr. Cert Dude (OSCP, OSCE)";
    EXPECT_EQ(mut.clean_name(name), "cert dude");
}

TEST(NameMutatorFull, SplitName) {
    NameMutator mut("xxx");

    std::string name = "madonna wayne gacey";
    auto res = mut.split_name(name);
    EXPECT_EQ(res.at("first"), "madonna");
    EXPECT_EQ(res.at("second"), "wayne");
    EXPECT_EQ(res.at("last"), "gacey");

    name = "twiggy ramirez";
    res = mut.split_name(name);
    EXPECT_EQ(res.at("first"), "twiggy");
    EXPECT_EQ(res.at("second"), "");
    EXPECT_EQ(res.at("last"), "ramirez");

    name = "brian warner is marilyn manson";
    res = mut.split_name(name);
    EXPECT_EQ(res.at("first"), "brian");
    EXPECT_EQ(res.at("second"), "marilyn");
    EXPECT_EQ(res.at("last"), "manson");
}

TEST(Linkedin2UsernameFull, FindEmployees) {
    // Read data from test/mocks
    std::ifstream infile("tests/mock-employee-response");
    ASSERT_TRUE(infile.is_open());
    std::string result((std::istreambuf_iterator<char>(infile)), std::istreambuf_iterator<char>());
    infile.close();

    std::vector<std::map<std::string, std::string>> employees = find_employees(result);

    ASSERT_EQ(employees.size(), 2);
    EXPECT_EQ(employees[0].at("full_name"), "Michael Myers");
    EXPECT_EQ(employees[0].at("occupation"), "Camp Counsellor");
    EXPECT_EQ(employees[1].at("full_name"), "Freddy Krueger");
    EXPECT_EQ(employees[1].at("occupation"), "Babysitter");

    std::ifstream infile2("tests/mock-employee-response-last-page");
    ASSERT_TRUE(infile2.is_open());
    std::string result2((std::istreambuf_iterator<char>(infile2)), std::istreambuf_iterator<char>());
    infile2.close();

    EXPECT_TRUE(find_employees(result2).empty());
}