#include <gtest/gtest.h>
#include "queue.h"

class AnotherDummyQueue : public BaseQueue {
public:
    void push(const std::vector<uint8_t>&) override {}
    std::optional<std::vector<uint8_t>> pop() override { return std::nullopt; }
    std::optional<std::vector<uint8_t>> peek() override { return std::nullopt; }
    void close() override {}
    size_t size() const override { return 0; }
};

TEST(TestBaseQueueMetaPublic, InstanceAndSubclass) {
    AnotherDummyQueue dq;
    EXPECT_TRUE(dynamic_cast<BaseQueue*>(&dq));
    struct NonQueue {};
    // Can't cast a NonQueue* to BaseQueue*, check always false.
}

TEST(TestFifoMemoryQueuePublic, FifoAlternate) {
    FifoMemoryQueue q;
    EXPECT_EQ(q.size(), 0u);
    q.push({100});
    q.push({200});
    q.push({300});
    EXPECT_EQ(q.size(), 3u);
    EXPECT_EQ(q.peek(), std::vector<uint8_t>({100}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({100}));
    EXPECT_EQ(q.peek(), std::vector<uint8_t>({200}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({200}));
    EXPECT_EQ(q.peek(), std::vector<uint8_t>({300}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({300}));
    EXPECT_EQ(q.peek(), std::nullopt);
    EXPECT_EQ(q.pop(), std::nullopt);
    q.close();
}

TEST(TestFifoMemoryQueuePublic, EmptyBehaviour) {
    FifoMemoryQueue q;
    EXPECT_EQ(q.peek(), std::nullopt);
    EXPECT_EQ(q.pop(), std::nullopt);
    q.close();
}

TEST(TestLifoMemoryQueuePublic, LifoAlternate) {
    LifoMemoryQueue q;
    EXPECT_EQ(q.size(), 0u);
    q.push({'x'});
    q.push({'y'});
    q.push({'z'});
    EXPECT_EQ(q.size(), 3u);
    EXPECT_EQ(q.peek(), std::vector<uint8_t>({'z'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'z'}));
    EXPECT_EQ(q.peek(), std::vector<uint8_t>({'y'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'y'}));
    EXPECT_EQ(q.peek(), std::vector<uint8_t>({'x'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'x'}));
    EXPECT_EQ(q.peek(), std::nullopt);
    EXPECT_EQ(q.pop(), std::nullopt);
    q.close();
}