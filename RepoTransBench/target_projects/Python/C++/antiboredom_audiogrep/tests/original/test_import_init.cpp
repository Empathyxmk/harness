#include <gtest/gtest.h>
#include <dlfcn.h>
#include <string>
#include <vector>

// The C++ equivalent: test that module exposes expected symbols (weak test)
TEST(ImportInitTest, ExportsExpectedSymbols)
{
    void* handle = dlopen("libaudiogrep.so", RTLD_LAZY);
    ASSERT_NE(handle, nullptr) << "Could not load libaudiogrep.so";

    // Try dlsym for "convert_to_wav" and "transcribe"
    void* sym1 = dlsym(handle, "convert_to_wav");
    EXPECT_NE(sym1, nullptr) << "convert_to_wav symbol missing";

    void* sym2 = dlsym(handle, "transcribe");
    EXPECT_NE(sym2, nullptr) << "transcribe symbol missing";

    dlclose(handle);
}