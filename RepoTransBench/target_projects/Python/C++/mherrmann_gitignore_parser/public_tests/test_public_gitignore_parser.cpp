#include <gtest/gtest.h>
#include <filesystem>
#include <fstream>
#include <cstdio>
#include "gitignore_parser.h"

using namespace gitignore;
namespace fs = std::filesystem;

TEST(TestPublic, Simple) {
    auto matches = parse_gitignore_str(
        "build/\n"
        "*.log", "/example"
    );
    EXPECT_FALSE(matches("/example/main.txt"));
    EXPECT_TRUE(matches("/example/main.log"));
    EXPECT_TRUE(matches("/example/dir/main.log"));
    EXPECT_TRUE(matches("/example/build"));
}

TEST(TestPublic, SimpleParseFile) {
    std::string fname = "/tmp/public_gitignore1";
    std::ofstream out(fname);
    out << "dist/\n*.tmp";
    out.close();

    auto matches = parse_gitignore(fname);
    EXPECT_FALSE(matches("/project/app.py"));
    EXPECT_TRUE(matches("/project/app.tmp"));
    EXPECT_TRUE(matches("/project/sub/app.tmp"));
    EXPECT_TRUE(matches("/project/dist"));

    std::remove(fname.c_str());
}

TEST(TestPublic, IncompleteFilename) {
    auto matches = parse_gitignore_str("app.js", "/public");
    EXPECT_TRUE(matches("/public/app.js"));
    EXPECT_FALSE(matches("/public/test.js"));
    EXPECT_FALSE(matches("/public/app.jsx"));
    EXPECT_TRUE(matches("/public/dir/app.js"));
    EXPECT_FALSE(matches("/public/dir/test.js"));
    EXPECT_FALSE(matches("/public/dir/app.jsx"));
}

TEST(TestPublic, Wildcard) {
    auto matches = parse_gitignore_str("error.*", "/tmp");
    EXPECT_TRUE(matches("/tmp/error.txt"));
    EXPECT_TRUE(matches("/tmp/error.bak/"));
    EXPECT_TRUE(matches("/tmp/dir/error.txt"));
    EXPECT_TRUE(matches("/tmp/error."));
    EXPECT_FALSE(matches("/tmp/error"));
    EXPECT_FALSE(matches("/tmp/errorX"));
}

TEST(TestPublic, AnchoredWildcard) {
    auto matches = parse_gitignore_str("/success.*", "/dirfoo");
    EXPECT_TRUE(matches("/dirfoo/success.txt"));
    EXPECT_TRUE(matches("/dirfoo/success.c"));
    EXPECT_FALSE(matches("/dirfoo/a/success.java"));
}

TEST(TestPublic, Trailingspaces) {
    auto matches = parse_gitignore_str(
        "ignoretailspace \n"
        "notignoredspace\\ \n"
        "almostignoredspace\\  \n"
        "almostignoredspace2 \\  \n"
        "notignoredmultiplespace\\ \\ \\ ",
        "/abc"
    );
    EXPECT_TRUE(matches("/abc/ignoretailspace"));
    EXPECT_FALSE(matches("/abc/ignoretailspace "));
    EXPECT_TRUE(matches("/abc/almostignoredspace "));
    EXPECT_FALSE(matches("/abc/almostignoredspace  "));
    EXPECT_FALSE(matches("/abc/almostignoredspace"));
    EXPECT_TRUE(matches("/abc/almostignoredspace2  "));
    EXPECT_FALSE(matches("/abc/almostignoredspace2   "));
    EXPECT_FALSE(matches("/abc/almostignoredspace2 "));
    EXPECT_FALSE(matches("/abc/almostignoredspace2"));
    EXPECT_TRUE(matches("/abc/notignoredspace "));
    EXPECT_FALSE(matches("/abc/notignoredspace"));
    EXPECT_TRUE(matches("/abc/notignoredmultiplespace   "));
    EXPECT_FALSE(matches("/abc/notignoredmultiplespace"));
}

TEST(TestPublic, Comment) {
    auto matches = parse_gitignore_str(
        "firstmatch\n"
        "#notrealcomment\n"
        "secondmatch\n"
        "\\#reallyamatch",
        "/bdir"
    );
    EXPECT_TRUE(matches("/bdir/firstmatch"));
    EXPECT_FALSE(matches("/bdir/#notrealcomment"));
    EXPECT_TRUE(matches("/bdir/secondmatch"));
    EXPECT_TRUE(matches("/bdir/#reallyamatch"));
}

TEST(TestPublic, IgnoreDirectory) {
    auto matches = parse_gitignore_str("cache/", "/mnt");
    EXPECT_TRUE(matches("/mnt/cache"));
    EXPECT_TRUE(matches("/mnt/cache/subdir"));
    EXPECT_TRUE(matches("/mnt/cache/file.txt"));
    EXPECT_FALSE(matches("/mnt/cachex"));
    EXPECT_FALSE(matches("/mnt/cache_v2.py"));
}

