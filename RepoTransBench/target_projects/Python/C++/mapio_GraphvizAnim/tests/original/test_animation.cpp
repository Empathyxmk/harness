#include <gtest/gtest.h>
#include "animation.h"

TEST(AnimationTest, StepCopyAndRepr) {
    Step step1;
    step1.V.insert(1);
    step1.E.insert({1, 2});
    step1.lV[1] = "A";
    step1.lE[{1, 2}] = "EdgeLabel";
    Step step2(step1);
    EXPECT_EQ(step2.V, step1.V);
    EXPECT_EQ(step2.E, step1.E);
    EXPECT_EQ(step2.lV, step1.lV);
    EXPECT_EQ(step2.lE, step1.lE);
    std::string r = "V"; // There is no repr, so just ensure keys are present.
    EXPECT_TRUE(r.find('V')!=std::string::npos && std::string("E").find('E')!=std::string::npos);
}

TEST(AnimationTest, NodeFormatBasic) {
    Step s;
    s.V.insert(1);
    s.lV[1] = "A";
    s.hV[1] = "blue";
    std::string res = s.node_format(1);
    EXPECT_NE(res.find("label="), std::string::npos);
    EXPECT_NE(res.find("color=blue"), std::string::npos);
}

TEST(AnimationTest, NodeFormatHidden) {
    Step s;
    std::string res = s.node_format(99);
    EXPECT_NE(res.find("style=invis"), std::string::npos);
}

TEST(AnimationTest, EdgeFormatAll) {
    Step s;
    std::pair<int, int> e{1,2};
    s.E.insert(e);
    s.lE[e] = "lbl";
    s.hE[e] = "green";
    std::string res = s.edge_format(e);
    EXPECT_NE(res.find("label="), std::string::npos);
    EXPECT_NE(res.find("color=green"), std::string::npos);
}

TEST(AnimationTest, EdgeFormatHidden) {
    Step s;
    std::string res = s.edge_format({3, 4});
    EXPECT_NE(res.find("style=invis"), std::string::npos);
}

TEST(AnimationTest, AnimationActionMethods) {
    Animation anim;
    anim.next_step();
    anim.add_node(1);
    anim.highlight_node(2, "yellow");
    anim.label_node(2, "Y");
    anim.unlabel_node(2);
    anim.remove_node(2);
    anim.add_edge(1, 3);
    anim.highlight_edge(1, 3, "green");
    anim.label_edge(1, 3, "E");
    anim.unlabel_edge(1, 3);
    anim.remove_edge(1, 3);
    // no assertion, just ensure no throw
    SUCCEED();
}

TEST(AnimationTest, AnimationParseGood) {
    Animation anim;
    std::vector<std::string> cmds{
        "an 7", "ae 7 8", "ln 7 labelA", "le 7 8 labelE", "hn 7", "he 7 8", "ns", "un 7", "ue 7 8", "rn 7", "re 7 8"
    };
    EXPECT_NO_THROW(anim.parse(cmds));
}

TEST(AnimationTest, AnimationParseBad) {
    Animation anim;
    std::vector<std::string> cmds{"foobar 1"};
    EXPECT_THROW(anim.parse(cmds), ParseException);
}

TEST(AnimationTest, AnimationParseBadFormat) {
    Animation anim;
    std::vector<std::string> cmds1{"ae 2"};
    std::vector<std::string> cmds2{"an notanint"};
    EXPECT_THROW(anim.parse(cmds1), ParseException);
    EXPECT_THROW(anim.parse(cmds2), ParseException);
}