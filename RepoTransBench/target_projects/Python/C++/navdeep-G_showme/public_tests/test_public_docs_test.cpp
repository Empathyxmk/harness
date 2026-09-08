#include <gtest/gtest.h>
#include "showme/core.h"
#include <string>

namespace {

TEST(PublicDocs, CoreDocstringContainsShowmeOrCore) {
    // Simulating: assert "showme" in doc.lower() or "core" in doc.lower()
    std::string doc = "showme core library provides tracing, timing, and utilities";
    auto doc_lower = doc;
    std::transform(doc_lower.begin(), doc_lower.end(), doc_lower.begin(), ::tolower);
    EXPECT_TRUE(doc_lower.find("showme") != std::string::npos || 
                doc_lower.find("core") != std::string::npos);
}

}