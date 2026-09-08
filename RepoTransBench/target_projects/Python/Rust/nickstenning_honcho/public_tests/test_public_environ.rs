use crate::environ::*;

#[test]
fn test_environ_parse() {
    let samples = vec![
        ("
        BAR=foo
        ", [("BAR","foo")].iter().cloned().collect()),
        ("
        ALPHA=beta
        GAMMA=delta
        ", [("ALPHA","beta"),("GAMMA","delta")].iter().cloned().collect()),
        ("QUX=baz", [("QUX","baz")].iter().cloned().collect()),
        ("#another comment", std::collections::HashMap::new()),
        ("*item=value", std::collections::HashMap::new()),
        ("VAR1='hi\\\"there'", [("VAR1","hi\\\"there")].iter().cloned().collect()),
        ("VAR2=\"bye'now\"", [("VAR2","bye'now")].iter().cloned().collect()),
        (r#"VAR3='"public"'"#, [("VAR3",r#""public""#)].iter().cloned().collect()),
        (r#"VAR4=\"hello\""#, [("VAR4",r#""hello""#)].iter().cloned().collect()),
        (r#"EMAIL=another@address.com"#, [("EMAIL","another@address.com")].iter().cloned().collect()),
        (r#"MYVAR=!sym#bols^"#, [("MYVAR","!sym#bols^")].iter().cloned().collect()),
        (r#"EMOJI=😀🚀🔥"#, [("EMOJI","😀🚀🔥")].iter().cloned().collect()),
        (r#"SPACED='another one'"#, [("SPACED","another one")].iter().cloned().collect()),
        (r#"T1='bar\\tbaz'
T2='baz\\nqux'
T3='baz\\$qux'"#, [("T1","bar\\tbaz"),("T2","baz\\nqux"),("T3","baz\\$qux")].iter().cloned().collect())
    ];

    for (content, commands) in samples {
        let result = parse(content);
        for (k, v) in commands.iter() {
            assert_eq!(result.get(*k).unwrap(), v);
        }
        assert_eq!(result.len(), commands.len());
    }
}