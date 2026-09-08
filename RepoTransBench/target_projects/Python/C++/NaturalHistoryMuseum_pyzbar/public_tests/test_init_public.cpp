#include <gtest/gtest.h>
#include "pyzbar/pyzbar.h"

TEST(InitPublic, Init) {
    // Check for non-empty doc and version attribute
    EXPECT_FALSE(get_pyzbar_doc().empty());
    EXPECT_FALSE(get_pyzbar_version().empty());
}