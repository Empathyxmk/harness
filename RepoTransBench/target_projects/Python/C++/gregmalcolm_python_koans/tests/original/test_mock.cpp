#include "gtest/gtest.h"
#include "lib/mock.h"
#include <tuple>
#include <set>
#include <vector>
#include <map>
#include <stdexcept>

TEST(TestMock, SentinelObjectRepr) {
    SentinelObject s("MY_MARK");
    EXPECT_EQ(s.repr(), "<SentinelObject \"MY_MARK\">");
}

TEST(TestMock, SentinelAttributeUniqueness) {
    Sentinel s;
    auto a = s.foo();
    auto b = s.foo();
    auto c = s.bar();
    EXPECT_EQ(&a, &b);
    EXPECT_NE(&a, &c);
}

TEST(TestMock, DefaultAndClassType) {
    EXPECT_TRUE(sentinel_has_DEFAULT());
    EXPECT_TRUE(ClassType_is_type());
}

TEST(TestMock, DotLookupBasic) {
    struct X { static int foo; };
    int X::foo = 123;
    EXPECT_EQ(_dot_lookup<X>("foo"), 123);
}

TEST(TestMock, CopyListsDictsTuplesSets) {
    std::vector<int> lst = {1,2};
    EXPECT_EQ(_copy(lst), lst);
    std::map<std::string,int> dct = { {"a",1} };
    EXPECT_EQ(_copy(dct), dct);
    std::tuple<int,int> tpl (1,2);
    EXPECT_EQ(_copy(tpl), tpl);
    std::set<int> st = {1,2};
    EXPECT_EQ(_copy(st), st);
    int s = 12;
    EXPECT_EQ(_copy(s), s);
}

TEST(TestMock, MockBasicsAndMethods) {
    Mock m;
    m(1,2, {{"x",3}});
    EXPECT_TRUE(m.called());
    EXPECT_EQ(m.call_count(), 1);
    auto call_args = m.call_args();
    EXPECT_EQ(std::get<0>(call_args)[0], 1);
    EXPECT_EQ(std::get<1>(call_args)["x"], 3);
    m.reset_mock();
    EXPECT_FALSE(m.called());
    Mock m2;
    m2.set_return_value("abc");
    std::string rv = m2();
    EXPECT_EQ(rv, "abc");
    m2(1,2);
    EXPECT_TRUE(m2.assert_called_with({1,2}));
}

TEST(TestMock, MockSideEffectLambda) {
    Mock m;
    m.set_side_effect([](int a){ return a*2; });
    EXPECT_EQ(m(4), 8);
}

TEST(TestMock, MockSideEffectException) {
    Mock m;
    m.set_side_effect([](){ throw std::runtime_error("fail"); return 0; });
    EXPECT_THROW(m(), std::runtime_error);
}

TEST(TestMock, MockSpecBlocksNonexistent) {
    Mock m;
    m.set_spec({"foo"});
    m.foo();
    EXPECT_THROW(m.bar(), std::runtime_error);
}

TEST(TestMock, MockWraps) {
    auto f = [](int x){ return x+1; };
    Mock m;
    m.set_wraps(f);
    EXPECT_EQ(m(3), 4);
}

TEST(TestMock, MagicMethodsBlocked) {
    Mock m;
    EXPECT_THROW(m.magic_method("__foobar__"), std::runtime_error);
}