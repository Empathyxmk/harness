#include <gtest/gtest.h>
#include "action.h"
#include <vector>

TEST(PublicActionExtraTest, AddNodeActionPublic) {
    std::vector<Step> s{Step()};
    AddNode(12)(s);
    EXPECT_NE(s.back().V.find(12), s.back().V.end());
}

TEST(PublicActionExtraTest, HighlightNodeAndLabelNodePublic) {
    std::vector<Step> s{Step()};
    HighlightNode(20, "red")(s);
    LabelNode(20, "lbl2")(s);
    EXPECT_NE(s.back().hV.find(20), s.back().hV.end());
    EXPECT_NE(s.back().lV.find(20), s.back().lV.end());
}

TEST(PublicActionExtraTest, UnlabelAndRemoveNodePublic) {
    std::vector<Step> s{Step()};
    AddNode(9)(s);
    LabelNode(9, "zzz")(s);
    UnlabelNode(9)(s);
    EXPECT_EQ(s.back().lV.find(9), s.back().lV.end());
    RemoveNode(9)(s);
    EXPECT_EQ(s.back().V.find(9), s.back().V.end());
}

TEST(PublicActionExtraTest, AddEdgeAndHighlightLabelUnlabelRemovePublic) {
    std::vector<Step> s{Step()};
    AddNode(6)(s);
    AddNode(13)(s);
    AddEdge(6, 13)(s);
    HighlightEdge(6, 13, "purple")(s);
    LabelEdge(6, 13, "Y")(s);
    EXPECT_NE(s.back().E.find({6, 13}), s.back().E.end());
    EXPECT_NE(s.back().hE.find({6, 13}), s.back().hE.end());
    EXPECT_NE(s.back().lE.find({6, 13}), s.back().lE.end());
    UnlabelEdge(6, 13)(s);
    RemoveEdge(6, 13)(s);
    EXPECT_EQ(s.back().E.find({6, 13}), s.back().E.end());
}