#include <gtest/gtest.h>
#include <filesystem>
#include "gitignore_parser.h"

using namespace gitignore;
namespace fs = std::filesystem;

TEST(GitignoreParserTests, Simple) {
    auto matches = parse_gitignore_str(
        "__pycache__/\n"
        "*.py[cod]", "/home/michael"
    );
    EXPECT_FALSE(matches("/home/michael/main.py"));
    EXPECT_TRUE(matches("/home/michael/main.pyc"));
    EXPECT_TRUE(matches("/home/michael/dir/main.pyc"));
    EXPECT_TRUE(matches("/home/michael/__pycache__"));
}

TEST(GitignoreParserTests, SimpleParseFile) {
    // Simulate opening a .gitignore containing '__pycache__/\n*.py[cod]'
    // We'll write to a temp file and read it back.
    std::string fname = "/tmp/test_gitignore_file";
    std::ofstream out(fname);
    out << "__pycache__/\n*.py[cod]";
    out.close();

    auto matches = parse_gitignore(fname);
    EXPECT_FALSE(matches("/home/michael/main.py"));
    EXPECT_TRUE(matches("/home/michael/main.pyc"));
    EXPECT_TRUE(matches("/home/michael/dir/main.pyc"));
    EXPECT_TRUE(matches("/home/michael/__pycache__"));

    std::remove(fname.c_str());
}

TEST(GitignoreParserTests, IncompleteFilename) {
    auto matches = parse_gitignore_str("o.py", "/home/michael");
    EXPECT_TRUE(matches("/home/michael/o.py"));
    EXPECT_FALSE(matches("/home/michael/foo.py"));
    EXPECT_FALSE(matches("/home/michael/o.pyc"));
    EXPECT_TRUE(matches("/home/michael/dir/o.py"));
    EXPECT_FALSE(matches("/home/michael/dir/foo.py"));
    EXPECT_FALSE(matches("/home/michael/dir/o.pyc"));
}

TEST(GitignoreParserTests, Wildcard) {
    auto matches = parse_gitignore_str("hello.*", "/home/michael");
    EXPECT_TRUE(matches("/home/michael/hello.txt"));
    EXPECT_TRUE(matches("/home/michael/hello.foobar/"));
    EXPECT_TRUE(matches("/home/michael/dir/hello.txt"));
    EXPECT_TRUE(matches("/home/michael/hello."));
    EXPECT_FALSE(matches("/home/michael/hello"));
    EXPECT_FALSE(matches("/home/michael/helloX"));
}

TEST(GitignoreParserTests, AnchoredWildcard) {
    auto matches = parse_gitignore_str("/hello.*", "/home/michael");
    EXPECT_TRUE(matches("/home/michael/hello.txt"));
    EXPECT_TRUE(matches("/home/michael/hello.c"));
    EXPECT_FALSE(matches("/home/michael/a/hello.java"));
}

TEST(GitignoreParserTests, Trailingspaces) {
    auto matches = parse_gitignore_str(
        "ignoretrailingspace \n"
        "notignoredspace\\ \n"
        "partiallyignoredspace\\  \n"
        "partiallyignoredspace2 \\  \n"
        "notignoredmultiplespace\\ \\ \\ ",
        "/home/michael"
    );
    EXPECT_TRUE(matches("/home/michael/ignoretrailingspace"));
    EXPECT_FALSE(matches("/home/michael/ignoretrailingspace "));
    EXPECT_TRUE(matches("/home/michael/partiallyignoredspace "));
    EXPECT_FALSE(matches("/home/michael/partiallyignoredspace  "));
    EXPECT_FALSE(matches("/home/michael/partiallyignoredspace"));
    EXPECT_TRUE(matches("/home/michael/partiallyignoredspace2  "));
    EXPECT_FALSE(matches("/home/michael/partiallyignoredspace2   "));
    EXPECT_FALSE(matches("/home/michael/partiallyignoredspace2 "));
    EXPECT_FALSE(matches("/home/michael/partiallyignoredspace2"));
    EXPECT_TRUE(matches("/home/michael/notignoredspace "));
    EXPECT_FALSE(matches("/home/michael/notignoredspace"));
    EXPECT_TRUE(matches("/home/michael/notignoredmultiplespace   "));
    EXPECT_FALSE(matches("/home/michael/notignoredmultiplespace"));
}

