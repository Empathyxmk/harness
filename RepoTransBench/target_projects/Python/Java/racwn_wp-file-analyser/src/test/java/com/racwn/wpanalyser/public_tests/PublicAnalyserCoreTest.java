package com.racwn.wpanalyser.public_tests;

import com.racwn.wpanalyser.analyser.Analyser;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class PublicAnalyserCoreTest {

    @Test
    void testFileExtensionExtraction() {
        String filePath = "/home/user/wp-content/plugins/my-custom-plugin/hello-world.php";
        String result = Analyser.getFileExtension(filePath);
        assertEquals("php", result);
    }

    @Test
    void testNonPhpFileExtension() {
        String filePath = "/var/www/theme/functions.js";
        String result = Analyser.getFileExtension(filePath);
        assertEquals("js", result);
    }

    @Test
    void testWordpressPluginFolderExtraction() {
        String path = "/usr/share/wp-content/plugins/sample-plugin/file.php";
        String result = Analyser.getPluginFolder(path);
        assertEquals("sample-plugin", result);
    }

    @Test
    void testWordpressThemeFolderExtraction() {
        String path = "/var/www/wp-content/themes/mytheme/index.php";
        String result = Analyser.getThemeFolder(path);
        assertEquals("mytheme", result);
    }

    @Test
    void testNonstandardThemeFolderReturnsNone() {
        String path = "/some/path/without/theme/structure/file.php";
        String result = Analyser.getThemeFolder(path);
        assertNull(result);
    }

    @Test
    void testNonWordpressPluginFolderReturnsNone() {
        String path = "/no/wp-content/here/plugins/any-plugin/file.php";
        String result = Analyser.getPluginFolder(path);
        assertNull(result);
    }

    @Test
    void testDetectFunctionDefinition() {
        String php = "<?php\nfunction alpha_func($foo){ return $foo; }\n";
        List<String> funcs = Analyser.getFunctionNames(php);
        assertTrue(funcs.contains("alpha_func"));
    }

    @Test
    void testMultipleFunctionDefinitions() {
        String php = "<?php\nfunction a(){}\nfunction b($x){}\nfunction __setup(){}\n";
        List<String> funcs = Analyser.getFunctionNames(php);
        assertTrue(funcs.contains("a"));
        assertTrue(funcs.contains("b"));
        assertTrue(funcs.contains("__setup"));
    }

    @Test
    void testNoFunctionDefinitionsGivesEmptyList() {
        String php = "<?php\necho 'Just text';\n";
        List<String> funcs = Analyser.getFunctionNames(php);
        assertTrue(funcs.isEmpty());
    }

    @Test
    void testFindHooksDoAction() {
        String php = "<?php\ndo_action('custom_action');\nadd_action('init','cb');\n";
        List<String> hooks = Analyser.getHooks(php);
        assertTrue(hooks.contains("custom_action"));
        assertTrue(hooks.contains("init"));
    }

    @Test
    void testFindFiltersAndHooks() {
        String php = "<?php\nadd_filter('my_filter','func');\ndo_action('demo');\n";
        List<String> hooks = Analyser.getHooks(php);
        assertEquals(2, hooks.size());
        assertTrue(hooks.contains("my_filter"));
        assertTrue(hooks.contains("demo"));
    }

    @Test
    void testFileSizeCategorySmall() {
        String result = Analyser.getFileSizeCategory(1234);
        assertEquals("small", result);
    }

    @Test
    void testFileSizeCategoryLarge() {
        String result = Analyser.getFileSizeCategory(10485760);
        assertEquals("large", result);
    }

    @Test
    void testFileSizeCategoryMedium() {
        String result = Analyser.getFileSizeCategory(1572864);
        assertEquals("medium", result);
    }
}