use crate::analyser;

#[test]
fn test_different_branch_count() {
    let file_content = "<?php\nif(1){echo 'a';}else{echo 'b';}\nif(2){echo 'c';}\n";
    let result = analyser::count_branches(file_content);
    assert_eq!(result, 2);
}

#[test]
fn test_switch_case_branch() {
    let file_content = "<?php\nswitch($var){case 2: break; case 3: break; default: break;}\n";
    let result = analyser::count_branches(file_content);
    assert_eq!(result, 1);
}

#[test]
fn test_multiple_elseif_branch() {
    let file_content = "<?php\nif($a==2){echo 2;}elseif($a==3){echo 3;}elseif($a==4){echo 4;}\n";
    let result = analyser::count_branches(file_content);
    assert_eq!(result, 1);
}

#[test]
fn test_nested_if_else_branch() {
    let file_content = "<?php\nif($a){if($b){echo 1;}else{echo 2;}}\n";
    let result = analyser::count_branches(file_content);
    assert_eq!(result, 2);
}

#[test]
fn test_try_catch_count() {
    let file_content = "<?php\ntry{ risky(); } catch(Exception $e) {} catch(Error $e) {}\n";
    let result = analyser::count_branches(file_content);
    assert_eq!(result, 1);
}