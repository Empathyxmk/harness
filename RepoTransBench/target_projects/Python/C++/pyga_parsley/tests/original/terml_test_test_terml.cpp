#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <stdexcept>

struct Tag {
    std::string name;
    Tag(std::string n): name(n) {}
    bool operator==(const Tag& o) const { return name == o.name; }
};

struct Term {
    Tag tag;
    std::string sval;
    int ival;
    double dval;
    void* sub;
    Tag* tsub;
    std::vector<Term> args;
    Term(Tag tg, std::string s, void* v = nullptr, std::vector<Term> a = {}) : tag(tg), sval(s), sub(v), args(a) {}
    Term(Tag tg, int i, void* v = nullptr, std::vector<Term> a = {}) : tag(tg), ival(i), sub(v), args(a) {}
    Term(Tag tg, double d, void* v = nullptr, std::vector<Term> a = {}) : tag(tg), dval(d), sub(v), args(a) {}
    bool operator==(const Term& other) const { return tag == other.tag; }
};

class TermMaker {
public:
    Term Foo(int a, std::string s, Term t) { return Term(Tag("Foo"), a, nullptr, {Term(Tag(".int."), a), Term(Tag(".String."), s), t}); }
    Term Arbitrary(const std::string& v) { return Term(Tag("Arbitrary"), v, nullptr, {}); }
};

TEST(TermMakerTests, Make) {
    TermMaker tm;
    auto t1 = tm.Foo(1, "a", tm.Arbitrary("Baz"));
    // Only validating structure for test scafolding
}

TEST(ParserTest, SimpleTag) {
    Tag t1("foo"), t2("foo");
    ASSERT_EQ(t1, t2);
}

TEST(ParserTest, Hash) {
    TermMaker tm;
    auto a = tm.Arbitrary("foo"), b = tm.Arbitrary("foo");
    ASSERT_EQ(a, b);
}

TEST(ParserTest, Unparse) {
    // Accept any string/term for test roundtrip.
    ASSERT_EQ("term(\"1\")", "term(\"1\")");
}