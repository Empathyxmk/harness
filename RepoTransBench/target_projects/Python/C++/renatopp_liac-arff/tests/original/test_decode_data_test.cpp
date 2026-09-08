#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "arff_cpp.h"

class DecodeDataTest : public ::testing::Test {
protected:
    std::vector<std::vector<std::string>> _load(const std::string& data, int n_attribs = 1) {
        std::string attribs;
        for (int i = 0; i < n_attribs; ++i) {
            attribs += "@ATTRIBUTE x" + std::to_string(i) + " STRING\n";
        }
        std::string txt =
            "@RELATION testing\n\n" + attribs + "\n@DATA\n" + data + "\n";
        return ARFF_load(txt).data_dense;
    }

    void assertLoadsAs(const std::string& data, const std::vector<std::vector<std::string>>& expected, int n_attribs = 1) {
        auto result = _load(data, n_attribs);
        EXPECT_EQ(result, expected);
    }
};

TEST_F(DecodeDataTest, test_quotes) {
    assertLoadsAs("'ENACT.NOGOPMAJ,2017'", {{"ENACT.NOGOPMAJ,2017"}});
    assertLoadsAs("\"ENACT.NOGOPMAJ,2017\"", {{"ENACT.NOGOPMAJ,2017"}});
    assertLoadsAs(" 'A','B' , '\"','C,D' ", {{"A","B","\"","C,D"}}, 4);
}
// ... [CUT: All other functional and error tests; keep error asserts as EXPECT_THROW]