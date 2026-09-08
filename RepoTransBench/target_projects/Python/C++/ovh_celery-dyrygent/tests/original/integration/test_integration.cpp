#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include <set>
#include <memory>
#include <regex>
#include "ovh_celery_dyrygent/workflow.h"
#include "ovh_celery_dyrygent/tasks.h"
#include "ovh_celery_dyrygent/entities.h"
#include "app_api.h" // Assume this header exists for test stubs for order_task, read_logs, return_value_task

using namespace ovh_celery_dyrygent;
// The following "API" functions & classes are representative; real versions would come from the implementation/environment.

namespace {

std::map<std::string, std::vector<std::string>> parse_logs(const std::string& logs) {
    std::map<std::string, std::vector<std::string>> grouped_logs;
    std::regex task_regex(R"(app\.(?:order|return_value)_task\[([\w-]+)\]: Test name: ([\w-]+) Test value: ([\w-]+))");
    std::stringstream ss(logs);
    std::string line;
    while (std::getline(ss, line)) {
        std::smatch findings;
        if (std::regex_search(line, findings, task_regex)) {
            // findings[2] = test_name, findings[3] = test_value
            std::string test_name = findings[2];
            std::string test_value = findings[3];
            grouped_logs[test_name].push_back(test_value);
        }
    }
    return grouped_logs;
}

std::string uuid4() {
    // For the test; would use real UUID generation
    static int cnt = 0;
    return "UUID-" + std::to_string(++cnt);
}

}

TEST(TestCeleryDyrygentIntegration, test_return_value) {
    std::string test_name = uuid4();

    auto canvas = return_value_task::s(test_name);

    Workflow workflow;
    workflow.add_celery_canvas(canvas);
    auto result = workflow.apply_async();
    result.wait();

    std::string task_id = workflow.nodes.begin()->first;
    auto logs_result = read_logs::delay();
    std::string log_content = logs_result.get();
    auto results = parse_logs(log_content)[test_name];

    ASSERT_EQ(task_id, results[0]);
}

class TestCeleryDyrygentOrder : public ::testing::Test {
protected:
    std::string test_name;
    void SetUp() override {
        test_name = uuid4();
    }

    std::map<std::string, std::vector<std::string>> get_canvas_order(const Canvas& canvas) {
        Workflow workflow;
        workflow.add_celery_canvas(canvas);
        auto result = workflow.apply_async();
        result.wait();
        auto logs_result = read_logs::delay();
        std::string log_content = logs_result.get();
        return parse_logs(log_content);
    }
};

TEST_F(TestCeleryDyrygentOrder, test_single_task) {
    auto canvas = order_task::s(test_name, "task1");
    auto res = get_canvas_order(canvas);
    ASSERT_EQ(res[test_name], std::vector<std::string>({"task1"}));
}

TEST_F(TestCeleryDyrygentOrder, test_group) {
    std::vector<Canvas> group_members;
    for (int i = 1; i <= 5; ++i) {
        group_members.push_back(order_task::s(test_name, "task" + std::to_string(i)));
    }
    auto canvas = celery_group(group_members);
    auto orders = get_canvas_order(canvas)[test_name];
    std::set<std::string> order_set(orders.begin(), orders.end());
    std::set<std::string> expected_set{"task1","task2","task3","task4","task5"};
    ASSERT_EQ(order_set, expected_set);
}

TEST_F(TestCeleryDyrygentOrder, test_chord) {
    std::vector<Canvas> header;
    for (int i = 1; i <= 5; ++i) {
        header.push_back(order_task::s(test_name, "task" + std::to_string(i)));
    }
    auto body = order_task::s(test_name, "last");
    auto canvas = celery_chord(header, body);
    auto orders = get_canvas_order(canvas)[test_name];
    ASSERT_EQ(orders.back(), "last");
}

TEST_F(TestCeleryDyrygentOrder, test_chain) {
    std::vector<Canvas> chain_tasks{
        order_task::s(test_name, "task1"),
        order_task::s(test_name, "task2"),
        order_task::s(test_name, "task3")
    };
    auto canvas = celery_chain(chain_tasks);
    auto orders = get_canvas_order(canvas)[test_name];
    ASSERT_EQ(orders, (std::vector<std::string>{"task1","task2","task3"}));
}

TEST_F(TestCeleryDyrygentOrder, test_combination) {
    auto g1 = celery_group({order_task::s(test_name, "task1a"), order_task::s(test_name, "task1b")});
    auto t2 = order_task::s(test_name, "task2");
    auto t3 = order_task::s(test_name, "task3");
    auto g2 = celery_group({order_task::s(test_name, "task4a"), order_task::s(test_name, "task4b")});
    auto t5 = order_task::s(test_name, "task5");
    auto canvas = g1 | t2 | t3 | g2 | t5;

    auto order = get_canvas_order(canvas)[test_name];

    std::set<std::string> expected_g1 = {"task1a", "task1b"};
    std::set<std::string> g1_actual(order.begin(), order.begin()+2);
    ASSERT_EQ(g1_actual, expected_g1);
    ASSERT_EQ(std::vector<std::string>(order.begin()+2, order.begin()+4), (std::vector<std::string>{"task2","task3"}));
    std::set<std::string> expected_g2 = {"task4a", "task4b"};
    std::set<std::string> g2_actual(order.begin()+4, order.begin()+6);
    ASSERT_EQ(g2_actual, expected_g2);
    ASSERT_EQ(order[6], "task5");
}