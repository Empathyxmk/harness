#include "gtest/gtest.h"
#include "lib/mock.h"
#include <string>

TEST(TestPublicMockExample, PublicBasicMock) {
    Mock m;
    EXPECT_TRUE(Mock::is_instance(m));
    m.hello([&](){ return std::string("moon"); });
    EXPECT_EQ(m.hello(), "moon");
}

TEST(TestPublicMockExample, PublicSideEffect) {
    std::vector<std::string> val;
    Mock m;
    m.set_side_effect([&](){ val.push_back("invoked"); });
    m();
    auto it = std::find(val.begin(), val.end(), "invoked");
    EXPECT_TRUE(it != val.end());
}

TEST(TestPublicMockExample, PublicCallArgs) {
    Mock m;
    m("b", {{"c", "y"}});
    auto args = m.call_args();
    EXPECT_EQ(args.first[0], std::string("b"));
    EXPECT_EQ(args.second["c"], std::string("y"));
}

TEST(TestPublicMockExample, PublicMockReturnValue) {
    Mock m;
    m.set_return_value(55);
    EXPECT_EQ(m(), 55);
    m.set_return_value(23);
    EXPECT_EQ(m(), 23);
}

TEST(TestPublicMockExample, PublicMockReset) {
    Mock m;
    m("b");
    EXPECT_TRUE(m.called());
    m.reset_mock();
    EXPECT_FALSE(m.called());
}

TEST(TestPublicMockCalls, PublicMultipleCalls) {
    Mock m;
    m(11);
    m(22);
    EXPECT_EQ(m.call_count(), 2);
    auto call_args_list = m.call_args_list();
    EXPECT_EQ(call_args_list[0].first[0], 11);
    EXPECT_EQ(call_args_list[1].first[0], 22);
}

TEST(TestPublicMockCalls, PublicAssertCalledWith) {
    Mock m;
    m(999, {{"z",888}});
    EXPECT_TRUE(m.assert_called_with({999}, {{"z",888}}));
}