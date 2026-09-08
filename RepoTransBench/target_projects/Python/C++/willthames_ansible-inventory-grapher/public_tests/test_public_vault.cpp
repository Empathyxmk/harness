#include <gtest/gtest.h>
#include <string>
#include <fstream>
#include <filesystem>

using namespace std;

TEST(TestPublicVault, PublicFakeVaultFile) {
    namespace fs = std::filesystem;
    fs::path vault_file = fs::temp_directory_path() / "public_vaultfile";
    ofstream fout(vault_file);
    fout << "$ANSIBLE_VAULT;1.1;AES256\ntestpublic";
    fout.close();
    ASSERT_TRUE(fs::exists(vault_file));
    ifstream fin(vault_file);
    std::string content((std::istreambuf_iterator<char>(fin)), std::istreambuf_iterator<char>());
    fin.close();
    EXPECT_NE(content.find("$ANSIBLE_VAULT"), std::string::npos);
    EXPECT_NE(content.find("public"), std::string::npos);
    fs::remove(vault_file);
}

TEST(TestPublicVault, PublicVaultPassword) {
    namespace fs = std::filesystem;
    fs::path pw_file = fs::temp_directory_path() / "public_vaultpass";
    std::string vault_password = "superpublicpw";
    ofstream fout(pw_file);
    fout << vault_password;
    fout.close();
    ifstream fin(pw_file);
    std::string contents;
    fin >> contents;
    fin.close();
    EXPECT_EQ(contents, vault_password);
    fs::remove(pw_file);
}

TEST(TestPublicVault, PublicMultipleVaultFiles) {
    namespace fs = std::filesystem;
    std::vector<std::string> vault_contents = {
        "$ANSIBLE_VAULT;1.2;AES256\npublicvaultcipher",
        "$ANSIBLE_VAULT;1.2;AES256\nanotherpubliccipher"
    };
    for (auto& vault_content : vault_contents) {
        fs::path vault_file = fs::temp_directory_path() / "vault_varied.public";
        ofstream fout(vault_file);
        fout << vault_content;
        fout.close();
        ifstream fin(vault_file);
        std::string content((std::istreambuf_iterator<char>(fin)), std::istreambuf_iterator<char>());
        fin.close();
        EXPECT_NE(content.find("AES256"), std::string::npos);
        fs::remove(vault_file);
    }
}