#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <map>
#include <string>

// Dummy field implementation mimicking JSONField API
class JSONField {
public:
    JSONField(bool nullable = false) : nullable_(nullable) {}

    std::tuple<std::string, std::string, std::vector<std::string>, std::map<std::string, nlohmann::json>> deconstruct() const {
        std::string name = "JSONField";
        std::string path = "src.jsonfield.fields.JSONField";
        std::vector<std::string> args;
        std::map<std::string, nlohmann::json> kwargs;
        if (encoder_class_) kwargs["encoder_class"] = encoder_class_.value();
        if (decoder_class_) kwargs["decoder_class"] = decoder_class_.value();
        if (!dump_kwargs_.empty()) kwargs["dump_kwargs"] = dump_kwargs_;
        return {name, path, args, kwargs};
    }

    nlohmann::json get_prep_value(const nlohmann::json& val) const {
        if (val.is_null()) {
            return nullable_ ? nlohmann::json(nullptr) : "null";
        }
        return val.dump();
    }
    nlohmann::json from_db_value(const std::string& val, void*, void*, void*) const {
        if (val == "null" || val.empty()) return nullptr;
        return nlohmann::json::parse(val);
    }

    bool nullable_;
    std::optional<std::string> encoder_class_;
    std::optional<std::string> decoder_class_;
    nlohmann::json dump_kwargs_;
};

TEST(PublicFieldsTest, DeconstructNonDefaultKwargs) {
    JSONField f;
    f.encoder_class_ = "str";
    f.decoder_class_ = "str";
    f.dump_kwargs_ = nlohmann::json::object({{"indent", 4}});
    auto [name, path, args, kwargs] = f.deconstruct();
    ASSERT_EQ(kwargs["encoder_class"], "str");
    ASSERT_EQ(kwargs["decoder_class"], "str");
    ASSERT_EQ(kwargs["dump_kwargs"], nlohmann::json::object({{"indent", 4}}));
}

TEST(PublicFieldsTest, DeconstructDefaultKwargs) {
    JSONField f;
    auto [name, path, args, kwargs] = f.deconstruct();
    ASSERT_TRUE(kwargs.find("encoder_class") == kwargs.end());
    ASSERT_TRUE(kwargs.find("decoder_class") == kwargs.end());
    ASSERT_TRUE(kwargs.find("dump_kwargs") == kwargs.end());
}

TEST(PublicFieldsTest, GetPrepValueCanReturnNoneIfNull) {
    JSONField field(true);  // nullable=True
    auto val = field.get_prep_value(nullptr);
    ASSERT_TRUE(val.is_null());
}

TEST(PublicFieldsTest, GetPrepValueAlwaysJsonDumpsIfNotNull) {
    JSONField field(true);
    nlohmann::json input = {{"number", 33}, {"flag", false}};
    auto val = field.get_prep_value(input);
    ASSERT_EQ(val, input.dump());
}

TEST(PublicFieldsTest, FromDbValueLoadedTypes) {
    JSONField field;
    nlohmann::json expect = nlohmann::json::object({{"z", 1}});
    ASSERT_EQ(field.from_db_value("{\"z\":1}", nullptr, nullptr, nullptr), expect);
    ASSERT_TRUE(field.from_db_value("", nullptr, nullptr, nullptr).is_null());
}