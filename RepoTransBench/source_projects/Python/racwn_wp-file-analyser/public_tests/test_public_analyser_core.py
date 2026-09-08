import sys
import os
import pytest

# Ensure the wpanalyser package is on the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import wpanalyser.analyser as analyser


def test_file_extension_extraction():
    # Different file name from originals
    file_path = "/home/user/wp-content/plugins/my-custom-plugin/hello-world.php"
    result = analyser.get_file_extension(file_path)
    assert result == "php"

def test_non_php_file_extension():
    file_path = "/var/www/theme/functions.js"
    result = analyser.get_file_extension(file_path)
    assert result == "js"

def test_wordpress_plugin_folder_extraction():
    path = "/usr/share/wp-content/plugins/sample-plugin/file.php"
    result = analyser.get_plugin_folder(path)
    assert result == "sample-plugin"

def test_wordpress_theme_folder_extraction():
    path = "/var/www/wp-content/themes/mytheme/index.php"
    result = analyser.get_theme_folder(path)
    assert result == "mytheme"

def test_nonstandard_theme_folder_returns_none():
    path = "/some/path/without/theme/structure/file.php"
    result = analyser.get_theme_folder(path)
    assert result is None

def test_non_wordpress_plugin_folder_returns_none():
    path = "/no/wp-content/here/plugins/any-plugin/file.php"
    result = analyser.get_plugin_folder(path)
    assert result is None

def test_detect_function_definition():
    php = "<?php\nfunction alpha_func($foo){ return $foo; }\n"
    funcs = analyser.get_function_names(php)
    assert "alpha_func" in funcs

def test_multiple_function_definitions():
    php = "<?php\nfunction a(){}\nfunction b($x){}\nfunction __setup(){}\n"
    funcs = analyser.get_function_names(php)
    assert "b" in funcs and "a" in funcs and "__setup" in funcs

def test_no_function_definitions_gives_empty_list():
    php = "<?php\necho 'Just text';\n"
    funcs = analyser.get_function_names(php)
    assert funcs == []

def test_find_hooks_do_action():
    php = "<?php\ndo_action('custom_action');\nadd_action('init','cb');\n"
    hooks = analyser.get_hooks(php)
    assert "custom_action" in hooks and "init" in hooks

def test_find_filters_and_hooks():
    php = "<?php\nadd_filter('my_filter','func');\ndo_action('demo');\n"
    hooks = analyser.get_hooks(php)
    assert set(hooks) == {"my_filter", "demo"}

def test_file_size_category_small():
    result = analyser.get_file_size_category(1234)  # Small size
    assert result == "small"

def test_file_size_category_large():
    result = analyser.get_file_size_category(10485760)  # 10MB
    assert result == "large"

def test_file_size_category_medium():
    result = analyser.get_file_size_category(1572864)  # 1.5MB
    assert result == "medium"