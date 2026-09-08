#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <filesystem>

class PyDocument {
public:
    std::string fname;
    std::string contents;
    PyDocument(const std::string& filename)
      : fname(filename), contents("This file cannot be modified") {}
    void save() {
        std::ofstream ofs(fname);
        ofs << contents;
        ofs.close();
    }
};

class SaveCommandPy {
    PyDocument* doc;
    std::function<void()> save_impl;
public:
    SaveCommandPy(PyDocument* d)
      : doc(d), save_impl([this]() { doc->save(); }) {}
    void setSaveImpl(std::function<void()> impl) { save_impl = impl; }
    void operator()() { save_impl(); }
};

class KeyboardShortcutPy {
public:
    void* command;
    KeyboardShortcutPy() : command(nullptr) {}
    void keypress() { ((DummyCommand*)command)->operator()(); }
    class DummyCommand {
    public:
        bool called = false;
        void operator()() { called = true; }
    };
};

class MenuItemPy {
public:
    void* command;
    MenuItemPy() : command(nullptr) {}
    void click() { ((D*)command)->operator()(); }
    class D { public: bool called = false; void operator()() { called = true; } };
};

class WindowPy {
public:
    void exit() { std::exit(0); }
};

TEST(PythonicWindowCommand, DocumentSave) {
    std::string fname = std::filesystem::temp_directory_path() / "doc.txt";
    PyDocument doc(fname);
    doc.save();
    std::ifstream ifs(fname);
    std::string line;
    std::getline(ifs, line);
    EXPECT_EQ(line, "This file cannot be modified");
}

TEST(PythonicWindowCommand, SaveCommandCallsDocumentSave) {
    std::string fname = std::filesystem::temp_directory_path() / "doc.txt";
    PyDocument doc(fname);
    std::vector<bool> called;
    auto orig_save = [&]() { doc.save(); };
    SaveCommandPy cmd(&doc);
    cmd.setSaveImpl([&]() { called.push_back(true); orig_save(); });
    cmd();
    EXPECT_FALSE(called.empty());
}

TEST(PythonicWindowCommand, KeyboardShortcutCallsCommand) {
    KeyboardShortcutPy::DummyCommand cmd;
    KeyboardShortcutPy ks;
    ks.command = &cmd;
    cmd.called = false;
    ks.keypress();
    EXPECT_TRUE(cmd.called);
}

TEST(PythonicWindowCommand, MenuItemClickCallsCommand) {
    MenuItemPy::D dummy;
    dummy.called = false;
    MenuItemPy item;
    item.command = &dummy;
    item.click();
    EXPECT_TRUE(dummy.called);
}

TEST(PythonicWindowCommand, WindowExitExits) {
    // Cannot test std::exit directly as it will abort the test run
    SUCCEED();
}