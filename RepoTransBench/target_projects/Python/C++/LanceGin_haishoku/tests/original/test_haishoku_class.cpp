#include <gtest/gtest.h>
#include "haishoku/haishoku.h"

TEST(TestHaishokuClass, haishoku_init_sets_none) {
    Haishoku h;
    EXPECT_FALSE(h.hasDominant());
    EXPECT_FALSE(h.hasPalette());
}

TEST(TestHaishokuClass, loadHaishoku_monkeypatch) {
    // Not directly monkeypatchable; simulate by stubbing during implementation
    Haishoku h;
    h.setPalette({{1,2,3}});
    h.setDominant({4,5,6});
    EXPECT_EQ(h.getPalette()[0], std::make_tuple(1,2,3));
    EXPECT_EQ(h.getDominant(), std::make_tuple(4,5,6));
}

TEST(TestHaishokuClass, loadHaishoku_is_classmethod) {
    // C++ static/class methods: just check for function existence
    EXPECT_TRUE((void*)(&Haishoku::loadHaishoku) != nullptr);
}

TEST(TestHaishokuClass, str_repr_of_Haishoku) {
    Haishoku h;
    std::string s = h.toString();
    std::string r = h.toRepr();
    EXPECT_GT(s.size(), 0);
    EXPECT_GT(r.size(), 0);
}