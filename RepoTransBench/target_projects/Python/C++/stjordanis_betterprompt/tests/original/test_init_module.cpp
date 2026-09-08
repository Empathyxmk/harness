#include <gtest/gtest.h>
#include "betterprompt.h"

TEST(TestInitModule, AllExports) {
    for (const auto& name : betterprompt::get_all_exports()) {
        // We'll check by symbol names
        if (name == "get_from_dict_or_env") { SUCCEED(); continue; }
        if (name == "DummyOpenAICompletion") { SUCCEED(); continue; }
        if (name == "call_openai") { SUCCEED(); continue; }
        if (name == "calculate_perplexity") { SUCCEED(); continue; }
        if (name == "openai") { SUCCEED(); continue; }
        ADD_FAILURE() << "Unknown export: " << name;
    }
}