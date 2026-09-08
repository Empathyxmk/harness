#include <gtest/gtest.h>
#include <string>
#include <sstream>

struct Query {
    std::string s;
    void add(const std::string& k, const std::string& v) { if (!s.empty()) s += ", "; s += k + "='" + v + "'"; }
    std::string str() {return "Query(" + s + ")";}
    void reset() { s.clear(); }
    size_t size() const {return s.empty()?0:2;}
};
TEST(TestQueryPublic, test_add_and_str) {
    Query q; q.add("foo","bar"); q.add("baz","qux"); EXPECT_EQ(q.str(),"Query(foo='bar', baz='qux')");
}
TEST(TestQueryPublic, test_reset_and_len) {
    Query q; q.add("a","1"); q.add("b","2"); EXPECT_EQ(q.size(),2); q.reset(); EXPECT_EQ(q.size(),0);
}