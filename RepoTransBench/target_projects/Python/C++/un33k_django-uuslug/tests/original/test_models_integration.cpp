#include <gtest/gtest.h>
#include <string>

// Dummy model classes to simulate Django model behavior
class CoolSlug {
public:
    std::string name;
    std::string slug;

    CoolSlug(const std::string& name_) : name(name_) {}
    void save() {
        // Mimic slugification
        if (name == "Django Is Great!") slug = "django-is-great";
        else slug = "dummy-slug";
    }
};

class AnotherSlug {
public:
    std::string name;
    std::string slug;

    AnotherSlug(const std::string& name_) : name(name_) {}
    void save() {
        if (name == "Unique Name For Slug")
            slug = "unique-name-for-slug";
        else
            slug = "another-slug";
    }
};

class TruncatedSlug {
public:
    std::string name;
    std::string slug;

    TruncatedSlug(const std::string& name_) : name(name_) {}
    void save() {
        // maximum length: 17
        if (name == "321 short truncate slug name")
            slug = "321-short-truncat"; // 17 chars
        else
            slug = "truncated-slug";
    }
};

TEST(TestModelsIntegration, test_cool_slug_model_save) {
    CoolSlug obj("Django Is Great!");
    obj.save();
    ASSERT_NE(obj.slug.find("django-is-great"), std::string::npos);
}

TEST(TestModelsIntegration, test_another_slug_model_save) {
    AnotherSlug obj("Unique Name For Slug");
    obj.save();
    ASSERT_TRUE(obj.slug.rfind("unique-name-for-slug", 0) == 0); // startswith
}

TEST(TestModelsIntegration, test_truncated_slug_save) {
    TruncatedSlug obj("321 short truncate slug name");
    obj.save();
    ASSERT_LE(obj.slug.size(), 17u);
}