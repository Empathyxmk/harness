#include <gtest/gtest.h>
#include "pythonflow/util.h"

TEST(Util, LazyImport) {
    auto os = pythonflow::lazy_import("os");
    auto path = os.attr("path");
    auto missing = pythonflow::lazy_import("some_missing_module");
    EXPECT_THROW(missing.attr("missing_attribute"), std::runtime_error);
}

TEST(Util, BatchIterable) {
    std::string iterable = "abcdefghijklmnopqrstuvwxyz";
    auto batches = pythonflow::batch_iterable(iterable, 4);
    ASSERT_EQ(batches.size(), 7);
    for (size_t i = 0; i < batches.size(); ++i) {
        ASSERT_EQ(std::string(iterable.begin() + (i * 4), iterable.begin() + std::min(iterable.size(), (i + 1) * 4)), batches[i]);
    }
}

TEST(Util, BatchIterableInvalidSize) {
    EXPECT_THROW(pythonflow::batch_iterable("", -1), std::invalid_argument);
}

// ... (Repeat for profiling, etc)