#include <gtest/gtest.h>
#include "queue.h"

TEST(TestFifoDiskQueuePublic, FifoDiskAlternate) {
    FifoDiskQueue q("test_fifo_disk_public");
    q.push({'w'});
    q.push({'x'});
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'w'}));
    q.push({'y'});
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'x'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'y'}));
    EXPECT_EQ(q.pop(), std::nullopt);
    q.close();
}

TEST(TestLifoDiskQueuePublic, LifoDiskDifferent) {
    LifoDiskQueue q("test_lifo_disk_public");
    q.push({'x'});
    q.push({'y'});
    q.push({'z'});
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'z'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'y'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'x'}));
    EXPECT_EQ(q.pop(), std::nullopt);
    q.close();
}
// SQLite queues are not available in C++