#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <set>
#include "wpanalyser/analyser.h"

TEST(PublicAnalyserCore, FileExtensionExtraction) {
    std::string filepath = "/home/user/wp-content/plugins/my-custom-plugin/hello-world.php";
    EXPECT_EQ(wpanalyser::get_file_extension(filepath), "php");
}

TEST(PublicAnalyserCore, NonPhpFileExtension) {
    std::string filepath = "/var/www/theme/functions.js";
    EXPECT_EQ(wpanalyser::get_file_extension(filepath), "js");
}

TEST(PublicAnalyserCore, WordpressPluginFolderExtraction) {
    std::string path = "/usr/share/wp-content/plugins/sample-plugin/file.php";
    EXPECT_EQ(wpanalyser::get_plugin_folder(path), "sample-plugin");
}

TEST(PublicAnalyserCore, WordpressThemeFolderExtraction) {
    std::string path = "/var/www/wp-content/themes/mytheme/index.php";
    EXPECT_EQ(wpanalyser::get_theme_folder(path), "mytheme");
}

TEST(PublicAnalyserCore, NonstandardThemeFolderReturnsNone) {
    std::string path = "/some/path/without/theme/structure/file.php";
    EXPECT_EQ(wpanalyser::get_theme_folder(path), "");
}

TEST(PublicAnalyserCore, NonWordpressPluginFolderReturnsNone) {
    std::string path = "/no/wp-content/here/plugins/any-plugin/file.php";
    EXPECT_EQ(wpanalyser::get_plugin_folder(path), "");
}

TEST(PublicAnalyserCore, DetectFunctionDefinition) {
    std::string php = "<?php\nfunction alpha_func($foo){ return $foo; }\n";
    auto funcs = wpanalyser::get_function_names(php);
    EXPECT_NE(std::find(funcs.begin(), funcs.end(), "alpha_func"), funcs.end());
}

TEST(PublicAnalyserCore, MultipleFunctionDefinitions) {
    std::string php = "<?php\nfunction a(){}\nfunction b($x){}\nfunction __setup(){}\n";
    auto funcs = wpanalyser::get_function_names(php);
    EXPECT_NE(std::find(funcs.begin(), funcs.end(), "b"), funcs.end());
    EXPECT_NE(std::find(funcs.begin(), funcs.end(), "a"), funcs.end());
    EXPECT_NE(std::find(funcs.begin(), funcs.end(), "__setup"), funcs.end());
}

TEST(PublicAnalyserCore, NoFunctionDefinitionsGivesEmptyList) {
    std::string php = "<?php\necho 'Just text';\n";
    auto funcs = wpanalyser::get_function_names(php);
    EXPECT_TRUE(funcs.empty());
}

TEST(PublicAnalyserCore, FindHooksDoAction) {
    std::string php = "<?php\ndo_action('custom_action');\nadd_action('init','cb');\n";
    auto hooks = wpanalyser::get_hooks(php);
    EXPECT_NE(std::find(hooks.begin(), hooks.end(), "custom_action"), hooks.end());
    EXPECT_NE(std::find(hooks.begin(), hooks.end(), "init"), hooks.end());
}

TEST(PublicAnalyserCore, FindFiltersAndHooks) {
    std::string php = "<?php\nadd_filter('my_filter','func');\ndo_action('demo');\n";
    auto hooks = wpanalyser::get_hooks(php);
    std::set<std::string> hookset(hooks.begin(), hooks.end());
    EXPECT_EQ(hookset, std::set<std::string>{"my_filter", "demo"});
}

TEST(PublicAnalyserCore, FileSizeCategorySmall) {
    EXPECT_EQ(wpanalyser::get_file_size_category(1234), "small");
}

TEST(PublicAnalyserCore, FileSizeCategoryLarge) {
    EXPECT_EQ(wpanalyser::get_file_size_category(10485760), "large");
}

TEST(PublicAnalyserCore, FileSizeCategoryMedium) {
    EXPECT_EQ(wpanalyser::get_file_size_category(1572864), "medium");
}