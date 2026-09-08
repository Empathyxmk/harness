use dfu_programmer::libdfu::{parse_arguments, dfu_programmer, ProgrammerArguments};

#[test]
fn test_main_args_error() {
    let argv = vec!["prog".to_string(), "fail".to_string()];
    let mut args = ProgrammerArguments::default();
    let parse_status = parse_arguments(&mut args, 2, argv);
    assert_eq!(parse_status, -1); // ARGUMENT_ERROR
}

#[test]
fn test_main_args_handled() {
    let argv = vec!["prog".to_string(), "handled".to_string()];
    let mut args = ProgrammerArguments::default();
    let parse_status = parse_arguments(&mut args, 2, argv);
    assert_eq!(parse_status, 1); // handled
}

#[test]
fn test_main_args_normal() {
    let argv = vec!["prog".to_string(), "default".to_string()];
    let mut args = ProgrammerArguments::default();
    let parse_status = parse_arguments(&mut args, 2, argv);
    assert_eq!(parse_status, 0); // Request to handle in programmer
    let status = dfu_programmer(Some(&args));
    assert_eq!(status, 123);
}