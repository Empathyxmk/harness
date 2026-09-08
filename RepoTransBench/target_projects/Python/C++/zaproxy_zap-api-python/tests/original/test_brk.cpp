#include <gtest/gtest.h>
#include "BrkModule.h"
#include "DummyZAP.h"

class BrkTest : public ::testing::Test {
protected:
    DummyZAP dummyZap;
    Brk* brk;
    void SetUp() override {
        brk = new Brk(&dummyZap);
    }
    void TearDown() override {
        delete brk;
    }
};

TEST_F(BrkTest, IsBreakAll) {
    ASSERT_EQ(brk->is_break_all(), "dummy");
}
TEST_F(BrkTest, IsBreakRequest) {
    ASSERT_EQ(brk->is_break_request(), "dummy");
}
TEST_F(BrkTest, IsBreakResponse) {
    ASSERT_EQ(brk->is_break_response(), "dummy");
}
TEST_F(BrkTest, HttpMessage) {
    ASSERT_EQ(brk->http_message(), "dummy");
}
TEST_F(BrkTest, BrkTypeState) {
    ASSERT_EQ(brk->brk("http-all", "true"), "dummy");
}
TEST_F(BrkTest, BrkWithScope) {
    ASSERT_EQ(brk->brk("http-request", "false", "myscope"), "dummy");
}
TEST_F(BrkTest, SetHttpMessageHeaderOnly) {
    ASSERT_EQ(brk->set_http_message("header"), "dummy");
}
TEST_F(BrkTest, SetHttpMessageHeaderAndBody) {
    ASSERT_EQ(brk->set_http_message("header", "body"), "dummy");
}
TEST_F(BrkTest, Cont) {
    ASSERT_EQ(brk->cont(), "dummy");
}
TEST_F(BrkTest, Step) {
    ASSERT_EQ(brk->step(), "dummy");
}
TEST_F(BrkTest, Drop) {
    ASSERT_EQ(brk->drop(), "dummy");
}
TEST_F(BrkTest, AddHttpBreakpoint) {
    ASSERT_EQ(brk->add_http_breakpoint("string", "url", "contains", false, false), "dummy");
}
TEST_F(BrkTest, RemoveHttpBreakpoint) {
    ASSERT_EQ(brk->remove_http_breakpoint("string", "url", "contains", false, false), "dummy");
}