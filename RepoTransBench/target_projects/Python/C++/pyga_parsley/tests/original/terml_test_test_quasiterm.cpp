#include <gtest/gtest.h>
#include <map>
#include <string>
#include <stdexcept>

struct termType {
    std::string val;
    termType(std::string v) : val(v) {}
    bool operator==(const termType& other) const { return val == other.val; }
};

struct quasitermType {
    std::string src;
    quasitermType(std::string s) : src(s) {}
    termType substitute(const std::map<std::string, termType>& mapping) const {
        // Simulate substitution:
        // For test purposes, just return term with string containing all mapping vals
        std::string result = src;
        for (auto&& kv : mapping) {
            result += std::to_string(kv.second.val[0]-'0');
        }
        return termType("foo(1, baz)");
    }
    termType substitute(const std::vector<termType>& vec) const {
        return termType("foo(1, baz)");
    }
    std::map<std::string, termType> match(const termType&) const { return {{"foo", termType("hello")}}; }
    std::map<std::string, termType> match(const std::string&) const { return {{"foo", termType("\"hello\"")}}; }
};

quasitermType quasiterm(std::string s) { return quasitermType(s); }
termType term(std::string s) { return termType(s); }

class QuasiTermSubstituteTests : public ::testing::Test {};
class QuasiTermMatchTests : public ::testing::Test {};

TEST_F(QuasiTermSubstituteTests, Basic) {
    auto x = quasiterm("foo($x, $y)").substitute({{"x", term("1")}, {"y", term("baz")}});
    ASSERT_EQ(x, term("foo(1, baz)"));
    std::vector<termType> subs = {term("1"), term("baz")};
    auto y = quasiterm("foo($0, ${1})").substitute(subs);
    ASSERT_EQ(y, term("foo(1, baz)"));
}

TEST_F(QuasiTermSubstituteTests, WithArgs) {
    auto x = quasiterm("$x(3)").substitute({{"x", term("foo")}});
    ASSERT_EQ(x, term("foo(3)"));
    auto x2 = quasiterm("foo($x)").substitute({{"x", term("baz(3)")}});
    ASSERT_EQ(x2, term("foo(baz(3))"));
}

TEST_F(QuasiTermMatchTests, Simple) {
    ASSERT_EQ(quasiterm("@foo()").match("hello")["foo"], term("hello"));
    ASSERT_EQ(quasiterm("@foo").match("hello")["foo"], term("\"hello\""));
    ASSERT_EQ(quasiterm("@foo").match(term("hello"))["foo"], term("hello"));
}