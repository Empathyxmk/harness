#include <gtest/gtest.h>
#include "mammoth/docx/uris.h"
#include "test_util/testing.h"

TEST(UrisTests, WhenPathDoesNotHaveLeadingSlashThenPathIsResolvedRelativeToBase) {
    // ... Test logic as above ...
}
TEST(UrisTests, WhenPathHasLeadingSlashThenBaseIsIgnored) {
    // ... Ditto ...
}