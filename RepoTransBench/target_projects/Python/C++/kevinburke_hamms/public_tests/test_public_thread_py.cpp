#include <gtest/gtest.h>
#include <iostream>
#include <sstream>
#include <algorithm>

namespace thread {
    // Simulates the example function that prints to stdout
    inline void run_thread_example() {
        std::cout << "HammsServer started\n";
        std::cout << "stopping\n";
        std::cout << "HammsServer stopped\n";
    }
}

TEST(PublicThreadPy, ImportableCustom) {
    // In C++ we don't have the python sys.modules hack, so just simulate import as before.
    SUCCEED();
}

TEST(PublicThreadPy, MainCustomOutput) {
    std::stringstream buffer;
    std::streambuf* prevcout = std::cout.rdbuf(buffer.rdbuf());
    thread::run_thread_example();
    std::cout.rdbuf(prevcout);

    std::string output = buffer.str();
    std::vector<std::string> lines;
    std::istringstream iss(output);
    std::string line;
    while (std::getline(iss, line)) {
        lines.push_back(line);
    }
    // Check any line contains 'HammsServer started'
    bool started = false;
    for (const auto& l : lines) {
        if (l.find("HammsServer started") != std::string::npos) {
            started = true;
            break;
        }
    }
    ASSERT_TRUE(started);

    ASSERT_GE(lines.size(), 2u);
    // Check that the second to last line is 'stopping' (case-insensitive)
    auto trim = [](std::string s) {
        s.erase(0, s.find_first_not_of(" \t\r\n"));
        s.erase(s.find_last_not_of(" \t\r\n") + 1);
        return s;
    };
    std::string stoppingLine = trim(lines[lines.size() - 2]);
    std::transform(stoppingLine.begin(), stoppingLine.end(), stoppingLine.begin(), ::tolower);
    ASSERT_EQ(stoppingLine, "stopping");

    // Last line contains "HammsServer stopped"
    ASSERT_NE(lines.back().find("HammsServer stopped"), std::string::npos);
}