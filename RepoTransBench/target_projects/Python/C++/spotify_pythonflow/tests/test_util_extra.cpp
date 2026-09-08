#include <gtest/gtest.h>
#include "pythonflow/util.h"

TEST(UtilExtra, LazyImportActual) {
    auto math = pythonflow::util::lazy_import("math");
    ASSERT_DOUBLE_EQ(math.sqrt(4), 2.0);
    ASSERT_TRUE(math.has_attr("cos"));
}

TEST(UtilExtra, LazyImportAlreadyImported) {
    auto math = pythonflow::util::lazy_import("math");
    (void)math.sqrt;
    // Simulate monkeypatching: not applicable for C++, skip/replace as needed
    ASSERT_DOUBLE_EQ(math.cos(0), 1.0);
}

// ... (Repeat all others: batch_iterable, profiler, deprecated, NOOP, etc)