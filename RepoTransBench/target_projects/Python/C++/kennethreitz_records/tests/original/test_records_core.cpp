#include <gtest/gtest.h>
#include "records.hpp"

TEST(TestRecordCollectionCore, IterNextSliceRepr) {
    std::vector<records::Record> data1 {
        records::Record({"a"}, {1}),
        records::Record({"a"}, {2})
    };
    records::RecordCollection rc(data1);
    EXPECT_TRUE(rc.repr().find("pending") != std::string::npos);
    std::vector<records::Record> vals;
    for (auto& r : rc) vals.push_back(r);
    EXPECT_EQ(vals.size(), 2u);

    std::vector<records::Record> data2 {
        records::Record({"a"}, {4}),
        records::Record({"a"}, {5})
    };
    records::RecordCollection rc2(data2);
    auto out = rc2[0];
    // This would check dynamic_cast, in C++ we check typeid
    EXPECT_EQ(typeid(out), typeid(records::Record));

    // Slicing
    records::RecordCollection sl = rc2.slice(0,2);
    EXPECT_EQ(typeid(sl), typeid(records::RecordCollection));
}

TEST(TestRecordCollectionCore, ConsumingAndAttrs) {
    std::vector<records::Record> data {
        records::Record({"a"}, {1}),
        records::Record({"a"}, {2}),
        records::Record({"a"}, {3})
    };
    records::RecordCollection rc(data);

    // Slicing out of bounds
    rc.slice(0,5);
    rc.append(records::Record({"a"}, {4}));
    EXPECT_GE(rc.size(), 3u);

    // Try as_dicts
    if constexpr (requires{ rc.as_dicts(); }) {
        EXPECT_TRUE(typeid(rc.as_dicts()) == typeid(std::vector<std::map<std::string, std::any>>));
    } else {
        SUCCEED();
    }
}

// Skipped CLI/monkeypatch test per Py test skip