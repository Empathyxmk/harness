#include <gtest/gtest.h>
#include "rrqueue.h"
#include "queue.h"

class DummyFifoFactory {
public:
    BaseQueue* operator()(const std::string&) { return new FifoMemoryQueue(); }
};
class DummyLifoFactory {
public:
    BaseQueue* operator()(const std::string&) { return new LifoMemoryQueue(); }
};

TEST(RRQueueFifoMemoryTest, PushPopKey) {
    RoundRobinQueue q(DummyFifoFactory());
    q.push({'a'}, "1");
    q.push({'b'}, "1");
    q.push({'c'}, "2");
    q.push({'d'}, "2");
    // Should pop: a, c, b, d
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'a'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'c'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'b'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'d'}));
    EXPECT_EQ(q.pop(), std::nullopt);
}

TEST(RRQueueLifoMemoryTest, PushPopKey) {
    RoundRobinQueue q(DummyLifoFactory());
    q.push({'a'}, "1");
    q.push({'b'}, "1");
    q.push({'c'}, "2");
    q.push({'d'}, "2");
    // Should pop: b, d, a, c
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'b'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'d'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'a'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'c'}));
    EXPECT_EQ(q.pop(), std::nullopt);
}