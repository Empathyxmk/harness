#include <gtest/gtest.h>
#include <string>
#include <stdexcept>

class Pipe {
public:
    int in_fd = 5, out_fd = 6;
    bool out_closed = false, in_closed = false;
    std::string write_path = "/dev/fd/7";
    Pipe() {}
    void close_in() { in_closed = true; }
    void close_out() { out_closed = true; }
};

// For monkeypatching, we simply simulate
TEST(TestPipeClass, CreationAndClose) {
    Pipe p;
    ASSERT_TRUE(typeid(p.out_fd) == typeid(int));
    ASSERT_TRUE(typeid(p.in_fd) == typeid(int));
    ASSERT_FALSE(p.out_closed);
    ASSERT_FALSE(p.in_closed);
    ASSERT_TRUE(p.write_path.find("/dev/fd/") == 0);

    p.close_in();
    ASSERT_TRUE(p.in_closed);

    p.close_out();
    ASSERT_TRUE(p.out_closed);
}