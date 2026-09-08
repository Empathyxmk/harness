#include <gtest/gtest.h>
#include "pqueue.h"
#include "queue.h"

class DummyFifoFactory {
public:
    BaseQueue* operator()(int prio) { return new FifoMemoryQueue(); }
};
class DummyLifoFactory {
public:
    BaseQueue* operator()(int prio) { return new LifoMemoryQueue(); }
};

TEST(FifoMemoryPriorityQueueTest, PushPopPrio) {
    PriorityQueue q(DummyFifoFactory());
    q.push({'a'}, 3);
    q.push({'b'}, 1);
    q.push({'c'}, 2);
    q.push({'d'}, 1);

    // Should pop in order of prio 1,1,2,3: b,d,c,a
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'b'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'d'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'c'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'a'}));
    EXPECT_EQ(q.pop(), std::nullopt);
}

TEST(LifoMemoryPriorityQueueTest, PushPopPrio) {
    PriorityQueue q(DummyLifoFactory());
    q.push({'a'}, 3);
    q.push({'b'}, 1);
    q.push({'c'}, 2);
    q.push({'d'}, 1);
    // Should pop 1,1,2,3: d,b,c,a for LIFO
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'d'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'b'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'c'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'a'}));
    EXPECT_EQ(q.pop(), std::nullopt);
}