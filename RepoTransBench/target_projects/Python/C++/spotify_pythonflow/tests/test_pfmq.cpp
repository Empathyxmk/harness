#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "pythonflow/pfmq.h"
#include "pythonflow/core.h"
#include "pythonflow/operations.h"
#include "pythonflow/util.h"

using namespace std::chrono_literals;

std::string backend_address() {
    // Generate unique inproc address, e.g., "inproc://{uuid}"
    return "inproc://" + pythonflow::random_uuid();
}

class BrokerFixture : public ::testing::Test {
protected:
    std::unique_ptr<pythonflow::pfmq::Broker> broker;
    virtual void SetUp() override {
        broker = std::make_unique<pythonflow::pfmq::Broker>(backend_address());
        broker->runAsync();
    }
    virtual void TearDown() override {
        broker->cancel();
    }
};

TEST_F(BrokerFixture, WorkersRunning) {
    std::vector<std::unique_ptr<pythonflow::pfmq::Worker>> workers;
    auto graph = pythonflow::build_worker_graph();
    for (int i = 0; i < 10; ++i) {
        auto w = std::make_unique<pythonflow::pfmq::Worker>(*graph, broker->backendAddress());
        w->runAsync();
        workers.push_back(std::move(w));
    }
    std::this_thread::sleep_for(1s);
    for (auto& worker : workers) {
        ASSERT_TRUE(worker->isAlive());
    }
    for (auto& worker : workers) {
        worker->cancel();
    }
}

// ... (Repeat for all the test logic, covering Broker/Broker error handling, batch apply, timeouts etc)