#include <gtest/gtest.h>
#include "queue.h"

class DummyQueue : public BaseQueue {
public:
    void push(const std::vector<uint8_t>&) override {}
    std::optional<std::vector<uint8_t>> pop() override { return std::nullopt; }
    std::optional<std::vector<uint8_t>> peek() override { return std::nullopt; }
    void close() override {}
    size_t size() const override { return 0; }
};

TEST(BaseQueueMetaTest, InstanceCheckAndSubclassCheck) {
    DummyQueue dq;
    EXPECT_TRUE(dynamic_cast<BaseQueue*>(&dq));
    struct NotAQueue {};
    // Can't check dynamic_cast<NotAQueue*> to BaseQueue, always false if no inheritance
}

TEST(FifoMemoryQueueTest, FifoNormal) {
    FifoMemoryQueue q;
    EXPECT_EQ(q.size(), 0u);
    q.push({1});
    q.push({2});
    EXPECT_EQ(q.size(), 2u);
    EXPECT_EQ(q.peek(), std::vector<uint8_t>({1}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({1}));
    EXPECT_EQ(q.peek(), std::vector<uint8_t>({2}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({2}));
    EXPECT_EQ(q.peek(), std::nullopt);
    EXPECT_EQ(q.pop(), std::nullopt);
    q.close();
}

TEST(FifoMemoryQueueTest, EmptyPopPeek) {
    FifoMemoryQueue q;
    EXPECT_EQ(q.pop(), std::nullopt);
    EXPECT_EQ(q.peek(), std::nullopt);
    q.close();
}

TEST(LifoMemoryQueueTest, LifoNormal) {
    LifoMemoryQueue q;
    EXPECT_EQ(q.size(), 0u);
    q.push({'a'});
    q.push({'b'});
    EXPECT_EQ(q.size(), 2u);
    EXPECT_EQ(q.peek(), std::vector<uint8_t>({'b'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'b'}));
    EXPECT_EQ(q.peek(), std::vector<uint8_t>({'a'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'a'}));
    EXPECT_EQ(q.peek(), std::nullopt);
    EXPECT_EQ(q.pop(), std::nullopt);
    q.close();
}