TEST(GitignoreParserTests, Comment) {
    auto matches = parse_gitignore_str(
        "somematch\n"
        "#realcomment\n"
        "othermatch\n"
        "\\#imnocomment",
        "/home/michael"
    );
    EXPECT_TRUE(matches("/home/michael/somematch"));
    EXPECT_FALSE(matches("/home/michael/#realcomment"));
    EXPECT_TRUE(matches("/home/michael/othermatch"));
    EXPECT_TRUE(matches("/home/michael/#imnocomment"));
}

TEST(GitignoreParserTests, IgnoreDirectory) {
    auto matches = parse_gitignore_str(".venv/", "/home/michael");
    EXPECT_TRUE(matches("/home/michael/.venv"));
    EXPECT_TRUE(matches("/home/michael/.venv/folder"));
    EXPECT_TRUE(matches("/home/michael/.venv/file.txt"));
    EXPECT_FALSE(matches("/home/michael/.venv_other_folder"));
    EXPECT_FALSE(matches("/home/michael/.venv_no_folder.py"));
}

TEST(GitignoreParserTests, IgnoreDirectoryAsterisk) {
    auto matches = parse_gitignore_str(".venv/*", "/home/michael");
    EXPECT_FALSE(matches("/home/michael/.venv"));
    EXPECT_TRUE(matches("/home/michael/.venv/folder"));
    EXPECT_TRUE(matches("/home/michael/.venv/file.txt"));
}

TEST(GitignoreParserTests, Negation) {
    auto matches = parse_gitignore_str(
        "*.ignore\n!keep.ignore\n",
        "/home/michael"
    );
    EXPECT_TRUE(matches("/home/michael/trash.ignore"));
    EXPECT_FALSE(matches("/home/michael/keep.ignore"));
    EXPECT_TRUE(matches("/home/michael/waste.ignore"));
}

TEST(GitignoreParserTests, LiteralExclamationMark) {
    auto matches = parse_gitignore_str("\\!ignore_me!", "/home/michael");
    EXPECT_TRUE(matches("/home/michael/!ignore_me!"));
    EXPECT_FALSE(matches("/home/michael/ignore_me!"));
    EXPECT_FALSE(matches("/home/michael/ignore_me"));
}

TEST(GitignoreParserTests, DoubleAsterisks) {
    auto matches = parse_gitignore_str("foo/**/Bar", "/home/michael");
    EXPECT_TRUE(matches("/home/michael/foo/hello/Bar"));
    EXPECT_TRUE(matches("/home/michael/foo/world/Bar"));
    EXPECT_TRUE(matches("/home/michael/foo/Bar"));
    EXPECT_FALSE(matches("/home/michael/foo/BarBar"));
}

TEST(GitignoreParserTests, DoubleAsteriskWithoutSlashes) {
    auto matches = parse_gitignore_str("a/b**c/d", "/home/michael");
    EXPECT_TRUE(matches("/home/michael/a/bc/d"));
    EXPECT_TRUE(matches("/home/michael/a/bXc/d"));
    EXPECT_TRUE(matches("/home/michael/a/bbc/d"));
    EXPECT_TRUE(matches("/home/michael/a/bcc/d"));
    EXPECT_FALSE(matches("/home/michael/a/bcd"));
    EXPECT_FALSE(matches("/home/michael/a/b/c/d"));
    EXPECT_FALSE(matches("/home/michael/a/bb/cc/d"));
    EXPECT_FALSE(matches("/home/michael/a/bb/XX/cc/d"));
}

