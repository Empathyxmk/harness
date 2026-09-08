#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <memory>

// Dummy implementation to match the public scenario
class Package {
public:
    std::string name;
    explicit Package(const std::string& n) : name(n) {}
};

class Person {
public:
    std::string name;
    bool looks_like_a_programmer = false;
    explicit Person(std::string n) : name(std::move(n)) {}
    virtual void learn(const std::string&) { looks_like_a_programmer = true; }
    virtual ~Person() = default;
};
class Woman : public Person { public: using Person::Person; };
class Man   : public Person { public: using Person::Person; };

std::vector<std::shared_ptr<Person>> get_people() {
    return {
        std::make_shared<Man>("Oliver"),
        std::make_shared<Woman>("Amelia"),
        std::make_shared<Man>("Mason"),
        std::make_shared<Man>("Logan"),
        std::make_shared<Woman>("Harper")
    };
}

TEST(PublicFoobar, BecomeAProgrammer) {
    std::vector<Package> pkgs = { Package("matplotlib"), Package("pandas") };
    auto people = get_people();
    for (const auto& pkg: pkgs)
        for (auto& person: people) {
            person->learn(pkg.name);
            EXPECT_TRUE(person->looks_like_a_programmer);
        }
}

TEST(PublicFoobar, LearnMultiplePackagesPublic) {
    std::vector<std::shared_ptr<Person>> people = {
        std::make_shared<Man>("Jack"),
        std::make_shared<Woman>("Lily")
    };
    for (auto& person : people) {
        person->learn("sqlalchemy");
        person->learn("httpx");
        EXPECT_TRUE(person->looks_like_a_programmer);
    }
}

TEST(PublicFoobar, NotProgrammerInitiallyPublic) {
    std::vector<std::shared_ptr<Person>> people = {
        std::make_shared<Man>("Henry"),
        std::make_shared<Woman>("Ella")
    };
    for (auto& person : people) {
        EXPECT_FALSE(person->looks_like_a_programmer);
    }
}