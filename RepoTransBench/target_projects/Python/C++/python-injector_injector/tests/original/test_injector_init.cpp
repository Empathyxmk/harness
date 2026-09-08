#include <gtest/gtest.h>
#include "injector.h"
#include <string>

using namespace injector_ns;

TEST(InjectorInitTest, DunderPackage) {
    // Should have package info
    extern const std::string injector_package;
    ASSERT_FALSE(injector_package.empty());
}

TEST(InjectorInitTest, DunderFile) {
    extern const std::string injector_file;
    ASSERT_FALSE(injector_file.empty());
}

TEST(InjectorInitTest, AttributesListing) {
    // List of attributes (simulate via functions/classes in namespace)
    std::string dummy_class = Injector().repr();
    ASSERT_FALSE(dummy_class.empty()); // Asserting that dir() would give something non-empty
}

TEST(InjectorInitTest, ReprIncludesInjector) {
    Injector inj;
    ASSERT_NE(inj.repr().find("injector"), std::string::npos);
}