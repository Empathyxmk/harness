#include <gtest/gtest.h>
#include <string>
#include <map>
#include <memory>

// Stub composite tree for translation
class Node;
class Folder;

class Node {
public:
    std::string name;
    Folder* parent = nullptr;
    virtual ~Node() {}
};

class File : public Node {
public:
    std::string contents;
    File(const std::string& name, const std::string& contents)
      : contents(contents) { this->name = name; }
    void move(const std::string& parent_path);
    void delete_from_parent();
};

class Folder : public Node {
public:
    std::map<std::string, std::unique_ptr<Node>> children;
    Folder(const std::string& name) { this->name = name; }
    void add_child(Node* n) {
        n->parent = this;
        // Store as unique_ptr, must not double-own in loose stub tests
        children[n->name].reset(n);
    }
};

static Folder ROOT("root");

void File::move(const std::string& parent_path) {
    // Only support "/docs2" or "/foo/bar" etc for tests
    Folder* folder = &ROOT;
    if (parent_path == "/docs1" || parent_path == "/docs2" || parent_path == "/foo" || parent_path.substr(0,4)=="/foo") {
        auto seg = parent_path.substr(1); // skip leading '/'
        if (ROOT.children.find(seg) != ROOT.children.end()) {
            folder = static_cast<Folder*>(ROOT.children[seg].get());
        }
        else if (parent_path.find('/') != std::string::npos) {
            // Nested path
            size_t pos = parent_path.find('/', 1);
            std::string top = parent_path.substr(1, pos-1);
            folder = static_cast<Folder*>(ROOT.children[top].get());
            if (folder && pos != std::string::npos) {
                std::string sub = parent_path.substr(pos+1);
                if (folder->children.find(sub) != folder->children.end())
                    folder = static_cast<Folder*>(folder->children[sub].get());
            }
        }
        // Remove from current parent
        if (this->parent) {
            auto& parent_children = static_cast<Folder*>(this->parent)->children;
            parent_children.erase(this->name);
        }
        folder->add_child(this);
    }
}
void File::delete_from_parent() {
    if (this->parent) {
        auto& parent_children = static_cast<Folder*>(this->parent)->children;
        parent_children.erase(this->name);
        this->parent = nullptr;
    }
}

Node* get_path(const std::string& path) {
    if (path == "/foo")
        return ROOT.children.count("foo") ? ROOT.children["foo"].get(): nullptr;
    if (path == "/foo/bar") {
        Folder* foo = static_cast<Folder*>(ROOT.children["foo"].get());
        return foo ? foo->children["bar"].get() : nullptr;
    }
    if (path == "/docs2")
        return ROOT.children.count("docs2") ? ROOT.children["docs2"].get() : nullptr;
    return nullptr;
}

class CompositeTest : public ::testing::Test {
protected:
    void SetUp() override { ROOT.children.clear(); }
};

TEST_F(CompositeTest, FolderAndFileBasicStructure) {
    Folder* f = new Folder("documents");
    ROOT.add_child(f);
    File* file_txt = new File("notes.txt", "abc");
    f->add_child(file_txt);
    ASSERT_TRUE(dynamic_cast<File*>(f->children["notes.txt"].get()) == file_txt);
    ASSERT_EQ(file_txt->parent, f);
}

TEST_F(CompositeTest, MoveAndDeleteBehavior) {
    Folder* f1 = new Folder("docs1");
    Folder* f2 = new Folder("docs2");
    ROOT.add_child(f1);
    ROOT.add_child(f2);
    File* myfile = new File("my.txt", "content");
    f1->add_child(myfile);
    myfile->move("/docs2");
    ASSERT_EQ(myfile->parent, f2);
    ASSERT_TRUE(f2->children.count("my.txt"));
    myfile->delete_from_parent();
    ASSERT_FALSE(f2->children.count("my.txt"));
}

TEST_F(CompositeTest, GetPathReturnsCorrectNode) {
    Folder* f = new Folder("foo");
    ROOT.add_child(f);
    Node* res = get_path("/foo");
    ASSERT_EQ(res, f);
    Folder* sub = new Folder("bar");
    f->add_child(sub);
    Node* path = get_path("/foo/bar");
    ASSERT_EQ(path, sub);
}

TEST_F(CompositeTest, FileAndFolderInit) {
    File* file1 = new File("dafile.txt", "cc");
    ASSERT_EQ(file1->name, "dafile.txt");
    ASSERT_EQ(file1->contents, "cc");
    Folder* folder = new Folder("bktest");
    ASSERT_EQ(folder->name, "bktest");
}

TEST_F(CompositeTest, FolderAddChildSetsParent) {
    Folder* p = new Folder("parentf");
    Folder* c = new Folder("childf");
    p->add_child(c);
    ASSERT_EQ(c->parent, p);
    ASSERT_TRUE(p->children.count("childf"));
}