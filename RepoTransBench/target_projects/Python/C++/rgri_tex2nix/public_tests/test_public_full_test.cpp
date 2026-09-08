#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <algorithm>
#include "tex2nix.h"

TEST(PublicFullTest, FullTex2NixPipeline) {
    std::string tex_example = R"(
        \documentclass[10pt]{report}
        \usepackage{pdfpages}
        \usepackage{mhchem}
    )";
    auto pkgs = latex2nix(tex_example);
    EXPECT_TRUE(std::find(pkgs.begin(), pkgs.end(), "pdfpages") != pkgs.end());
    EXPECT_TRUE(std::find(pkgs.begin(), pkgs.end(), "mhchem") != pkgs.end());
    EXPECT_EQ(std::count(pkgs.begin(), pkgs.end(), "pdfpages"), 1);
    std::string docclass = detect_documentclass(tex_example);
    EXPECT_EQ(docclass, "report");
}