#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "overholt/tasks.h"

class OutputCapture {
public:
    OutputCapture() {
        old_buf = std::cout.rdbuf();
        std::cout.rdbuf(stream.rdbuf());
    }
    ~OutputCapture() {
        std::cout.rdbuf(old_buf);
    }
    std::string get() { return stream.str(); }
private:
    std::ostringstream stream;
    std::streambuf* old_buf = nullptr;
};

TEST(TasksTest, SendManagerAddedEmailPrints) {
    OutputCapture cap;
    Overholt::Tasks::send_manager_added_email("user1@example.com", "user2@example.com");
    std::string output = cap.get();
    EXPECT_NE(output.find("sending manager added email"), std::string::npos);
}

TEST(TasksTest, SendManagerRemovedEmailPrints) {
    OutputCapture cap;
    Overholt::Tasks::send_manager_removed_email("user3@example.com");
    std::string output = cap.get();
    EXPECT_NE(output.find("sending manager removed email"), std::string::npos);
}