#include <gtest/gtest.h>
#include "gigachat/Settings.h"

TEST(PublicSettingsTest, InstantiationHasClass) {
    gigachat::Settings instance;
    // C++ always has type info, simulate python hasattr
    SUCCEED();
}