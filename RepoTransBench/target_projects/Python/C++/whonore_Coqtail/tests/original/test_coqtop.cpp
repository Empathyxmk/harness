#include <gtest/gtest.h>
#include <string>

// Simulate "reset" state test
class Coqtop {
public:
    bool running = false;

    void start() { running = true; }
    void stop() { running = false; }
    bool is_running() const { return running; }
};

TEST(CoqtopTest, BasicStartStop) {
    Coqtop ct;
    ASSERT_FALSE(ct.is_running());
    ct.start();
    ASSERT_TRUE(ct.is_running());
    ct.stop();
    ASSERT_FALSE(ct.is_running());
}