#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include "linkedin2username.h"

struct PubNameTestCase {
    std::string input_name;
    std::map<std::string, std::string> expected;
};

class PublicNameMutatorParamTest : public testing::TestWithParam<PubNameTestCase> {};

TEST_P(PublicNameMutatorParamTest, CleanAndSplitNamePublic) {
    auto param = GetParam();
    NameMutator nm(param.input_name);
    EXPECT_EQ(nm.name, param.expected);
}

INSTANTIATE_TEST_SUITE_P(
    PublicNameMutatorParamTests,
    PublicNameMutatorParamTest,
    testing::Values(
        PubNameTestCase{"Sam Lee", {{"first", "sam"}, {"last", "lee"}, {"second", ""}}},
        PubNameTestCase{"Ms. Eva O'Brien", {{"first", "eva"}, {"last", "obrien"}, {"second", ""}}},
        PubNameTestCase{"Prof. Łukasz Nowak (PhD)", {{"first", "lukasz"}, {"last", "nowak"}, {"second", ""}}},
        PubNameTestCase{"María-José Carreño", {{"first", "maria"}, {"last", "carreno"}, {"second", ""}}},
        PubNameTestCase{"Chris (CEO) Smithers", {{"first", "chris"}, {"last", "smithers"}, {"second", ""}}}
    )
);