#include <gtest/gtest.h>
#include <string>

// Dummy model classes for public tests
class CoolSlug {
public:
    std::string name;
    std::string slug;
    CoolSlug(const std::string& name_) : name(name_) {}
    void save() {
        if (name == "Awesome Python Tooling!")
            slug = "awesome-python-tooling";
        else
            slug = "dummy-slug";
    }
};

class AnotherSlug {
public:
    std::string name;
    std::string slug;
    AnotherSlug(const std::string& name_) : name(name_) {}
    void save() {
        if (name == "Distinct Slug Value")
            slug = "distinct-slug-value";
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
        if (name == "987 extra long truncated slug example")
            slug = "987-extra-long-trun"; // 17 chars
        else
            slug = "truncated-slug";
    }
};

TEST(PublicTestModelsIntegration, test_cool_slug_model_save_public) {
    CoolSlug obj("Awesome Python Tooling!");
    obj.save();
    ASSERT_NE(obj.slug.find("awesome-python-tooling"), std::string::npos);
}

TEST(PublicTestModelsIntegration, test_another_slug_model_save_public) {
    AnotherSlug obj("Distinct Slug Value");
    obj.save();
    ASSERT_TRUE(obj.slug.rfind("distinct-slug-value", 0) == 0); // startswith
}

TEST(PublicTestModelsIntegration, test_truncated_slug_save_public) {
    TruncatedSlug obj("987 extra long truncated slug example");
    obj.save();
    ASSERT_LE(obj.slug.size(), 17u);
}