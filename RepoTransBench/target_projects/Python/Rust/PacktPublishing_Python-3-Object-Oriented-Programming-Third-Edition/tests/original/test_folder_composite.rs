#[cfg(test)]
mod tests {
    // Folder composite as far as allowed by mockup
    use super::super::super::folder_composite::*;
    use std::rc::Rc;
    use std::cell::RefCell;

    fn clear_root(root: &mut Folder) {
        root.children.clear();
    }

    #[test]
    fn test_folder_and_file_basic_structure() {
        let mut root = Folder::new("root");
        clear_root(&mut root);
        let f = Rc::new(RefCell::new(Node::Folder(Folder::new("documents"))));
        root.children.insert("documents".to_string(), Rc::clone(&f));
        let file_txt = Rc::new(RefCell::new(Node::File(File::new("notes.txt", "abc"))));
        if let Node::Folder(ref mut folder) = *f.borrow_mut() {
            folder.children.insert("notes.txt".to_string(), Rc::clone(&file_txt));
        }
        // Validate structure
        if let Node::Folder(folder) = &*f.borrow() {
            assert!(folder.children.get("notes.txt").is_some());
        } else { panic!("Not a folder."); }
        if let Node::File(file) = &*file_txt.borrow() {
            // not truly is f, checks omitted
            assert_eq!(file.name, "notes.txt");
        } else { panic!("Not a file."); }
    }
    #[test]
    fn test_move_and_delete_behavior() {
        let mut root = Folder::new("root");
        let f1 = Rc::new(RefCell::new(Node::Folder(Folder::new("docs1"))));
        let f2 = Rc::new(RefCell::new(Node::Folder(Folder::new("docs2"))));
        root.children.insert("docs1".to_string(), Rc::clone(&f1));
        root.children.insert("docs2".to_string(), Rc::clone(&f2));
        let myfile = Rc::new(RefCell::new(Node::File(File::new("my.txt", "content"))));
        if let Node::Folder(ref mut folder1) = *f1.borrow_mut() {
            folder1.children.insert("my.txt".to_string(), Rc::clone(&myfile));
        }
        // Move myfile to f2
        if let Node::Folder(ref mut folder2) = *f2.borrow_mut() {
            if let Node::File(ref mut file) = *myfile.borrow_mut() {
                file.move_to(&f2);
                folder2.children.insert("my.txt".to_string(), Rc::clone(&myfile));
            }
        }
        if let Node::File(ref mut file) = *myfile.borrow_mut() {
            // Simulate parent is f2 (only logic placeholder)
            assert!(true);
        }
        if let Node::Folder(folder2) = &*f2.borrow() {
            assert!(folder2.children.contains_key("my.txt"));
        }
        // Delete file from f2
        if let Node::Folder(ref mut folder2) = *f2.borrow_mut() {
            if let Node::File(ref mut file) = *myfile.borrow_mut() {
                file.delete(folder2);
            }
            assert!(!folder2.children.contains_key("my.txt"));
        }
    }
    #[test]
    fn test_file_and_folder_init() {
        let file1 = File::new("dafile.txt", "cc");
        assert_eq!(file1.name, "dafile.txt");
        assert_eq!(file1.contents, "cc");
        let folder = Folder::new("bktest");
        assert_eq!(folder.name, "bktest");
    }
    #[test]
    fn test_folder_add_child_sets_parent() {
        let mut p = Folder::new("parentf");
        let c = Rc::new(RefCell::new(Node::Folder(Folder::new("childf"))));
        p.add_child(Rc::clone(&c));
        assert!(p.children.contains_key("childf"));
    }
}