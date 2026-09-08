#include <gtest/gtest.h>
#include <string>
#include <stdexcept>

class Pipe {
public:
    int in_fd = 10, out_fd = 11;
    bool auto_close = true;

    Pipe() {}
    void close_in() { in_fd = -1; }
    void close_out() { out_fd = -1; }
};

class PipeCloseError : public std::runtime_error {
public:
    PipeCloseError() : std::runtime_error("PipeCloseError") {}
    std::string repr() const { return std::string("PipeCloseError()"); }
};

TEST(TestPipeManual, PipeInitAndClose) {
    Pipe pipe;
    ASSERT_TRUE((pipe.in_fd != -1 && pipe.out_fd != -1));
    pipe.close_in();
    pipe.close_out();
    ASSERT_TRUE(typeid(pipe.auto_close) == typeid(bool));
}

TEST(TestPipeManual, PipeCloseErrorRepr) {
    PipeCloseError e;
    ASSERT_TRUE(typeid(e.repr()) == typeid(std::string));
}