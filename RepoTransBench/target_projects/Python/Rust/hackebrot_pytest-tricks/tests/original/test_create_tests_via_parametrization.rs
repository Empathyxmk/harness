mod model_foobar;
use model_foobar::{Package, Woman, Man};

fn python_packages() -> Vec<Package> {
    vec![
        Package::new("requests", "Apache 2.0"),
        Package::new("django", "BSD"),
        Package::new("pytest", "MIT"),
    ]
}

fn make_persons() -> Vec<Box<dyn Programmer>> {
    vec![
        Box::new(Woman::new("Audrey")) as Box<dyn Programmer>,
        Box::new(Woman::new("Brianna")),
        Box::new(Man::new("Daniel")),
        Box::new(Woman::new("Ola")),
        Box::new(Man::new("Kenneth")),
    ]
}

trait Programmer {
    fn learn(&mut self, package: &str);
    fn looks_like_a_programmer(&self) -> bool;
}

impl Programmer for Man {
    fn learn(&mut self, package: &str) {
        self.learn(package);
    }
    fn looks_like_a_programmer(&self) -> bool {
        self.looks_like_a_programmer
    }
}

impl Programmer for Woman {
    fn learn(&mut self, package: &str) {
        self.learn(package);
    }
    fn looks_like_a_programmer(&self) -> bool {
        self.looks_like_a_programmer
    }
}

#[test]
fn test_become_a_programmer() {
    let mut persons = make_persons();
    for mut person in persons.iter_mut() {
        for pkg in python_packages() {
            person.learn(&pkg.name);
            assert!(person.looks_like_a_programmer());
        }
    }
}

#[test]
fn test_is_open_source() {
    for pkg in python_packages() {
        assert!(pkg.is_open_source());
    }
}