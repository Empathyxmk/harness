#include <gtest/gtest.h>
#include <string>
#include "wpanalyser/analyser.h"

TEST(PublicAnalyserBranches, DifferentBranchCount) {
    std::string file_content = "<?php\nif(1){echo 'a';}else{echo 'b';}\nif(2){echo 'c';}\n";
    int result = wpanalyser::count_branches(file_content);
    EXPECT_EQ(result, 2);
}

TEST(PublicAnalyserBranches, SwitchCaseBranch) {
    std::string file_content = "<?php\nswitch($var){case 2: break; case 3: break; default: break;}\n";
    int result = wpanalyser::count_branches(file_content);
    EXPECT_EQ(result, 1);
}

TEST(PublicAnalyserBranches, MultipleElseifBranch) {
    std::string file_content = "<?php\nif($a==2){echo 2;}elseif($a==3){echo 3;}elseif($a==4){echo 4;}\n";
    int result = wpanalyser::count_branches(file_content);
    EXPECT_EQ(result, 1);
}

TEST(PublicAnalyserBranches, NestedIfElseBranch) {
    std::string file_content = "<?php\nif($a){if($b){echo 1;}else{echo 2;}}\n";
    int result = wpanalyser::count_branches(file_content);
    EXPECT_EQ(result, 2);
}

TEST(PublicAnalyserBranches, TryCatchCount) {
    std::string file_content = "<?php\ntry{ risky(); } catch(Exception $e) {} catch(Error $e) {}\n";
    int result = wpanalyser::count_branches(file_content);
    EXPECT_EQ(result, 1);
}