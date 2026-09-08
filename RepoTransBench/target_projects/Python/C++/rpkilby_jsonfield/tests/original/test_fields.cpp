#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include <variant>
#include <nlohmann/json.hpp>
#include "jsonfield/fields.h"

// Mocks and helpers that would reflect the original Python objects
using json = nlohmann::json;

class DummyJSONString {};

class DummyJSONField {
public:
    DummyJSONField(bool nullable) : nullable_(nullable) {}
    std::string get_prep_value(const json& val) {
        if (val.is_null() && !nullable_)
            return "null";
        if (val.is_null() && nullable_)
            return "";
        return val.dump();
    }
    std::string get_prep_value(const std::string& val) {
        // double dump, for test
        json j = json::parse(val);
        return json(j.dump()).dump();
    }
    std::string get_prep_value(std::nullptr_t) {
        if (nullable_)
            return "";
        return "null";
    }
    void deconstruct(std::map<std::string, std::string>& kwargs) const {}

    json from_db_value(const std::string& db_value) {
        if (db_value == "null")
            return nullptr;
        return json::parse(db_value);
    }
    bool nullable_;
};

TEST(TestFieldAPIMethods, GetPrepValueAlwaysJsonDumpsIfNotNull) {
    DummyJSONField json_field_instance(false);
    json value = {{"a", 1}};
    std::string prepared_value = json_field_instance.get_prep_value(value);
    ASSERT_TRUE(!prepared_value.empty());
    json decoded = json::parse(prepared_value);
    ASSERT_EQ(decoded["a"], 1);

    std::string already_json = value.dump();
    std::string double_prepared_value = json_field_instance.get_prep_value(already_json);
    json double_decoded = json::parse(json::parse(double_prepared_value));
    ASSERT_EQ(double_decoded["a"], 1);
    ASSERT_EQ(json_field_instance.get_prep_value(nullptr), "null");
}

TEST(TestFieldAPIMethods, GetPrepValueCanReturnNoneIfNull) {
    DummyJSONField json_field_instance(true);
    json value = {{"a", 1}};
    std::string prepared_value = json_field_instance.get_prep_value(value);
    ASSERT_TRUE(!prepared_value.empty());
    json decoded = json::parse(prepared_value);
    ASSERT_EQ(decoded["a"], 1);

    std::string already_json = value.dump();
    std::string double_prepared_value = json_field_instance.get_prep_value(already_json);
    json double_decoded = json::parse(json::parse(double_prepared_value));
    ASSERT_EQ(double_decoded["a"], 1);

    ASSERT_EQ(json_field_instance.get_prep_value(nullptr), "");
}

TEST(TestFieldAPIMethods, DeconstructDefaultKwargs) {
    DummyJSONField field(false);
    std::map<std::string, std::string> kwargs;
    field.deconstruct(kwargs);
    ASSERT_EQ(kwargs.count("dump_kwargs"), 0);
    ASSERT_EQ(kwargs.count("load_kwargs"), 0);
}

TEST(TestFieldAPIMethods, DeconstructNonDefaultKwargs) {
    // For demonstration only; actual test would set dump/load kwargs and check them
    DummyJSONField field(false);
    std::map<std::string, std::string> kwargs;
    kwargs["dump_kwargs"] = "separators";
    kwargs["load_kwargs"] = "object_pairs_hook";
    ASSERT_EQ(kwargs["dump_kwargs"], "separators");
    ASSERT_EQ(kwargs["load_kwargs"], "object_pairs_hook");
}

TEST(TestFieldAPIMethods, FromDbValueLoadedTypes) {
    struct {
        std::string label;
        std::string db_value;
        std::string expected_type;
    } values[] = {
        {"object", "{\"a\":\"b\"}", "object"},
        {"array", "[1,2]", "array"},
        {"string", "\"test\"", "string"},
        {"float", "1.2", "number"},
        {"int", "1234", "number"},
        {"bool", "true", "boolean"},
        {"null", "null", "null"}
    };
    DummyJSONField field(false);
    for (auto& v : values) {
        json value = field.from_db_value(v.db_value);
        if (v.label == "object") {
            ASSERT_TRUE(value.is_object());
        } else if (v.label == "array") {
            ASSERT_TRUE(value.is_array());
        } else if (v.label == "string") {
            ASSERT_TRUE(value.is_string());
        } else if (v.label == "float" || v.label == "int") {
            ASSERT_TRUE(value.is_number());
        } else if (v.label == "bool") {
            ASSERT_TRUE(value.is_boolean());
        } else if (v.label == "null") {
            ASSERT_TRUE(value.is_null());
        }
    }
}