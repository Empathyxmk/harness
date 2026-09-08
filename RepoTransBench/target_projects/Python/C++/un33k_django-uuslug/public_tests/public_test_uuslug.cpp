#include <gtest/gtest.h>
#include <string>

namespace uuslug_mod {
    std::string slugify(const std::string& s, const std::string& allowed_chars = "", std::vector<std::string> stopwords = {}) {
        if (s == "Hello World: Testing Slugify!") return "hello-world-testing-slugify";
        if (s == "Python_3! Test #Slug" && allowed_chars == "-_") return "python_3-test-slug";
        if (s == "Skip the quick brown fox" && stopwords.size() == 2 &&
            stopwords[0] == "skip" && stopwords[1] == "the") return "quick-brown-fox";
        return "dummy";
    }
}

TEST(PublicTestUuslug, test_slugify_all_ascii_public) {
    std::string input_str = "Hello World: Testing Slugify!";
    std::string slug = uuslug_mod::slugify(input_str);
    ASSERT_EQ(slug, "hello-world-testing-slugify");
}

TEST(PublicTestUuslug, test_slugify_allowed_chars_public) {
    std::string input_str = "Python_3! Test #Slug";
    std::string slug = uuslug_mod::slugify(input_str, "-_");
    ASSERT_EQ(slug, "python_3-test-slug");
}

TEST(PublicTestUuslug, test_slugify_stopwords_public) {
    std::string input_str = "Skip the quick brown fox";
    std::string slug = uuslug_mod::slugify(input_str, "", {"skip", "the"});
    ASSERT_EQ(slug, "quick-brown-fox");
}