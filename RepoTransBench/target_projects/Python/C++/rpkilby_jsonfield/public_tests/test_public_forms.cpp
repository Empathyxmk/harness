#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <string>
#include <optional>
#include <map>

// Dummy form to mimic simple form validation
class JSONFormField {
public:
    JSONFormField(bool required = false) : required_(required) {}

    bool is_valid(const std::string& val) {
        try {
            nlohmann::json parsed = val.empty() ? nullptr : nlohmann::json::parse(val);
            cleaned_ = parsed.is_null() ? nullptr : parsed;
            return true;
        } catch (...) {
            error_ = true;
            return false;
        }
    }
    nlohmann::json cleaned_data() const { return cleaned_; }
    bool error_ = false;
    bool required_;
private:
    nlohmann::json cleaned_;
};

class DummyForm {
public:
    DummyForm(const std::map<std::string, std::string>& data) {
        std::string payload = "";
        auto it = data.find("payload");
        if (it != data.end()) payload = it->second;

        if (!payload.empty() && (payload.front() == '{' || payload.front() == '[' || payload.front() == '\"'))
            valid_ = field_.is_valid(payload);
        else if (!payload.empty())
            valid_ = false, field_.error_ = true;
        else
            valid_ = field_.is_valid(payload);
    }
    bool is_valid() const { return valid_ && !field_.error_; }
    nlohmann::json cleaned_data() const { return field_.cleaned_data(); }
    bool has_error() const { return field_.error_; }
private:
    JSONFormField field_;
    bool valid_ = false;
};

TEST(PublicFormsTest, BlankForm) {
    DummyForm form({});
    ASSERT_TRUE(form.is_valid());
    ASSERT_TRUE(form.cleaned_data().is_null());
}

TEST(PublicFormsTest, ValidJsonFormValue) {
    DummyForm form({{"payload", "{\"species\": \"cat\", \"legs\": 4}"}});
    ASSERT_TRUE(form.is_valid());
    auto cd = form.cleaned_data();
    ASSERT_EQ(cd["species"], "cat");
    ASSERT_EQ(cd["legs"], 4);
}

TEST(PublicFormsTest, InvalidJsonFormValue) {
    DummyForm form({{"payload", "{\"species\": unquoted}"}});
    ASSERT_FALSE(form.is_valid());
    ASSERT_TRUE(form.has_error());
}

TEST(PublicFormsTest, PythonObjInput) {
    // Simulate passing a Python dict directly: in C++, just use JSON object directly
    DummyForm form({{"payload", nlohmann::json({{"key", {1, 2}}}).dump()}});
    ASSERT_TRUE(form.is_valid());
    auto cd = form.cleaned_data();
    ASSERT_EQ(cd["key"][0], 1);
    ASSERT_EQ(cd["key"][1], 2);
}