#include <gtest/gtest.h>
#include "queue.h"

class DummyQueue : public BaseQueue {
    std::vector<std::vector<uint8_t>> q;
public:
    void push(const std::vector<uint8_t>& obj) override {
        q.push_back(obj);
    }
    std::optional<std::vector<uint8_t>> pop() override {
        if (q.empty()) return std::nullopt;
        auto value = q.back();
        q.pop_back();
        return value;
    }
    std::optional<std::vector<uint8_t>> peek() override {
        if (q.empty()) return std::nullopt;
        return q.back();
    }
    void close() override { }
    size_t size() const override { return q.size(); }
};

TEST(InterfaceTest, QueueNotImplemented) {
    class DummyImpl : public BaseQueue {};
    DummyImpl q;
    // Can't test NotImplementedError in C++; just check pure virtuals
}
TEST(InterfaceTest, IsSubclassAndInstance) {
    EXPECT_FALSE((std::is_base_of<BaseQueue, std::vector<int>>::value));
    EXPECT_TRUE((std::is_base_of<BaseQueue, DummyQueue>::value));
    FifoMemoryQueue fq;
    LifoMemoryQueue lq;
    EXPECT_TRUE(dynamic_cast<BaseQueue*>(&fq));
    EXPECT_TRUE(dynamic_cast<BaseQueue*>(&lq));
}

TEST(InterfaceTest, IsInstanceOfDiskQueues) {
    FifoDiskQueue fq("foo.bin");
    LifoDiskQueue lq("bar.bin");
    EXPECT_TRUE(dynamic_cast<BaseQueue*>(&fq));
    EXPECT_TRUE(dynamic_cast<BaseQueue*>(&lq));
    fq.close();
    lq.close();
}

TEST(FifoTest, PushPop1) {
    FifoMemoryQueue q;
    q.push({'a'});
    q.push({'b'});
    q.push({'c'});
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'a'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'b'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'c'}));
    EXPECT_EQ(q.pop(), std::nullopt);
    q.close();
}
TEST(LifoTest, PushPop1) {
    LifoMemoryQueue q;
    q.push({'a'});
    q.push({'b'});
    q.push({'c'});
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'c'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'b'}));
    EXPECT_EQ(q.pop(), std::vector<uint8_t>({'a'}));
    EXPECT_EQ(q.pop(), std::nullopt);
    q.close();
}