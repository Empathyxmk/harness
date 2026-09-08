#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicWikipediaPageTest, PublicPageSections) {
    Wikipedia wiki("public-page/1.0", "en");
    auto page = wiki.page("Geography");
    auto sections = page.sections();
    ASSERT_TRUE(typeid(sections) == typeid(std::vector<Section>));
    ASSERT_TRUE(std::any_of(
        sections.begin(), sections.end(),
        [](const Section& sec) {
            auto title = sec.title();
            std::transform(title.begin(), title.end(), title.begin(), ::tolower);
            return title.find("phy") != std::string::npos ||
                   title.find("geo") != std::string::npos;
        }
    ));
}

TEST(PublicWikipediaPageTest, PublicPageLangLinks) {
    Wikipedia wiki("public-page/2.0", "en");
    auto page = wiki.page("Sun");
    auto langlinks = page.langlinks();
    ASSERT_TRUE(typeid(langlinks) == typeid(std::unordered_map<std::string, WikipediaPagePtr>));
    ASSERT_TRUE(langlinks.contains("es") || langlinks.contains("fr"));
}