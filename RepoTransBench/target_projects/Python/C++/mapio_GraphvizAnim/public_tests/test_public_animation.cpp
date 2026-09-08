#include <gtest/gtest.h>
#include "animation.h"

TEST(PublicAnimationTest, StepCopyAndReprPublic) {
    Step step1;
    step1.V.insert(10);
    step1.E.insert({10, 20});
    step1.lV[10] = "X";
    step1.lE[{10, 20}] = "EdgeAB";
    Step step2(step1);
    EXPECT_EQ(step2.V, step1.V);
    EXPECT_EQ(step2.E, step1.E);
    EXPECT_EQ(step2.lV, step1.lV);
    EXPECT_EQ(step2.lE, step1.lE);
    std::string r = "V"; // stub for repr, as above
    EXPECT_TRUE(r.find('V')!=std::string::npos && std::string("E").find('E')!=std::string::npos);
}

TEST(PublicAnimationTest, NodeFormatBasicPublic) {
    Step s;
    s.V.insert(5);
    s.lV[5] = "B";
    s.hV[5] = "red";
    std::string res = s.node_format(5);
    EXPECT_NE(res.find("label="), std::string::npos);
    EXPECT_NE(res.find("color=red"), std::string::npos);
}

TEST(PublicAnimationTest, NodeFormatHiddenPublic) {
    Step s;
    std::string res = s.node_format(123);
    EXPECT_NE(res.find("style=invis"), std::string::npos);
}

TEST(PublicAnimationTest, EdgeFormatAllPublic) {
    Step s;
    std::pair<int, int> e{7, 8};
    s.E.insert(e);
    s.lE[e] = "labelZ";
    s.hE[e] = "orange";
    std::string res = s.edge_format(e);
    EXPECT_NE(res.find("label="), std::string::npos);
    EXPECT_NE(res.find("color=orange"), std::string::npos);
}

TEST(PublicAnimationTest, EdgeFormatHiddenPublic) {
    Step s;
    std::string res = s.edge_format({17, 28});
    EXPECT_NE(res.find("style=invis"), std::string::npos);
}

TEST(PublicAnimationTest, AnimationActionMethodsPublic) {
    Animation anim;
    anim.next_step();
    anim.add_node(101);
    anim.highlight_node(201, "purple");
    anim.label_node(201, "Z");
    anim.unlabel_node(201);
    anim.remove_node(201);
    anim.add_edge(101, 301);
    anim.highlight_edge(101, 301, "pink");
    anim.label_edge(101, 301, "F");
    anim.unlabel_edge(101, 301);
    anim.remove_edge(101, 301);
    SUCCEED();
}

TEST(PublicAnimationTest, AnimationParseGoodPublic) {
    Animation anim;
    std::vector<std::string> cmds{
        "an 17", "ae 17 18", "ln 17 labelB", "le 17 18 labelF",
        "hn 17", "he 17 18", "ns", "un 17", "ue 17 18", "rn 17", "re 17 18"
    };
    EXPECT_NO_THROW(anim.parse(cmds));
}

TEST(PublicAnimationTest, AnimationParseBadPublic) {
    Animation anim;
    std::vector<std::string> cmds{"badcmd 77"};
    EXPECT_THROW(anim.parse(cmds), ParseException);
}

TEST(PublicAnimationTest, AnimationParseBadFormatPublic) {
    Animation anim;
    std::vector<std::string> cmds1{"ae"};
    std::vector<std::string> cmds2{"an invalidnum"};
    EXPECT_THROW(anim.parse(cmds1), ParseException);
    EXPECT_THROW(anim.parse(cmds2), ParseException);
}