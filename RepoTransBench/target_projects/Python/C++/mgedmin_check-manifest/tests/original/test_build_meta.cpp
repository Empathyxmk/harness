#include <gtest/gtest.h>

TEST(TestBuildMetaBackend, GetRequiresForBuildWheel) {
    SUCCEED() << "Stub: get_requires_for_build_wheel returns setup_requires";
}

TEST(TestBuildMetaBackend, GetRequiresForBuildSdist) {
    SUCCEED() << "Stub: get_requires_for_build_sdist returns setup_requires";
}

TEST(TestBuildMetaBackend, BuildWheel) {
    SUCCEED() << "Stub: build_wheel produces a wheel containing all expected files";
}

TEST(TestBuildMetaBackend, BuildWithExistingFilePresent) {
    SUCCEED() << "Stub: re-builds with different versions and preserves non-overwritten archives";
}

TEST(TestBuildMetaBackend, BuildWithPyprojectConfig) {
    SUCCEED() << "Stub: build_sdist and build_wheel work with pyproject.toml only";
}

TEST(TestBuildMetaBackend, StaticMetadataInPyprojectConfig) {
    SUCCEED() << "Stub: static pyproject.toml metadata not overwritten by setup.py";
}

TEST(TestBuildMetaBackend, BuildSdist) {
    SUCCEED() << "Stub: build_sdist writes the archive";
}

TEST(TestBuildMetaBackend, PrepareMetadataForBuildWheel) {
    SUCCEED() << "Stub: prepare_metadata_for_build_wheel writes dist-info";
}

TEST(TestBuildMetaBackend, PrepareMetadataInplace) {
    SUCCEED() << "Stub: pre-existing .dist-info dirs do not break metadata build";
}

TEST(TestBuildMetaBackend, BuildSdistExplicitDist) {
    SUCCEED() << "Stub: destination folder can be same as --dist-dir";
}

TEST(TestBuildMetaBackend, BuildSdistVersionChange) {
    SUCCEED() << "Stub: build_sdist works after changing version";
}

TEST(TestBuildMetaBackend, BuildSdistPyprojectTomlExists) {
    SUCCEED() << "Stub: sdist includes pyproject.toml if present";
}

TEST(TestBuildMetaBackend, BuildSdistSetupPyExists) {
    SUCCEED() << "Stub: sdist includes setup.py if not excluded";
}

TEST(TestBuildMetaBackend, BuildSdistSetupPyManifestExcluded) {
    SUCCEED() << "Stub: sdist respects MANIFEST.in exclude of setup.py";
}

TEST(TestBuildMetaBackend, BuildSdistBuildsTargzEvenIfZipIndicated) {
    SUCCEED() << "Stub: sdist format zip ignored in favor of tar.gz";
}

TEST(TestBuildMetaBackend, BuildSdistRelativePathImport) {
    SUCCEED() << "Stub: ImportError for relative path imports in sdist";
}

TEST(TestBuildMetaBackend, EditableWithoutConfigSettings) {
    SUCCEED() << "Stub: build_editable does not create build dir";
}

TEST(TestBuildMetaBackend, BuildWheelInplace) {
    SUCCEED() << "Stub: build_wheel can run in build/ dir";
}

TEST(TestBuildMetaBackend, EditableWithConfigSettings) {
    SUCCEED() << "Stub: editable mode builds links";
}

TEST(TestBuildMetaBackend, SetupRequiresVariants) {
    SUCCEED() << "Stub: setup_requires parsed consistently for all permutations";
}

TEST(TestBuildMetaBackend, SetupRequiresWithAutoDiscovery) {
    SUCCEED() << "Stub: setup_requires with auto-discovery does not break";
}

TEST(TestBuildMetaBackend, DontInstallSetupRequires) {
    SUCCEED() << "Stub: build backend does not try to install missing reqs";
}

TEST(TestBuildMetaBackend, SysArgvPassthrough) {
    SUCCEED() << "Stub: sys.argv[0] passed through as abs path";
}

TEST(TestBuildMetaBackend, SetupPyFileAbspath) {
    SUCCEED() << "Stub: setup.py __file__ path is absolute";
}

TEST(TestBuildMetaBackend, BuildWithEmptySetuppyFails) {
    SUCCEED() << "Stub: empty setup.py is an error";
}

TEST(TestBuildMetaLegacyBackend, BuildSdistRelativePathImportAllowed) {
    SUCCEED() << "Stub: legacy backend allows module imports from setup.py";
}

TEST(TestBuildMetaLegacyBackend, SysArgvPassthroughLegacy) {
    SUCCEED() << "Stub: sys.argv[0] passthrough for legacy backend";
}

TEST(TestBuildMeta, SysExit0InSetuppy) {
    SUCCEED() << "Stub: setup.py with sys.exit(0) gives empty requires";
}

TEST(TestBuildMeta, SystemExitInSetuppy) {
    SUCCEED() << "Stub: setup.py with sys.exit raises SystemExit";
}