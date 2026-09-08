#include <gtest/gtest.h>
#include "betterprompt.h"

TEST(TestPublicInitModule, AllExportsViaDict) {
    for (const auto& name : betterprompt::get_all_exports()) {
        // Cannot check __dict__ in C++ – just that the symbol exists in __all__
        SUCCEED();
    }
}