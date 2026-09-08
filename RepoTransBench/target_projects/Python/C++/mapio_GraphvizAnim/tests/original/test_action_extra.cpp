#include <gtest/gtest.h>
#include "action.h"
#include <vector>

TEST(ActionExtraTest, AddNodeAction) {
    std::vector<Step> s{Step()};
    AddNode(42)(s);
    EXPECT_NE(s.back().V.find(42), s.back().V.end());
}

TEST(ActionExtraTest, HighlightNodeAndLabelNode) {
    std::vector<Step> s{Step()};
    HighlightNode(2, "blue")(s);
    LabelNode(2, "lbl")(s);
    EXPECT_NE(s.back().hV.find(2), s.back().hV.end());
    EXPECT_NE(s.back().lV.find(2), s.back().lV.end());
}

TEST(ActionExtraTest, UnlabelAndRemoveNode) {
    std::vector<Step> s{Step()};
    AddNode(1)(s);
    LabelNode(1, "tok")(s);
    UnlabelNode(1)(s);
    EXPECT_EQ(s.back().lV.find(1), s.back().lV.end());
    RemoveNode(1)(s);
    EXPECT_EQ(s.back().V.find(1), s.back().V.end());
}

TEST(ActionExtraTest, AddEdgeAndHighlightLabelUnlabelRemove) {
    std::vector<Step> s{Step()};
    AddNode(3)(s);
    AddNode(4)(s);
    AddEdge(3, 4)(s);
    HighlightEdge(3, 4, "green")(s);
    LabelEdge(3, 4, "X")(s);
    EXPECT_NE(s.back().E.find({3, 4}), s.back().E.end());
    EXPECT_NE(s.back().hE.find({3, 4}), s.back().hE.end());
    EXPECT_NE(s.back().lE.find({3, 4}), s.back().lE.end());
    UnlabelEdge(3, 4)(s);
    RemoveEdge(3, 4)(s);
    EXPECT_EQ(s.back().E.find({3, 4}), s.back().E.end());
}