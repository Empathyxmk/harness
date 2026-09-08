use crate::command::{parser, map_from, ParsedArgs};
use std::collections::HashMap;

#[test]
fn test_command_equivalence_public() {
    let groups = vec![
        vec![vec!["start", "-p", "8080"], vec!["-p", "8080", "start"]],
        vec![
            vec!["start", "--procfile", "Customfile"],
            vec!["--procfile", "Customfile", "start"],
        ],
        vec![vec!["start", "--no-prefix"], vec!["--no-prefix", "start"]],
        vec![
            vec!["start", "--no-colour", "--no-prefix"],
            vec!["--no-prefix", "--no-colour", "start"],
            vec!["--no-colour", "start", "--no-prefix"],
        ]
    ];
    for mut commands in groups {
        assert!(commands.len() >= 2);
        let reference_args = commands.remove(0);
        let reference_result = parser.parse_args(&reference_args);
        for args in commands {
            let result = parser.parse_args(&args);
            assert_eq!(result, reference_result);
        }
    }
}

#[test]
fn test_port_precedence_public() {
    let args = parser.parse_args(&["start"]);
    let mut os_env = HashMap::new();
    let mut app_env = HashMap::new();

    let mut r = map_from(&args, None, None);
    assert_eq!(r["port"], "5000");

    os_env.insert("PORT".to_string(), "6500".to_string());
    let r = map_from(&args, Some(&os_env), None);
    assert_eq!(r["port"], "6500");

    app_env.insert("PORT".to_string(), "6700".to_string());
    let r = map_from(&args, Some(&os_env), Some(&app_env));
    assert_eq!(r["port"], "6700");

    let args = parser.parse_args(&["start", "-p", "8800"]);
    let r = map_from(&args, Some(&os_env), Some(&app_env));
    assert_eq!(r["port"], "8800");
}

#[test]
fn test_procfile_precedence_public() {
    let args = parser.parse_args(&["start"]);
    let mut os_env = HashMap::new();
    let mut app_env = HashMap::new();

    let r = map_from(&args, None, None);
    assert_eq!(r["procfile"], "Procfile");

    os_env.insert("PROCFILE".to_string(), "CustomProcfile.env".to_string());
    let r = map_from(&args, Some(&os_env), None);
    assert_eq!(r["procfile"], "CustomProcfile.env");

    app_env.insert("PROCFILE".to_string(), "CustomProcfile.app".to_string());
    let r = map_from(&args, Some(&os_env), Some(&app_env));
    assert_eq!(r["procfile"], "CustomProcfile.app");

    let args = parser.parse_args(&["start", "-f", "CustomProcfile.cli"]);
    let r = map_from(&args, Some(&os_env), Some(&app_env));
    assert_eq!(r["procfile"], "CustomProcfile.cli");
}