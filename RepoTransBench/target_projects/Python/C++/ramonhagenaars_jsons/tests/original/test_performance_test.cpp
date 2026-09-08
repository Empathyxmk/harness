#include <gtest/gtest.h>
#include <chrono>
#include <vector>
#include <string>
#include <sstream>
#include <iomanip>

// Simulating serialization logic for benchmarking

class C1 {
public:
    int x;
    std::string y;
    C1(int x_, const std::string& y_) : x(x_), y(y_) {}
};

class C2 {
public:
    std::vector<C1> list_of_c1;
    C2(const std::vector<C1>& l) : list_of_c1(l) {}
};

class C3 {
public:
    std::vector<C2> list_of_c2;
    C3(const std::vector<C2>& l) : list_of_c2(l) {}
};

// Simulated dump function (stub)
static inline std::string dump(const C3& c3, bool strict = false) {
    std::ostringstream oss;
    oss << "{";
    size_t n = c3.list_of_c2.size();
    for (size_t i = 0; i < n; ++i) {
        oss << "[";
        size_t m = c3.list_of_c2[i].list_of_c1.size();
        for (size_t j = 0; j < m; ++j) {
            oss << "{x:" << c3.list_of_c2[i].list_of_c1[j].x 
                << ",y:" << c3.list_of_c2[i].list_of_c1[j].y << "}";
            if (j != m - 1) oss << ",";
        }
        oss << "]";
        if (i != n - 1) oss << ",";
    }
    oss << "}";
    return oss.str();
}

class PerformanceFixture : public ::testing::Test {
protected:
    static C3* _c3_1;
    static C3* _c3_2;
    static C3* _c3_3;

    static C3* create_c3(size_t len1, size_t len2) {
        std::vector<C1> c1s;
        for (size_t x = 0; x < len1; ++x) {
            std::ostringstream oss;
            oss << x;
            c1s.emplace_back(static_cast<int>(x), oss.str());
        }
        std::vector<C2> c2s;
        for (size_t i = 0; i < len2; ++i) {
            c2s.emplace_back(c1s);
        }
        return new C3(c2s);
    }

    static void SetUpTestSuite() {
        _c3_1 = create_c3(100, 10);
        _c3_2 = create_c3(100, 100);
        _c3_3 = create_c3(100, 1000);
    }
    static void TearDownTestSuite() {
        delete _c3_1; delete _c3_2; delete _c3_3;
    }
};
C3* PerformanceFixture::_c3_1 = nullptr;
C3* PerformanceFixture::_c3_2 = nullptr;
C3* PerformanceFixture::_c3_3 = nullptr;

void do_test_dump(C3* c3_1, C3* c3_2, C3* c3_3, int time_limit, bool strict = false) {
    using namespace std::chrono;
    auto t1 = high_resolution_clock::now();
    dump(*c3_1, strict);
    auto t2 = high_resolution_clock::now();
    dump(*c3_2, strict);
    auto t3 = high_resolution_clock::now();
    dump(*c3_3, strict);
    auto t4 = high_resolution_clock::now();

    double delta1 = duration_cast<microseconds>(t2 - t1).count() / 1e6;
    double delta2 = duration_cast<microseconds>(t3 - t2).count() / 1e6;
    double delta3 = duration_cast<microseconds>(t4 - t3).count() / 1e6;

    EXPECT_LT(delta3, time_limit) << "The operation took " << delta3 << " seconds";

    double threshold = 0.1;
    double avg1 = delta1 / 10.0;
    double avg2 = delta2 / 100.0;
    double avg3 = delta3 / 1000.0;
    bool linear_scaling = std::abs(avg2 - avg1) < threshold && std::abs(avg3 - avg2) < threshold;
    EXPECT_TRUE(linear_scaling)
        << std::abs(avg2 - avg1) << ", " << std::abs(avg3 - avg2);
}

TEST_F(PerformanceFixture, test_dump) {
    do_test_dump(_c3_1, _c3_2, _c3_3, 16, false);
}

TEST_F(PerformanceFixture, test_dump_strict) {
    do_test_dump(_c3_1, _c3_2, _c3_3, 8, true);
}