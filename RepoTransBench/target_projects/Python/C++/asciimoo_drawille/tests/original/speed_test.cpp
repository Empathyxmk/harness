#include <gtest/gtest.h>
#include <chrono>
#include <iostream>
#include <string>
#include "drawille.h"

TEST(SpeedTest, FrameTimes) {
    Canvas c;
    int frames = 10000;
    std::vector<std::pair<int, int>> sizes = {
        {0, 0}, {10, 10}, {20, 20}, {20, 40},
        {40, 20}, {40, 40}, {100, 100}
    };
    for (auto sz : sizes) {
        int x = sz.first, y = sz.second;
        c.set(0, 0);
        for (int i = 0; i < y; ++i) c.set(x, i);

        auto t1 = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < frames; ++i) {
            c.frame();
        }
        auto t2 = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> sec = t2 - t1;
        std::cout << x << "x" << y << "\t" << sec.count() << std::endl;
        c.clear();
    }
}