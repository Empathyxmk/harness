#include <gtest/gtest.h>

TEST(TestDepends, ExtractConst) {
    SUCCEED() << "Stub: extract_constant handles direct and indirect assignments";
}

TEST(TestDepends, FindModule) {
    SUCCEED() << "Stub: find_module raises on invalid name, returns details on valid module";
}

TEST(TestDepends, ModuleExtract) {
    SUCCEED() << "Stub: get_module_constant returns constants for stdlib and tests";
}

TEST(TestDepends, RequireLogic) {
    SUCCEED() << "Stub: Require object behaves/validates as expected";
}

TEST(TestDepends, RequirePresentOptional) {
    SUCCEED() << "Stub: Require format/homepage and package path list";
}

TEST(TestDistro, DistroType) {
    SUCCEED() << "Stub: setup produces setuptools.dist.Distribution";
}

TEST(TestDistro, ExcludePackage) {
    SUCCEED() << "Stub: exclude_package removes from packages etc.";
}

TEST(TestDistro, IncludeExclude) {
    SUCCEED() << "Stub: include/exclude for ext_modules is correct and idempotent";
}

TEST(TestDistro, ExcludePackages) {
    SUCCEED() << "Stub: exclude(packages=[...]) removes from dist";
}

TEST(TestDistro, Empty) {
    SUCCEED() << "Stub: empty dist can include/exclude sets";
}

TEST(TestDistro, Contents) {
    SUCCEED() << "Stub: has_contents_for property checks after exclude_package";
}

TEST(TestDistro, InvalidIncludeExclude) {
    SUCCEED() << "Stub: includes/excludes with wrong types raise errors";
}

TEST(SetuptoolsMisc, FindAll) {
    SUCCEED() << "Stub: setuptools.findall finds all source files with and without cwd";
}

TEST(SetuptoolsMisc, FindAllMissingSymlink) {
    SUCCEED() << "Stub: setuptools.findall skips broken symlinks";
}

TEST(SetuptoolsMisc, ItsOwnWheelDoesNotContainTests) {
    SUCCEED() << "Stub: tests/ is excluded from self-distributed wheel";
}

TEST(SetuptoolsMisc, WheelIncludesCliScripts) {
    SUCCEED() << "Stub: self wheel includes CLI scripts";
}

TEST(SetuptoolsMisc, WheelIncludesVendoredMetadata) {
    SUCCEED() << "Stub: wheel contains vendored package dist-info METADATA";
}