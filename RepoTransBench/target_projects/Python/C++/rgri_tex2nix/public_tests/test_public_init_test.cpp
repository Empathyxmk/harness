#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <set>
#include <algorithm>
#include <filesystem>
#include <fstream>
#include "tex2nix.h"

std::string get_version() {
    // Simulate Python's __version__ retrieval from tex2nix module for test.
    if (tex2nix::__version__ && *tex2nix::__version__ != '\0') {
        return tex2nix::__version__;
    }
    return "";
}

TEST(PublicInitTest, Tex2NixVersion) {
    std::string version = get_version();
    if (!version.empty()) {
        EXPECT_GE(version.size(), 5u);
        auto dot1 = version.find('.');
        auto dot2 = version.find('.', dot1+1);
        EXPECT_NE(dot1, std::string::npos);
        EXPECT_NE(dot2, std::string::npos);
    }
}

TEST(PublicInitTest, MainEntryReturnsNone) {
    // Simulate main_entry, and check it runs without exceptions or errors
    EXPECT_NO_THROW(main_entry());
}

TEST(PublicInitTest, Latex2NixExampleUsage) {
    std::string input_tex = R"(
        \documentclass{scrreprt}
        \usepackage{fancyhdr}
        \usepackage{longtable}
        \begin{document}
        LaTeX public sample!
        \end{document}
    )";
    auto pkgs = latex2nix(input_tex);
    EXPECT_TRUE(pkgs.size() > 0);
    EXPECT_TRUE(std::find(pkgs.begin(), pkgs.end(), "fancyhdr") != pkgs.end());
    EXPECT_TRUE(std::find(pkgs.begin(), pkgs.end(), "longtable") != pkgs.end());
    EXPECT_TRUE(std::find(pkgs.begin(), pkgs.end(), "geometry") == pkgs.end());
}

TEST(PublicInitTest, Latex2NixHandlesEmpty) {
    auto pkgs = latex2nix("");
    EXPECT_EQ(pkgs, std::vector<std::string>{});
}

TEST(PublicInitTest, Latex2NixNoDuplicates) {
    std::string input_tex = R"(
        \usepackage{todonotes}
        \usepackage{todonotes}
        \usepackage{colortbl}
    )";
    auto pkgs = latex2nix(input_tex);
    EXPECT_EQ(std::count(pkgs.begin(), pkgs.end(), "todonotes"), 1);
    EXPECT_EQ(std::count(pkgs.begin(), pkgs.end(), "colortbl"), 1);
}

TEST(PublicInitTest, Latex2NixCustomPackage) {
    std::string input_tex = R"(
        \documentclass{standalone}
        \usepackage{publicpackage}
        \begin{document}
        Public
        \end{document}
    )";
    auto pkgs = latex2nix(input_tex);
    EXPECT_TRUE(std::find(pkgs.begin(), pkgs.end(), "publicpackage") != pkgs.end());
}

TEST(PublicInitTest, Latex2NixMultilineUsepackage) {
    std::string input_tex = R"(
        \usepackage{pgfplots,
        subcaption,
        caption}
    )";
    auto pkgs = latex2nix(input_tex);
    for (const auto& p : {"pgfplots","subcaption","caption"}) {
        EXPECT_TRUE(std::find(pkgs.begin(), pkgs.end(), p) != pkgs.end());
    }
}

TEST(PublicInitTest, Latex2NixWithCommentLines) {
    std::string input_tex = R"(
        % Just a comment line
        \usepackage{blindtext}
        % trailing comment
    )";
    auto pkgs = latex2nix(input_tex);
    EXPECT_TRUE(std::find(pkgs.begin(), pkgs.end(), "blindtext") != pkgs.end());
}

TEST(PublicInitTest, Latex2NixOptionalArg) {
    std::string input_tex = R"(
        \usepackage[top=2cm]{geometry}
        \usepackage[usenames]{color}
    )";
    auto pkgs = latex2nix(input_tex);
    EXPECT_TRUE(std::find(pkgs.begin(), pkgs.end(), "geometry") != pkgs.end());
    EXPECT_TRUE(std::find(pkgs.begin(), pkgs.end(), "color") != pkgs.end());
}

TEST(PublicInitTest, Latex2NixIgnoresUnrelatedLines) {
    std::string input_tex = R"(
        123 random text line
        \date{}
    )";
    auto pkgs = latex2nix(input_tex);
    EXPECT_TRUE(pkgs.empty());
}

TEST(PublicInitTest, DetectDocumentclass) {
    std::string input_tex = R"(
        \documentclass{memoir}
        \usepackage{zref}
    )";
    std::string docclass = detect_documentclass(input_tex);
    EXPECT_EQ(docclass, "memoir");
}

TEST(PublicInitTest, DetectDocumentclassNone) {
    std::string input_tex = R"(
        % no docclass here
        \usepackage{moreverb}
    )";
    std::string docclass = detect_documentclass(input_tex);
    EXPECT_EQ(docclass, "");
}