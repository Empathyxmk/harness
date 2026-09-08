use crate::analyser;

#[test]
fn test_file_extension_extraction() {
    let file_path = "/home/user/wp-content/plugins/my-custom-plugin/hello-world.php";
    let result = analyser::get_file_extension(file_path);
    assert_eq!(result.unwrap(), "php".to_string());
}

#[test]
fn test_non_php_file_extension() {
    let file_path = "/var/www/theme/functions.js";
    let result = analyser::get_file_extension(file_path);
    assert_eq!(result.unwrap(), "js".to_string());
}

#[test]
fn test_wordpress_plugin_folder_extraction() {
    let path = "/usr/share/wp-content/plugins/sample-plugin/file.php";
    let result = analyser::get_plugin_folder(path);
    assert_eq!(result.unwrap(), "sample-plugin".to_string());
}

#[test]
fn test_wordpress_theme_folder_extraction() {
    let path = "/var/www/wp-content/themes/mytheme/index.php";
    let result = analyser::get_theme_folder(path);
    assert_eq!(result.unwrap(), "mytheme".to_string());
}

#[test]
fn test_nonstandard_theme_folder_returns_none() {
    let path = "/some/path/without/theme/structure/file.php";
    let result = analyser::get_theme_folder(path);
    assert!(result.is_none());
}

#[test]
fn test_non_wordpress_plugin_folder_returns_none() {
    let path = "/no/wp-content/here/plugins/any-plugin/file.php";
    let result = analyser::get_plugin_folder(path);
    assert!(result.is_none());
}

#[test]
fn test_detect_function_definition() {
    let php = "<?php\nfunction alpha_func($foo){ return $foo; }\n";
    let funcs = analyser::get_function_names(php);
    assert!(funcs.contains(&"alpha_func".to_string()));
}

#[test]
fn test_multiple_function_definitions() {
    let php = "<?php\nfunction a(){}\nfunction b($x){}\nfunction __setup(){}\n";
    let funcs = analyser::get_function_names(php);
    assert!(funcs.contains(&"a".to_string()));
    assert!(funcs.contains(&"b".to_string()));
    assert!(funcs.contains(&"__setup".to_string()));
}

#[test]
fn test_no_function_definitions_gives_empty_list() {
    let php = "<?php\necho 'Just text';\n";
    let funcs = analyser::get_function_names(php);
    assert_eq!(funcs.len(), 0);
}

#[test]
fn test_find_hooks_do_action() {
    let php = "<?php\ndo_action('custom_action');\nadd_action('init','cb');\n";
    let hooks = analyser::get_hooks(php);
    assert!(hooks.contains(&"custom_action".to_string()));
    assert!(hooks.contains(&"init".to_string()));
}

#[test]
fn test_find_filters_and_hooks() {
    let php = "<?php\nadd_filter('my_filter','func');\ndo_action('demo');\n";
    let hooks = analyser::get_hooks(php);
    let hs: std::collections::HashSet<_> = hooks.into_iter().collect();
    let expected: std::collections::HashSet<_> = ["my_filter".to_string(), "demo".to_string()].iter().cloned().collect();
    assert_eq!(hs, expected);
}

#[test]
fn test_file_size_category_small() {
    let result = analyser::get_file_size_category(1234);
    assert_eq!(result, "small".to_string());
}

#[test]
fn test_file_size_category_large() {
    let result = analyser::get_file_size_category(10485760);
    assert_eq!(result, "large".to_string());
}

#[test]
fn test_file_size_category_medium() {
    let result = analyser::get_file_size_category(1572864);
    assert_eq!(result, "medium".to_string());
}