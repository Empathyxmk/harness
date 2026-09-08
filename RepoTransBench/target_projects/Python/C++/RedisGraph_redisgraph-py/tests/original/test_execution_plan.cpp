#include <gtest/gtest.h>
#include "execution_plan.h"
#include <stdexcept>
#include <memory>
#include <vector>
#include <string>

using namespace redisgraph;

TEST(ProfileStatsTest, Fields) {
    ProfileStats ps(10, 1.23);
    EXPECT_EQ(ps.records_produced, 10);
    EXPECT_DOUBLE_EQ(ps.execution_time, 1.23);
}

TEST(OperationTest, EqAndStr) {
    Operation op1("Filter");
    Operation op2("Filter");
    Operation op3("Scan");
    Operation op4("Filter", "x > 1");

    EXPECT_EQ(op1, op2);
    EXPECT_FALSE(op1 == op3);
    EXPECT_FALSE(op1 == op4);
    EXPECT_EQ(op1.toString(), "Filter");
    EXPECT_EQ(op4.toString(), "Filter | x > 1");
}

TEST(OperationTest, AppendAndChildCount) {
    Operation op("Root");
    Operation* child = new Operation("Child");
    op.append_child(child);
    EXPECT_EQ(op.child_count(), 1);
    EXPECT_EQ(op.children[0], child);

    EXPECT_THROW(op.append_child(&op), std::runtime_error);
    EXPECT_THROW(op.append_child(nullptr), std::runtime_error);
    delete child;
}

class DummyEP : public ExecutionPlan {
public:
    DummyEP() : ExecutionPlan(std::vector<std::string>{}) {}
protected:
    Operation* _operation_tree() override {
        Operation* op1 = new Operation("Root");
        Operation* op2 = new Operation("Child");
        op1->append_child(op2);
        return op1;
    }
};

class OtherEP : public ExecutionPlan {
public:
    OtherEP() : ExecutionPlan(std::vector<std::string>{}) {}
protected:
    Operation* _operation_tree() override {
        return new Operation("DifferentRoot");
    }
};

TEST(ExecutionPlanTest, EqAndStrPatchTree) {
    DummyEP ep1;
    DummyEP ep2;
    EXPECT_EQ(ep1, ep2);
    std::string s = ep1.toString();
    EXPECT_FALSE(s.empty());

    OtherEP ep3;
    EXPECT_FALSE(ep1 == ep3);
}

TEST(ExecutionPlanTest, InvalidInit) {
    EXPECT_THROW(ExecutionPlan("notalist"), std::invalid_argument);
}

class DummyEPManualTree : public ExecutionPlan {
public:
    DummyEPManualTree() : ExecutionPlan(std::vector<std::string>{}) {}
protected:
    Operation* _operation_tree() override {
        Operation* op = new Operation("A");
        Operation* opB = new Operation("B");
        Operation* opC = new Operation("C");
        op->append_child(opB);
        op->append_child(opC);
        return op;
    }
};

TEST(ExecutionPlanTest, OperationTraverseManualTree) {
    DummyEPManualTree ep;
    auto traverse = ep._operation_traverse(ep.structured_plan,
        [](Operation* x) { return x->name; },
        [](const std::vector<std::string>& c) {
            std::string r;
            for (size_t i = 0; i < c.size(); ++i) {
                r += c[i];
                if (i + 1 < c.size()) r += ",";
            }
            return r;
        },
        [](const std::string& x, const std::string& y) { return x + ">" + y; }
    );
    EXPECT_EQ(traverse, "A>B,C");
}

TEST(ExecutionPlanTest, OperationTreeSimple) {
    std::vector<std::pair<std::vector<std::string>, std::string>> params = {
        { {"Project","    Filter  (predicate: (n.v > 1))", "        NodeByLabelScan | (n:V)"}, "Project" },
        { {"Filter", "    NodeByLabelScan | (n:V)"}, "Filter" }
    };

    for (const auto& param : params) {
        ExecutionPlan ep(param.first);
        ASSERT_TRUE(dynamic_cast<Operation*>(ep.structured_plan));
        EXPECT_EQ(ep.structured_plan->name, param.second);
    }
}