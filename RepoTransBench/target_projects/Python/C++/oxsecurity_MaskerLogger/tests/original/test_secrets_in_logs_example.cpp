#include <gtest/gtest.h>
#include "../../src/secrets_in_logs_example.h"

TEST(TestImportSecretsInLogsExample, ImportAndMain) {
    // Call main() function; expect no exception thrown
    ASSERT_NO_THROW(maskerlogger::secrets_in_logs_example::main());
}

TEST(TestImportSecretsInLogsExample, CmdMainGuard) {
    // Simulate running with __main__
    // Not directly relevant in C++, but we can call the equivalent
    ASSERT_NO_THROW(maskerlogger::secrets_in_logs_example::main());
}

TEST(TestImportSecretsInLogsExample, LogSensitiveRuns) {
    // Test that log_sensitive runs and doesn't crash
    ASSERT_NO_THROW(maskerlogger::secrets_in_logs_example::log_sensitive());
}