#include <gtest/gtest.h>
#include <cstdlib>

// Simulated public version of is_flatpak logic
bool public_is_flatpak() {
    const char* flatpak_id = std::getenv("FLATPAK_ID");
    const char* steam_flatpak_prime = std::getenv("STEAM_FLATPAK_PRIME");
    const char* protontricks_flatpak = std::getenv("PROTONTRICKS_FLATPAK");
    return (flatpak_id != nullptr)
        || (steam_flatpak_prime != nullptr)
        || (protontricks_flatpak != nullptr && std::string(protontricks_flatpak) == "1");
}

TEST(PublicFlatpakTest, PublicIsFlatpak_EnvFlatpakId) {
    setenv("FLATPAK_ID", "foo.bar.publicprotontricks", 1);
    ASSERT_TRUE(public_is_flatpak());
    unsetenv("FLATPAK_ID");
}

TEST(PublicFlatpakTest, PublicIsFlatpak_EnvSteamFlatpakPrime) {
    unsetenv("FLATPAK_ID");
    setenv("STEAM_FLATPAK_PRIME", "1", 1);
    ASSERT_TRUE(public_is_flatpak());
    unsetenv("STEAM_FLATPAK_PRIME");
}

TEST(PublicFlatpakTest, PublicNotFlatpak_Default) {
    unsetenv("FLATPAK_ID");
    unsetenv("STEAM_FLATPAK_PRIME");
    setenv("PROTONTRICKS_FLATPAK", "0", 1);
    ASSERT_FALSE(public_is_flatpak());
    unsetenv("PROTONTRICKS_FLATPAK");
}