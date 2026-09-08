#include <gtest/gtest.h>
#include <dlfcn.h>

TEST(PublicImportTest, ImportsWork)
{
    void* handle = dlopen("libaudiogrep.so", RTLD_LAZY);
    ASSERT_NE(handle, nullptr) << "Could not load libaudiogrep.so";
    // Weak import check: library file must be present
    Dl_info info;
    ASSERT_TRUE(dladdr((void*)handle, &info));
    dlclose(handle);
}