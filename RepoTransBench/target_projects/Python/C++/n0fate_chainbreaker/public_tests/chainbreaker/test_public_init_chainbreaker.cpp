#include <gtest/gtest.h>
#include <string>

namespace chainbreaker {
    const std::string __version__ = "1.0.0";
    const char *__doc__ = "Some doc";
    const char *__name__ = "chainbreaker";
}

TEST(PublicInitChainbreakerTest, PublicImportChainbreaker) {
    ASSERT_TRUE(!chainbreaker::__version__.empty() || (chainbreaker::__doc__ != nullptr));
}

TEST(PublicInitChainbreakerTest, PublicChainbreakerModuleContent) {
    ASSERT_TRUE(chainbreaker::__doc__ != nullptr);
    ASSERT_TRUE(chainbreaker::__name__ != nullptr);
}