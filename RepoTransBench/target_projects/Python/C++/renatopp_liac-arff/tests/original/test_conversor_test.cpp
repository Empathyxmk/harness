#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>
#include "arff_cpp.h" // Hypothetical C++ port for ARFF; define matching interface

// Helper class to match the Python test conversational structure.
class BaseTestDecodeConversor {
protected:
    virtual std::function<ARFFValue(const std::string&)> get_conversor(const std::string& type, const std::vector<std::string>* values = nullptr) = 0;
    bool use_sparse = false;

    std::function<ARFFObject(const std::string&)> _get_arff_loader(const std::string& return_type, std::string type, const std::vector<std::string>* values = nullptr) {
        bool encode_nominal = (type == "ENCODED_NOMINAL");
        if (values != nullptr) {
            type = "{" + join(*values, ",") + "}";
        }
        bool is_sparse = use_sparse;
        return [return_type, type, encode_nominal, is_sparse](const std::string& value) {
            std::string data;
            if (is_sparse) {
                data = "{ 0 " + value + " }";
            } else {
                data = value + ",0";
            }
            std::string txt =
                "@RELATION testing\n\n"
                "@ATTRIBUTE name " + type + "\n"
                "@ATTRIBUTE dummy REAL\n"
                "\n"
                "@DATA\n" + 
                data + "\n";
            return ARFF_load(txt, return_type, encode_nominal);
        };
    }

    // Helper for join
    static std::string join(const std::vector<std::string>& v, const std::string& delim) {
        std::string s;
        for (size_t i = 0; i < v.size(); ++i) {
            s += v[i];
            if (i < v.size() - 1) s += delim;
        }
        return s;
    }
};

// Dense variant
class TestDecodeConversorDense 
    : public BaseTestDecodeConversor, public ::testing::Test {
protected:
    void SetUp() override { use_sparse = false; }
    std::function<ARFFValue(const std::string&)> get_conversor(const std::string& type, const std::vector<std::string>* values = nullptr) override {
        auto load = _get_arff_loader("DENSE", type, values);
        return [load](const std::string& value) -> ARFFValue {
            auto obj = load(value);
            const auto& data = obj.data_dense;
            EXPECT_EQ(data.size(), 1);
            EXPECT_EQ(data[0].size(), 2);
            EXPECT_EQ(data[0][1], ARFFValue(0.0));
            return data[0][0];
        };
    }
};
// Sparse-dense variant just sets use_sparse true, otherwise same logic
class TestDecodeConversorSparseDense : public TestDecodeConversorDense {
    void SetUp() override { use_sparse = true; }
};

// COO variant
class TestDecodeConversorCOO : public BaseTestDecodeConversor, public ::testing::Test {
protected:
    void SetUp() override { use_sparse = true; }
    std::function<ARFFValue(const std::string&)> get_conversor(const std::string& type, const std::vector<std::string>* values = nullptr) override {
        auto load = _get_arff_loader("COO", type, values);
        return [load](const std::string& value) -> ARFFValue {
            auto obj = load(value);
            const auto& data = obj.data_coo;
            const auto& row = obj.row, &col = obj.col;
            EXPECT_EQ(data.size(), 1);
            EXPECT_EQ(row.size(), 1);
            EXPECT_EQ(col.size(), 1);
            EXPECT_EQ(row[0], 0);
            EXPECT_EQ(col[0], 0);
            return data[0];
        };
    }
};

// LOD variant
class TestDecodeConversorLOD : public BaseTestDecodeConversor, public ::testing::Test {
protected:
    void SetUp() override { use_sparse = true; }
    std::function<ARFFValue(const std::string& type, const std::vector<std::string>* values = nullptr) override {
        auto load = _get_arff_loader("LOD", type, values);
        return [load](const std::string& value) -> ARFFValue {
            auto obj = load(value);
            const auto& data = obj.data_lod;
            EXPECT_EQ(data.size(), 1);
            EXPECT_TRUE(data[0].is_map());
            EXPECT_EQ(data[0].size(), (size_t)1);
            return data[0].at(0);
        };
    }
};

TEST_F(TestDecodeConversorDense, test_real) {
    auto conversor = get_conversor("REAL");

    // From Integer
    std::string fixture = "45";
    auto result = conversor(fixture);
    EXPECT_TRUE(std::holds_alternative<double>(result.value));
    EXPECT_DOUBLE_EQ(std::get<double>(result.value), 45.0);

    // From Float
    fixture = "45.13233322";
    result = conversor(fixture);
    EXPECT_TRUE(std::holds_alternative<double>(result.value));
    EXPECT_DOUBLE_EQ(std::get<double>(result.value), 45.13233322);
}

TEST_F(TestDecodeConversorDense, test_numeric) {
    auto conversor = get_conversor("NUMERIC");
    std::string fixture = "45";
    auto result = conversor(fixture);
    EXPECT_TRUE(std::holds_alternative<double>(result.value));
    EXPECT_DOUBLE_EQ(std::get<double>(result.value), 45.0);

    fixture = "45.13233322";
    result = conversor(fixture);
    EXPECT_TRUE(std::holds_alternative<double>(result.value));
    EXPECT_DOUBLE_EQ(std::get<double>(result.value), 45.13233322);
}

// ... [CUT: Similar code for test_integer, test_string, test_nominal, etc - keep identical assertion logic from Python]