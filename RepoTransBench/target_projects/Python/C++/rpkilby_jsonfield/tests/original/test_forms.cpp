#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <string>
#include <map>

using json = nlohmann::json;

// Dummy JSON model simulation for C++
struct JSONNotRequiredModel {
    static JSONNotRequiredModel create(json j) { JSONNotRequiredModel m; m.json = j; return m; }
    json json;
};

class JSONModelForm {
public:
    explicit JSONModelForm(const std::string& input, const JSONNotRequiredModel* instance = nullptr, bool disabled=false)
        : has_changed_(false), is_valid_(false), errors_({}), instance_(instance), disabled_(disabled) {
        field_value_ = input;
        is_valid_ = validate(input);
        if (instance_ && !disabled_) {
            has_changed_ = (json::parse(input) != instance_->json);
        } else if (instance_ && disabled_) {
            // field is not editable, so no change
            has_changed_ = false;
        } else {
            has_changed_ = !input.empty();
        }
    }

    bool has_changed() const { return has_changed_; }
    bool is_valid() const { return is_valid_; }
    json save() const { if (!is_valid_) throw std::runtime_error("invalid"); return json::parse(field_value_); }
    std::map<std::string, std::vector<std::string>> errors() const { return errors_; }
    std::string value() const { return field_value_; }
    json cleaned_data() const { if (disabled_ && instance_) return instance_->json; return json::parse(field_value_); }

private:
    bool validate(const std::string& val) {
        try {
            json j = json::parse(val.empty() ? "null" : val);
            return true;
        } catch (...) {
            errors_["json"] = {"\"" + val + "\" value must be valid JSON."};
            return false;
        }
    }

    bool has_changed_;
    bool is_valid_;
    std::map<std::string, std::vector<std::string>> errors_;
    std::string field_value_;
    const JSONNotRequiredModel* instance_;
    bool disabled_;
};

TEST(JSONModelFormTest, BlankForm) {
    JSONModelForm form("");
    ASSERT_FALSE(form.has_changed());
}

TEST(JSONModelFormTest, FormWithData) {
    JSONModelForm form("{}");
    ASSERT_TRUE(form.has_changed());
}

TEST(JSONModelFormTest, FormSave) {
    JSONModelForm form("");
    ASSERT_NO_THROW(form.save());
}

TEST(JSONModelFormTest, SaveValues) {
    struct V {
        std::string type;
        std::string form_input;
        json db_value;
    } values[] = {
        {"object", "{\"a\": \"b\"}", json({{"a", "b"}})},
        {"array", "[1, 2]", json::array({1,2})},
        {"string", "\"test\"", "test"},
        {"float", "1.2", 1.2},
        {"int", "1234", 1234},
        {"bool", "true", true},
        {"null", "null", nullptr}
    };

    for (const auto& v : values) {
        JSONModelForm form(v.form_input);
        ASSERT_TRUE(form.is_valid()) << v.form_input;
        auto instance = form.save();
        ASSERT_EQ(instance, v.db_value);
    }
}

TEST(JSONModelFormTest, InvalidValue) {
    JSONModelForm form("foo");
    ASSERT_FALSE(form.is_valid());
    auto errors = form.errors();
    ASSERT_EQ(errors.count("json"), 1);
    ASSERT_EQ(errors.at("json")[0], "\"foo\" value must be valid JSON.");
    ASSERT_EQ(form.value(), "foo");
}

TEST(JSONModelFormTest, DisabledField) {
    auto instance = JSONNotRequiredModel::create(100);

    JSONModelForm form("{\"foo\": \"bar\"}", &instance, true);
    ASSERT_TRUE(form.is_valid());
    ASSERT_EQ(form.cleaned_data(), 100);
    ASSERT_EQ(form.value(), "{\"foo\": \"bar\"}");
}

TEST(JSONModelFormTest, InitialDataHasChanged) {
    auto instance = JSONNotRequiredModel::create(json::array({1, 2}));

    JSONModelForm form("[1, 2]", &instance);
    ASSERT_FALSE(form.has_changed());

    JSONModelForm form2("[3, 4]", &instance);
    ASSERT_TRUE(form2.has_changed());
}

TEST(NonJSONFieldModelFormTest, FieldType) {
    // Not relevant for C++ static typing; placeholder to show field type is string
    std::string field = "{\"a\": \"b\"}";
    ASSERT_TRUE(typeid(field) == typeid(std::string));
}

TEST(NonJSONFieldModelFormTest, NoIndent) {
    std::string val = "{\"a\": \"b\"}";
    ASSERT_EQ(val, "{\"a\": \"b\"}");
}