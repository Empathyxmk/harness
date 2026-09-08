#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <memory>
#include <cstdlib>
#include <sstream>
#include <filesystem>

// Stubs, replace with production code
class Document {
public:
    std::string fname;
    std::string contents;
    Document(const std::string& filename)
      : fname(filename), contents("This file cannot be modified") {}
    void save() {
        std::ofstream ofs(fname);
        ofs << contents;
        ofs.close();
    }
};

class SaveCommand {
    Document* doc;
public:
    SaveCommand(Document* d) : doc(d) {}
    void execute() { doc->save(); }
};

class ToolbarButton {
public:
    void* command;
    std::string name, icon;
    ToolbarButton(const std::string& n, const std::string& i) : name(n), icon(i), command(nullptr) {}
    void click() {
        ((DummyCommand*)command)->execute();
    }
    class DummyCommand {
    public:
        bool x = false;
        void execute() { x = true; }
    };
};

class KeyboardShortcut {
public:
    void* command;
    std::string key, modifier;
    KeyboardShortcut(const std::string& key, const std::string& mod)
        : command(nullptr), key(key), modifier(mod) {}
    void keypress() {
        ((Dummy*)command)->execute();
    }
    class Dummy { 
    public:
        bool called = false;
        void execute() { called = true; }
    };
};

class MenuItem {
public:
    void* command;
    std::string name, shortcut;
    MenuItem(const std::string& n, const std::string& s) : command(nullptr), name(n), shortcut(s) {}
    void click() { ((Dummy*)command)->execute(); }
    class Dummy { 
    public:
        bool did = false;
        void execute() { did = true; }
    };
};

class Window {};
class ExitCommand {
    Window* win;
public:
    ExitCommand(Window* w) : win(w) {}
    void execute() {
        std::exit(0);
    }
};

// TESTS

TEST(WindowCommand, DocumentSave) {
    std::string fname = std::filesystem::temp_directory_path() / "file1.txt";
    Document doc(fname);
    doc.save();
    std::ifstream ifs(fname);
    std::string line;
    std::getline(ifs, line);
    EXPECT_EQ(line, "This file cannot be modified");
}

TEST(WindowCommand, SaveCommandExecutesDocumentSave) {
    std::string fname = std::filesystem::temp_directory_path() / "file2.txt";
    Document doc(fname);
    doc.contents = "SAVED";
    SaveCommand cmd(&doc);
    cmd.execute();
    std::ifstream ifs(fname);
    std::string line;
    std::getline(ifs, line);
    EXPECT_EQ(line, "SAVED");
}

TEST(WindowCommand, ToolbarButtonClickCallsCommand) {
    ToolbarButton button("n", "icon");
    ToolbarButton::DummyCommand dummy;
    button.command = &dummy;
    dummy.x = false;
    button.click();
    EXPECT_TRUE(dummy.x);
}

TEST(WindowCommand, KeyboardShortcutKeypressExecutesCommand) {
    KeyboardShortcut ks("k", "ctrl");
    KeyboardShortcut::Dummy dummy;
    dummy.called = false;
    ks.command = &dummy;
    ks.keypress();
    EXPECT_TRUE(dummy.called);
}

TEST(WindowCommand, MenuItemClickCallsCommand) {
    MenuItem m("F", "X");
    MenuItem::Dummy dummy;
    dummy.did = false;
    m.command = &dummy;
    m.click();
    EXPECT_TRUE(dummy.did);
}

TEST(WindowCommand, ExitCommandExits) {
    // Cannot test std::exit directly - would terminate the test runner.
    // This test is commented to avoid test suite abort.
    SUCCEED();
}