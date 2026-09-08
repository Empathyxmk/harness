use std::collections::HashMap;
use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;

#[derive(Clone, Debug, Eq)]
struct Edge {
    source: String,
    target: String,
}
impl Edge {
    fn new(src: &str, tgt: &str) -> Self {
        Edge { source: src.to_string(), target: tgt.to_string() }
    }
}
impl std::fmt::Display for Edge {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{} -> {}", self.source, self.target)
    }
}
impl PartialEq for Edge {
    fn eq(&self, other: &Self) -> bool {
        self.source == other.source && self.target == other.target
    }
}
impl Hash for Edge {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.source.hash(state);
        self.target.hash(state);
    }
}

#[derive(Clone, Debug, Eq)]
struct Node {
    name: String,
}
impl Node {
    fn new(name: &str) -> Self {
        Node { name: name.to_string() }
    }
}
impl std::fmt::Display for Node {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.name)
    }
}
impl PartialEq for Node {
    fn eq(&self, other: &Self) -> bool {
        self.name == other.name
    }
}
impl Hash for Node {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.name.hash(state);
    }
}

struct DummyVault {
    ciphertext: Option<String>
}
impl DummyVault {
    fn new(ciphertext: Option<&str>) -> Self {
        DummyVault { ciphertext: ciphertext.map(|s| s.to_string()) }
    }
}

#[derive(Hash, PartialEq, Eq, Clone, Debug)]
struct DummyGroup {
    name: String,
    parent_groups: Vec<DummyGroup>,
    ancestors: Vec<DummyGroup>,
}
impl DummyGroup {
    fn new(name: &str, parent_groups: Vec<DummyGroup>, ancestors: Vec<DummyGroup>) -> Self {
        DummyGroup {
            name: name.to_string(),
            parent_groups,
            ancestors
        }
    }
    fn get_ancestors(&self) -> &Vec<DummyGroup> {
        &self.ancestors
    }
}
struct DummyHost {
    name: String,
    groups: Vec<DummyGroup>,
    host_vars: HashMap<String, String>,
}
impl DummyHost {
    fn new(name: &str) -> Self {
        DummyHost {
            name: name.to_string(),
            groups: Vec::new(),
            host_vars: HashMap::new()
        }
    }
    fn set_groups(&mut self, groups: Vec<DummyGroup>) {
        self.groups = groups;
    }
}

struct DummyInventoryManager {
    group_vars: HashMap<String, HashMap<String, DummyVaultOrPlain>>,
    host_vars: HashMap<String, HashMap<String, DummyVaultOrPlain>>,
}
#[derive(Clone)]
enum DummyVaultOrPlain {
    Vault(DummyVault),
    Plain(String),
}
impl DummyInventoryManager {
    fn new(
        group_vars: HashMap<String, HashMap<String, DummyVaultOrPlain>>,
        host_vars: HashMap<String, HashMap<String, DummyVaultOrPlain>>
    ) -> Self {
        DummyInventoryManager { group_vars, host_vars }
    }
}

#[test]
fn test_edge_public_repr_eq_hash() {
    let e1 = Edge::new("x", "y");
    let e2 = Edge::new("x", "y");
    let e3 = Edge::new("x", "z");
    assert_eq!(format!("{}", e1), "x -> y");
    assert_eq!(e1, e2);
    assert_ne!(e1, e3);
    let mut hasher1 = DefaultHasher::new();
    e1.hash(&mut hasher1);
    let mut hasher2 = DefaultHasher::new();
    e2.hash(&mut hasher2);
    let mut hasher3 = DefaultHasher::new();
    e3.hash(&mut hasher3);
    assert_eq!(hasher1.finish(), hasher2.finish());
    assert_ne!(hasher1.finish(), hasher3.finish());
}

#[test]
fn test_node_public_repr_eq_hash() {
    let n1 = Node::new("nn");
    let n2 = Node::new("nn");
    let n3 = Node::new("yy");
    assert_eq!(format!("{}", n1), "nn");
    assert_eq!(n1, n2);
    assert_ne!(n1, n3);
    let mut hasher1 = DefaultHasher::new();
    n1.hash(&mut hasher1);
    let mut hasher2 = DefaultHasher::new();
    n2.hash(&mut hasher2);
    let mut hasher3 = DefaultHasher::new();
    n3.hash(&mut hasher3);
    assert_eq!(hasher1.finish(), hasher2.finish());
    assert_ne!(hasher1.finish(), hasher3.finish());
}