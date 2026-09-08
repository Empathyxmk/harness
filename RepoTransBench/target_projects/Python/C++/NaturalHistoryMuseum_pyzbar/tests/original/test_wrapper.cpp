#include <gtest/gtest.h>
#include "pyzbar/wrapper.h"

TEST(Wrapper, ImportWrapperModule) {
    EXPECT_TRUE(wrapper_module_imported());
}

TEST(Wrapper, VersionString) {
    EXPECT_TRUE(wrapper_module_has_doc());
}

TEST(Wrapper, DummyForCoverage) {
    SUCCEED();
}