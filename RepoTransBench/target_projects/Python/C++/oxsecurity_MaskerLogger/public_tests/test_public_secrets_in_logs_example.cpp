#include <gtest/gtest.h>
#include "../src/masker_formatter.h"

using maskerlogger::MaskerFormatter;

void log_sensitive_public() {
    // Simulate a logging system; in real usage would be to log
    MaskerFormatter formatter("%(message)s");
    std::vector<std::string> messages = {
        "secret field: thisshouldberedacted321 must be hidden",
        "nondescript info log",
        "skip me"
    };
    for (const auto& msg : messages) {
        // For demonstration, apply mask unless "skip me"
        if (msg == "skip me") {
            // Simulate extra {"apply_mask": false}
            struct Rec { std::string msg; bool apply_mask = false; Rec(std::string m):msg(m){} };
            Rec r(msg);
            formatter.format(r); // Should just return message unaltered
        } else {
            struct Rec { std::string msg; bool apply_mask = true; Rec(std::string m):msg(m){} };
            Rec r(msg);
            formatter.format(r); // Should mask if necessary
        }
    }
}

TEST(TestSecretsInLogsExamplePublic, LogSensitivePublicRuns) {
    // Ensure it runs
    ASSERT_NO_THROW(log_sensitive_public());
}