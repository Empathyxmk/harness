#include "gtest/gtest.h"
#include "lib/mountain.h"
#include "lib/mock.h"

TEST(TestMountain, ItGetsTestResults) {
    Mountain mountain;
    auto& stream = mountain.getStream();
    auto& lesson = mountain.getLesson();
    auto mockWriteln = [] (const std::string&) {};
    stream.setWritelnFn(mockWriteln);
    bool learnCalled = false;
    lesson.setLearnFn([&](){ learnCalled = true; });
    mountain.walk_the_path();
    EXPECT_TRUE(learnCalled);
}