TEST(TestPublic, IgnoreDirectoryAsterisk) {
    auto matches = parse_gitignore_str("output/*", "/results");
    EXPECT_FALSE(matches("/results/output"));
    EXPECT_TRUE(matches("/results/output/folder"));
    EXPECT_TRUE(matches("/results/output/file.txt"));
}

TEST(TestPublic, Negation) {
    auto matches = parse_gitignore_str(
        "*.bak\n!keep.bak\n",
        "/store"
    );
    EXPECT_TRUE(matches("/store/junk.bak"));
    EXPECT_FALSE(matches("/store/keep.bak"));
    EXPECT_TRUE(matches("/store/lost.bak"));
}

TEST(TestPublic, LiteralExclamationMark) {
    auto matches = parse_gitignore_str("\\!saveit!", "/fs");
    EXPECT_TRUE(matches("/fs/!saveit!"));
    EXPECT_FALSE(matches("/fs/saveit!"));
    EXPECT_FALSE(matches("/fs/saveit"));
}

TEST(TestPublic, DoubleAsterisks) {
    auto matches = parse_gitignore_str("dir/**/Final", "/abc");
    EXPECT_TRUE(matches("/abc/dir/sub/Final"));
    EXPECT_TRUE(matches("/abc/dir/foo/Final"));
    EXPECT_TRUE(matches("/abc/dir/Final"));
    EXPECT_FALSE(matches("/abc/dir/Finals"));
}

TEST(TestPublic, DoubleAsteriskWithoutSlashes) {
    auto matches = parse_gitignore_str("m/n**o/p", "/usr");
    EXPECT_TRUE(matches("/usr/m/no/p"));
    EXPECT_TRUE(matches("/usr/m/nko/p"));
    EXPECT_TRUE(matches("/usr/m/nno/p"));
    EXPECT_TRUE(matches("/usr/m/noo/p"));
    EXPECT_FALSE(matches("/usr/m/nop"));
    EXPECT_FALSE(matches("/usr/m/n/o/p"));
    EXPECT_FALSE(matches("/usr/m/nn/oo/p"));
    EXPECT_FALSE(matches("/usr/m/nn/YY/oo/p"));
}

TEST(TestPublic, MoreAsterisksAsSingle) {
    auto matches = parse_gitignore_str("***z/x", "/sample");
    EXPECT_TRUE(matches("/sample/ABCz/x"));
    EXPECT_FALSE(matches("/sample/yyy/z/x"));
    matches = parse_gitignore_str("z/x***", "/sample");
    EXPECT_TRUE(matches("/sample/z/xABC"));
    EXPECT_FALSE(matches("/sample/z/x/abc"));
}

TEST(TestPublic, DirectoryOnlyNegation) {
    auto matches = parse_gitignore_str(
        "content/**\n!content/**/\n!.hold\n!content/01_data/*\n",
        "/vault"
    );
    EXPECT_FALSE(matches("/vault/content/01_data/"));
    EXPECT_FALSE(matches("/vault/content/01_data/.hold"));
    EXPECT_FALSE(matches("/vault/content/01_data/doc.csv"));
    EXPECT_FALSE(matches("/vault/content/02_final/"));
    EXPECT_FALSE(matches("/vault/content/02_final/.hold"));
    EXPECT_TRUE(matches("/vault/content/02_final/summary.txt"));
}

TEST(TestPublic, SingleAsterisk) {
    auto matches = parse_gitignore_str("*", "/misc");
    EXPECT_TRUE(matches("/misc/note.txt"));
    EXPECT_TRUE(matches("/misc/folder"));
    EXPECT_TRUE(matches("/misc/folder-trailing/"));
}

TEST(TestPublic, SupportsPathTypeArgument) {
    auto matches = parse_gitignore_str("image1\n!image2", "/photos");
    EXPECT_TRUE(matches(fs::path("/photos/image1")));
    EXPECT_FALSE(matches(fs::path("/photos/image2")));
}

TEST(TestPublic, SlashInRangeDoesNotMatchDirs) {
    auto matches = parse_gitignore_str("pqr[S-U/]stu", "/zdir");
    EXPECT_FALSE(matches("/zdir/pqrststu"));
    EXPECT_TRUE(matches("/zdir/pqrSstu"));
    EXPECT_TRUE(matches("/zdir/pqrTstu"));
    EXPECT_TRUE(matches("/zdir/pqrUstu"));
    EXPECT_FALSE(matches("/zdir/pqr/stu"));
    EXPECT_FALSE(matches("/zdir/pqrSTUstu"));
}

TEST(TestPublic, SymlinkToAnotherDirectory) {
    char rootdir[] = "/tmp/pubtXXXXXX";
    char otherdir[] = "/tmp/pubxXXXXXX";
    mkdtemp(rootdir);
    mkdtemp(otherdir);

    auto matches = parse_gitignore_str("linker", rootdir);
    std::string link_path = std::string(rootdir) + "/linker";
    std::string othdir = otherdir;

    symlink(othdir.c_str(), link_path.c_str());
    EXPECT_TRUE(matches(link_path));
    EXPECT_FALSE(matches(std::string(rootdir) + "/link"));

    std::filesystem::remove(link_path);
    std::filesystem::remove_all(otherdir);
    std::filesystem::remove_all(rootdir);
}