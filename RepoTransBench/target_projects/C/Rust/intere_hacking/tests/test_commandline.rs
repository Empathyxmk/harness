use intere_hacking::main_commandline;

#[test]
fn test_single_arg() {
    let argv1 = vec!["prog".to_string()];
    let result = main_commandline(1, argv1);
    assert_eq!(result, 0);
}

#[test]
fn test_multiple_args() {
    let argv3 = vec!["prog".to_string(), "alpha".to_string(), "beta".to_string()];
    let result = main_commandline(3, argv3);
    assert_eq!(result, 0);
    println!("commandline coverage run complete");
}