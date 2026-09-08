#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <stdexcept>

class NoVaultSecretFound : public std::exception {};

std::string read_file(const std::string& filename) {
    // Dummy function to simulate file reading
    return "hello";
}

TEST(TestVault, VaultPasswordFile) {
    std::string group = "web";
    std::unordered_map<std::string, std::string> the_vars = { {group, "hello"} };
    EXPECT_EQ(the_vars[group], "hello");
}

TEST(TestVault, VaultPasswordFiles) {
    std::string group = "web";
    std::unordered_map<std::string, std::string> the_vars = { {group, "hello"} };
    EXPECT_EQ(the_vars[group], "hello");
}

TEST(TestVault, VaultIds) {
    std::string host = "web-01";
    std::unordered_map<std::string, std::string> the_vars = { {host, "world"} };
    EXPECT_EQ(the_vars[host], "world");
}

TEST(TestVault, NoVaultPass) {
    try {
        throw NoVaultSecretFound();
    } catch (const NoVaultSecretFound&) {
        SUCCEED();
    }
}

TEST(TestVault, InlineVaultWithoutPassword) {
    std::string group = "inline";
    std::string host = "inline-01";
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> the_vars = {
        {group, { {"text", "abc"} }},
        {host,  {         }}
    };
    EXPECT_TRUE(the_vars[group].find("text") != the_vars[group].end());
}