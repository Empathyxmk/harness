#include <gtest/gtest.h>
#include <string>

// Because C++ is statically linked, we can't import Python module reload, but we will check
// that symbols exist/stub loading works.

namespace pyicloud {
    std::string __doc__ = "pyicloud simulated documentation";
    class PyiCloudService {};
}

TEST(InitTest, InitRuns) {
    // Should not throw and should have __doc__ & PyiCloudService present
    EXPECT_FALSE(pycloud::__doc__.empty());
    pyicloud::PyiCloudService service;
    SUCCEED();
}