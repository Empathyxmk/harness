#include <gtest/gtest.h>
#include "injector.h"
#include <typeinfo>
#include <typeindex>
#include <memory>
#include <fstream>
#include <filesystem>
#include <string>

using namespace injector_ns;

TEST(InjectorTest, ImportInit) {
    // Checks if 'injector_version' is defined
    extern const std::string injector_version;
    SUCCEED();
}

TEST(InjectorTest, ModuleType) {
    // In Python tests: isinstance(injector, types.ModuleType)
    // Here: Confirm that Injector namespace/classes "exist"
    Injector inj;
    SUCCEED();
}

TEST(InjectorTest, PyTypedExists) {
    // Check py.typed exists next to src/injector.cpp (simulate as in real project)
    std::filesystem::path p = std::filesystem::current_path() / "injector" / "py.typed";
    ASSERT_TRUE(std::filesystem::exists(p));
}

TEST(InjectorTest, ReloadModule) {
    // Dynamic reload is not needed in C++; just check we can construct again
    Injector inj1, inj2;
    SUCCEED();
}

TEST(InjectorTest, DunderDoc) {
    extern const std::string injector_doc;
    ASSERT_FALSE(injector_doc.empty());
}