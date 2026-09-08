#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <algorithm>

// Stubs
namespace fields {
    class String {
    public:
        std::string value;
        String() : value("") {}
        String(const std::string& v) : value(v) {}
        operator std::string() const { return value; }
    };
    class Integer {
    public:
        int value;
        Integer() : value(0) {}
        Integer(int v) : value(v) {}
        operator int() const { return value; }
    };
}

class MyPublicModel {
public:
    MyPublicModel(std::string name_= "", int age_ = 0) : name(name_), age(age_) {}
    std::string name;
    int age;
};

namespace registry {
    class Registry {
    public:
        void register_model(const MyPublicModel&) {}
    };
}

namespace repositories {
    class InMemoryRepository {
    public:
        std::vector<MyPublicModel> storage;
        InMemoryRepository() = default;
        void save(const MyPublicModel& m) { storage.push_back(m); }
        const MyPublicModel& get(size_t id) const { return storage.at(id); }
        std::vector<MyPublicModel>::const_iterator all() const { return storage.cbegin(); }
    };
}

TEST(PublicOrmTest, test_public_model_fields) {
    MyPublicModel obj("Alice Wonderland", 35);
    EXPECT_EQ(obj.name, "Alice Wonderland");
    EXPECT_EQ(obj.age, 35);
}

TEST(PublicOrmTest, test_public_model_update_fields) {
    MyPublicModel obj("Bob Builder", 44);
    obj.name = "Bobby";
    obj.age = 45;
    EXPECT_EQ(obj.name, "Bobby");
    EXPECT_EQ(obj.age, 45);
}

TEST(PublicOrmTest, test_public_model_repository) {
    repositories::InMemoryRepository repo;
    MyPublicModel obj("Charlie Delta", 27);
    repo.save(obj);
    const MyPublicModel& found = repo.storage.front();
    EXPECT_EQ(found.name, "Charlie Delta");
    EXPECT_EQ(found.age, 27);
    auto it = std::find_if(repo.storage.begin(), repo.storage.end(),
                           [](const MyPublicModel& o) { return o.name == "Charlie Delta" && o.age == 27; });
    EXPECT_NE(it, repo.storage.end());
}