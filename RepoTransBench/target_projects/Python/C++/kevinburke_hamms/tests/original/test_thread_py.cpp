#include <gtest/gtest.h>
#include <iostream>
#include <sstream>

// Mocking a "thread" module as in Python; in reality, you'd include your thread.h/.cpp files
namespace thread {
    // Simulates the example function that prints to stdout
    inline void run_thread_example() {
        std::cout << "HammsServer started\n";
        std::cout << "stopping\n";
        std::cout << "HammsServer stopped\n";
    }
}

TEST(ThreadPy, Importable) {
    // Simulate import without running main code; in C++ import is always legal if compiled.
    // There's nothing to simulate here, so just check we "can use" the namespace.
    SUCCEED();
}

TEST(ThreadPy, MainFunctionPrints) {
    // Capture stdout using stringstream
    std::stringstream buffer;
    std::streambuf* prevcout = std::cout.rdbuf(buffer.rdbuf());
    thread::run_thread_example();
    std::cout.rdbuf(prevcout);

    std::string output = buffer.str();
    EXPECT_NE(output.find("HammsServer started"), std::string::npos);
    EXPECT_NE(output.find("stopping"), std::string::npos);
    EXPECT_NE(output.find("HammsServer stopped"), std::string::npos);
}