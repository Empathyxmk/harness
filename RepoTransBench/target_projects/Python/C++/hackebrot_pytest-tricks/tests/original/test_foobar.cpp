#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <memory>
#include <algorithm>

// Dummy implementation to support the tests, should match the original Python logic

class Package {
public:
    std::string name;
    std::string license;
    Package(const std::string& n, const std::string& l) : name(n), license(l) {}
    bool is_open_source = true;
};

class Person {
public:
    std::string name;
    bool looks_like_a_programmer = false;
    explicit Person(const std::string& n) : name(n) {}
    virtual void learn(const std::string& package) { looks_like_a_programmer = true; }
    virtual ~Person() = default;
};

class Woman : public Person {
public:
    using Person::Person;
};

class Man : public Person {
public:
    using Person::Person;
};

class FoobarTest : public ::testing::TestWithParam<Package> {};

std::vector<Package> PACKAGES = {
    Package("requests", "Apache 2.0"),
    Package("django", "BSD"),
    Package("pytest", "MIT"),
};

std::vector<std::shared_ptr<Person>> get_people() {
    return {
        std::make_shared<Woman>("Audrey"),
        std::make_shared<Woman>("Brianna"),
        std::make_shared<Man>("Daniel"),
        std::make_shared<Woman>("Ola"),
        std::make_shared<Man>("Kenneth"),
    };
}

INSTANTIATE_TEST_SUITE_P(Packages, FoobarTest, ::testing::ValuesIn(PACKAGES));

TEST_P(FoobarTest, is_open_source) {
    Package pkg = GetParam();
    EXPECT_TRUE(pkg.is_open_source);
}

TEST(FoobarLoose, become_a_programmer) {
    auto packages = PACKAGES;
    auto people = get_people();
    for (auto& person: people) {
        for (const auto& pkg: packages) {
            person->learn(pkg.name);
            EXPECT_TRUE(person->looks_like_a_programmer);
        }
    }
}