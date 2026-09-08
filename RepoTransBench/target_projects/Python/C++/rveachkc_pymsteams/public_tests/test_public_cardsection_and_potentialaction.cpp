#include <gtest/gtest.h>
#include "pymsteams.h"

using namespace pymsteams;

TEST(PublicCardSection, BasicPublic) {
    cardsection section;
    EXPECT_EQ(&section, &section.title("Public Section Title"));
    EXPECT_EQ(get_string(section.payload["title"]), "Public Section Title");
    EXPECT_EQ(get_string(section.activityTitle("public activity").payload["activityTitle"]), "public activity");
    EXPECT_EQ(get_string(section.activitySubtitle("public subtitle").payload["activitySubtitle"]), "public subtitle");
    EXPECT_EQ(get_string(section.activityImage("https://example.com/img.png").payload["activityImage"]), "https://example.com/img.png");
    EXPECT_EQ(get_string(section.activityText("public text here").payload["activityText"]), "public text here");
    EXPECT_EQ(get_string(section.text("greetings").payload["text"]), "greetings");
    section.linkButton("Visit", "https://visit.com");
    auto pActions = get_vecmap(section.payload["potentialAction"]);
    ASSERT_FALSE(pActions.empty());
    EXPECT_EQ(get_string(pActions[0]["name"]), "Visit");
    EXPECT_FALSE(get_bool(section.disableMarkdown().payload["markdown"]));
    EXPECT_TRUE(get_bool(section.enableMarkdown().payload["markdown"]));
    auto dumped = section.dumpSection();
    EXPECT_FALSE(dumped.empty());
}

TEST(PublicCardSection, AddFactAndAddImagePublic) {
    cardsection section;
    section.addFact("fact_one", "value_one");
    auto facts = get_vecmap(section.payload["facts"]);
    ASSERT_EQ(facts.size(), 1);
    EXPECT_EQ(get_string(facts[0]["name"]), "fact_one");
    EXPECT_EQ(get_string(facts[0]["value"]), "value_one");
    section.addFact("fact_two", "value_two");
    auto facts2 = get_vecmap(section.payload["facts"]);
    EXPECT_EQ(facts2.size(), 2);
    section.addImage("https://img-server.com/photo1.jpg", "photo title");
    auto images = get_vecmap(section.payload["images"]);
    EXPECT_EQ(get_string(images[0]["title"]), "photo title");
    section.addImage("https://img-server.com/photo2.jpg");
    auto images2 = get_vecmap(section.payload["images"]);
    EXPECT_EQ(images2.size(), 2);
    EXPECT_TRUE(images2[0].count("title"));
    EXPECT_FALSE(images2[1].count("title"));
}

TEST(PublicCardSection, FactAndImageKeysPublic) {
    cardsection section;
    section.payload["facts"] = std::vector<std::map<std::string, std::any>>{{{"name", "init_name"}, {"value", "init_val"}}};
    section.addFact("another_name", "another_val");
    auto facts = get_vecmap(section.payload["facts"]);
    EXPECT_EQ(facts.size(), 2);
    section.payload["images"] = std::vector<std::map<std::string, std::any>>{{{"image", "img_obj"}}};
    section.addImage("more-img-url");
    auto images = get_vecmap(section.payload["images"]);
    EXPECT_EQ(images.size(), 2);
}

TEST(PublicPotentialAction, InputsAndActionsPublic) {
    potentialaction pa("PublicAction");
    pa.addInput("TextInput", "pub_input", "Public Input Title", false);
    auto inputs = get_vecmap(pa.payload["inputs"]);
    ASSERT_FALSE(inputs.empty());
    if (inputs[0].count("isMultiline")) {
        EXPECT_FALSE(get_bool(inputs[0]["isMultiline"]));
    }
    pa.addInput("ChoiceInput", "pub_input2", "Public Choice Input", true);
    if (true) {
        pa.addChoice("pub_display", "pub_value");
        auto newinputs = get_vecmap(pa.payload["inputs"]);
        EXPECT_TRUE(newinputs.back().count("choices"));
    }
    pa.addAction("CustomActionType", "ActionPublic", {"https://example.org"});
    auto actions = get_vecmap(pa.payload["actions"]);
    ASSERT_FALSE(actions.empty());
    EXPECT_EQ(get_string(actions[0]["@type"]), "CustomActionType");
    pa.addAction("secondtype", "publicaction", {"weburl"}, "some body here");
    actions = get_vecmap(pa.payload["actions"]);
    EXPECT_EQ(get_string(actions[1]["body"]), "some body here");
}

TEST(PublicPotentialAction, AddOpenURIAndExceptionsPublic) {
    potentialaction pa("testopen");
    std::vector<std::map<std::string, std::any>> targets = {{ {"os", "mobile"}, {"uri", "https://other-url.com/"} }};
    pa.addOpenURI("OpenOther", targets);
    auto newtargs = get_vecmap(pa.payload["targets"]);
    ASSERT_EQ(newtargs.size(), 1);
    EXPECT_EQ(get_string(newtargs[0]["uri"]), "https://other-url.com/");
    EXPECT_THROW(pa.addOpenURI("Failer", {}), std::invalid_argument);
}

TEST(PublicPotentialAction, DumpPublic) {
    potentialaction pa("dumpPA");
    auto dumped = pa.dumpPotentialAction();
    EXPECT_FALSE(dumped.empty());
}

TEST(PublicTeamsWebhookException, ReprPublic) {
    TeamsWebhookException ex("public fail");
    EXPECT_STREQ(ex.what(), std::string("public fail").c_str());
}