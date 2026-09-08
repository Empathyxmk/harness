#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "overholt/tasks.h"

class OutputCapturePublic {
public:
    OutputCapturePublic() {
        old_buf = std::cout.rdbuf();
        std::cout.rdbuf(stream.rdbuf());
    }
    ~OutputCapturePublic() {
        std::cout.rdbuf(old_buf);
    }
    std::string get() { return stream.str(); }
private:
    std::ostringstream stream;
    std::streambuf* old_buf = nullptr;
};

TEST(PublicTasksTest, SendManagerAddedEmailContent) {
    OutputCapturePublic cap;
    Overholt::Tasks::send_manager_added_email("public1@example.com", "public2@example.com");
    std::string output = cap.get();
    EXPECT_NE(output.find("manager added email"), std::string::npos);
}

TEST(PublicTasksTest, SendManagerRemovedEmailContent) {
    OutputCapturePublic cap;
    Overholt::Tasks::send_manager_removed_email("public3@example.com");
    std::string output = cap.get();
    EXPECT_NE(output.find("manager removed email"), std::string::npos);
}