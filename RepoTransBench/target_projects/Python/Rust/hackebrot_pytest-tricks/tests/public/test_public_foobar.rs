mod model_foobar;
use model_foobar::{Man, Woman, Package};

fn public_python_package_names() -> Vec<String> {
    vec!["matplotlib".to_string(), "pandas".to_string()]
}

#[test]
fn test_become_a_programmer_public() {
    let mut persons = vec![
        Man::new("Oliver"),
        Woman::new("Amelia"),
        Man::new("Mason"),
        Man::new("Logan"),
        Woman::new("Harper")
    ];
    for person in persons.iter_mut() {
        for name in &public_python_package_names() {
            // Each learns the name, assert flag
            person.learn(name);
            assert!(person.looks_like_a_programmer);
        }
    }
}

#[test]
fn test_learn_multiple_packages_public() {
    let mut men = vec![
        Man::new("Jack"),
    ];
    let mut women = vec![
        Woman::new("Lily"),
    ];
    for m in men.iter_mut().chain(women.iter_mut()) {
        m.learn("sqlalchemy");
        m.learn("httpx");
        assert!(m.looks_like_a_programmer);
    }
}

#[test]
fn test_not_programmer_initially_public() {
    let men = vec![Man::new("Henry")];
    let women = vec![Woman::new("Ella")];
    for m in men.iter().chain(women.iter()) {
        assert!(!m.looks_like_a_programmer);
    }
}