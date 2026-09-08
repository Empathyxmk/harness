#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

class CoqtopPyPublic {
public:
    std::string version() const { return "8.13.2"; }
};

TEST(PublicCoqtopPyTest, PublicVersion) {
    CoqtopPyPublic coqtop;
    EXPECT_EQ(coqtop.version(), "8.13.2");
}