#include <gtest/gtest.h>
#include "records.hpp"

// Mimic the python @pytest.mark.usefixtures("foo_table")
class FooTableTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Would set up "foo" table (skipped implementation)
    }
    void TearDown() override {
        // Would tear down "foo" table (skipped implementation)
    }
};

TEST_F(FooTableTest, TestIssue105) {
    records::Database db("sqlite:///:memory:");
    auto result = db.query("select count(*) as n from foo");
    EXPECT_EQ(result.scalar(), 0);
}