TEST(GitignoreParserTests, MoreAsterisksAsSingle) {
    auto matches = parse_gitignore_str("***a/b", "/home/michael");
    EXPECT_TRUE(matches("/home/michael/XYZa/b"));
    EXPECT_FALSE(matches("/home/michael/foo/a/b"));
    matches = parse_gitignore_str("a/b***", "/home/michael");
    EXPECT_TRUE(matches("/home/michael/a/bXYZ"));
    EXPECT_FALSE(matches("/home/michael/a/b/foo"));
}

TEST(GitignoreParserTests, DirectoryOnlyNegation) {
    auto matches = parse_gitignore_str(
        "data/**\n!data/**/\n!.gitkeep\n!data/01_raw/*\n",
        "/home/michael"
    );
    EXPECT_FALSE(matches("/home/michael/data/01_raw/"));
    EXPECT_FALSE(matches("/home/michael/data/01_raw/.gitkeep"));
    EXPECT_FALSE(matches("/home/michael/data/01_raw/raw_file.csv"));
    EXPECT_FALSE(matches("/home/michael/data/02_processed/"));
    EXPECT_FALSE(matches("/home/michael/data/02_processed/.gitkeep"));
    EXPECT_TRUE(matches("/home/michael/data/02_processed/processed_file.csv"));
}

TEST(GitignoreParserTests, SingleAsterisk) {
    auto matches = parse_gitignore_str("*", "/home/michael");
    EXPECT_TRUE(matches("/home/michael/file.txt"));
    EXPECT_TRUE(matches("/home/michael/directory"));
    EXPECT_TRUE(matches("/home/michael/directory-trailing/"));
}

TEST(GitignoreParserTests, SupportsPathTypeArgument) {
    auto matches = parse_gitignore_str("file1\n!file2", "/home/michael");
    EXPECT_TRUE(matches(fs::path("/home/michael/file1")));
    EXPECT_FALSE(matches(fs::path("/home/michael/file2")));
}

TEST(GitignoreParserTests, SlashInRangeDoesNotMatchDirs) {
    auto matches = parse_gitignore_str("abc[X-Z/]def", "/home/michael");
    EXPECT_FALSE(matches("/home/michael/abcdef"));
    EXPECT_TRUE(matches("/home/michael/abcXdef"));
    EXPECT_TRUE(matches("/home/michael/abcYdef"));
    EXPECT_TRUE(matches("/home/michael/abcZdef"));
    EXPECT_FALSE(matches("/home/michael/abc/def"));
    EXPECT_FALSE(matches("/home/michael/abcXYZdef"));
}

TEST(GitignoreParserTests, SymlinkToAnotherDirectory) {
    // Use temp directories and symlinks
    char projdir[] = "/tmp/projXXXXXX";
    char anotherdir[] = "/tmp/othXXXXXX";
    mkdtemp(projdir);
    mkdtemp(anotherdir);

    auto matches = parse_gitignore_str("link", projdir);

    std::string link_path = std::string(projdir) + "/link";
    std::string target = std::string(anotherdir) + "/target";
    mkdir(target.c_str(), 0700);
    symlink(target.c_str(), link_path.c_str());

    // Symbolic links are not followed, matched as if they were files
    EXPECT_TRUE(matches(link_path));

    std::filesystem::remove(link_path);
    std::filesystem::remove_all(target);
    std::filesystem::remove_all(anotherdir);
    std::filesystem::remove_all(projdir);
}

TEST(GitignoreParserTests, SymlinkToSymlinkDirectory) {
    char pr[] = "/tmp/dirXXXXXX";
    char ld[] = "/tmp/lnkXXXXXX";
    mkdtemp(pr);
    mkdtemp(ld);

    std::string basedir(ld);

    std::string link = std::string(ld) + "/link";
    symlink(pr, link.c_str());
    std::string file = link + "/file.txt";

    auto matches = parse_gitignore_str("file.txt", basedir);
    EXPECT_TRUE(matches(file));

    std::filesystem::remove(link);
    std::filesystem::remove_all(ld);
    std::filesystem::remove_all(pr);
}