#include <gtest/gtest.h>
#include "pymsteams.h"

using namespace pymsteams;

TEST(CardSection, Basic) {
    cardsection section;
    EXPECT_EQ(&section, &section.title("title text"));
    EXPECT_EQ(get_string(section.payload["title"]), "title text");
    EXPECT_EQ(get_string(section.activityTitle("activity").payload["activityTitle"]), "activity");
    EXPECT_EQ(get_string(section.activitySubtitle("subtitle").payload["activitySubtitle"]), "subtitle");
    EXPECT_EQ(get_string(section.activityImage("http://image.png").payload["activityImage"]), "http://image.png");
    EXPECT_EQ(get_string(section.activityText("text here").payload["activityText"]), "text here");
    EXPECT_EQ(get_string(section.text("hello").payload["text"]), "hello");
    section.linkButton("Go", "http://go.com");
    auto pActions = get_vecmap(section.payload["potentialAction"]);
    ASSERT_FALSE(pActions.empty());
    EXPECT_EQ(get_string(pActions[0]["name"]), "Go");
    EXPECT_FALSE(get_bool(section.disableMarkdown().payload["markdown"]));
    EXPECT_TRUE(get_bool(section.enableMarkdown().payload["markdown"]));
    auto dumped = section.dumpSection();
    EXPECT_FALSE(dumped.empty());
}

TEST(CardSection, AddFactAndAddImage) {
    cardsection section;
    section.addFact("f1", "v1");
    auto facts = get_vecmap(section.payload["facts"]);
    ASSERT_EQ(facts.size(), 1);
    EXPECT_EQ(get_string(facts[0]["name"]), "f1");
    EXPECT_EQ(get_string(facts[0]["value"]), "v1");
    section.addFact("f2", "v2");
    auto facts2 = get_vecmap(section.payload["facts"]);
    EXPECT_EQ(facts2.size(), 2);
    section.addImage("http://img.com/img.jpg", "image1");
    auto images = get_vecmap(section.payload["images"]);
    EXPECT_EQ(get_string(images[0]["title"]), "image1");
    section.addImage("http://img.com/img2.jpg");
    auto images2 = get_vecmap(section.payload["images"]);
    EXPECT_EQ(images2.size(), 2);
    EXPECT_TRUE(images2[0].count("title"));
    EXPECT_FALSE(images2[1].count("title"));
}

TEST(CardSection, FactAndImageKeys) {
    cardsection section;
    section.payload["facts"] = std::vector<std::map<std::string, std::any>>{{{"name", "start"}, {"value", "val"}}};
    section.addFact("foo", "bar");
    auto facts = get_vecmap(section.payload["facts"]);
    EXPECT_EQ(facts.size(), 2);
    section.payload["images"] = std::vector<std::map<std::string, std::any>>{{{"image", "test"}}};
    section.addImage("img-url");
    auto images = get_vecmap(section.payload["images"]);
    EXPECT_EQ(images.size(), 2);
}

TEST(PotentialAction, InputsAndActions) {
    potentialaction pa("TestAction");
    pa.addInput("TextInput", "inputid", "My Title", true);
    auto inputs = get_vecmap(pa.payload["inputs"]);
    ASSERT_FALSE(inputs.empty());
    if (inputs[0].count("isMultiline"))
        EXPECT_TRUE(get_bool(inputs[0]["isMultiline"]));
    pa.addInput("ChoiceInput", "input2", "Another", false);
    if (true) {
        pa.addChoice("display", "value");
        auto newinputs = get_vecmap(pa.payload["inputs"]);
        EXPECT_TRUE(newinputs.back().count("choices"));
    }
    pa.addAction("ActionType", "ActionName", {"http://example.com"});
    auto actions = get_vecmap(pa.payload["actions"]);
    ASSERT_FALSE(actions.empty());
    EXPECT_EQ(get_string(actions[0]["@type"]), "ActionType");
    pa.addAction("type", "name", {"url"}, "body here");
    actions = get_vecmap(pa.payload["actions"]);
    EXPECT_EQ(get_string(actions[1]["body"]), "body here");
}

TEST(PotentialAction, AddOpenURIAndExceptions) {
    potentialaction pa("opentest");
    std::vector<std::map<std::string, std::any>> targets = { {{"os", "default"}, {"uri", "https://foo.bar/"}} };
    pa.addOpenURI("OpenName", targets);
    auto newtargs = get_vecmap(pa.payload["targets"]);
    ASSERT_EQ(newtargs.size(), 1);
    EXPECT_EQ(get_string(newtargs[0]["uri"]), "https://foo.bar/");
    EXPECT_THROW(pa.addOpenURI("Broken", {}), std::invalid_argument);
}

TEST(PotentialAction, Dump) {
    potentialaction pa("dumpTest");
    auto dumped = pa.dumpPotentialAction();
    EXPECT_FALSE(dumped.empty());
}

TEST(TeamsWebhookException, Repr) {
    TeamsWebhookException ex("fail");
    EXPECT_STREQ(ex.what(), std::string("fail").c_str());
}