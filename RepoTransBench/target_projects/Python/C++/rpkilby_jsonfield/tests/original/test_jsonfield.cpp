#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <string>
#include <map>
#include <vector>
#include <stdexcept>
#include <variant>
#include <optional>
#include <cmath>
#include <sstream>
#include <set>
#include <utility>
#include <typeinfo>

using json = nlohmann::json;

// Stubbed "model" classes as the real Django ORM logic relies on DB
struct JSONModel {
    int id;
    json json_val;
    static std::vector<JSONModel> db;
    static int id_seq;
    JSONModel(json j) : json_val(std::move(j)) { id = id_seq++; db.emplace_back(*this); }
    static JSONModel* get(int id) {
        for (auto& m : db) if (m.id == id) return &m; return nullptr;
    }
    static void reset() { db.clear(); id_seq = 1; }
};
std::vector<JSONModel> JSONModel::db;
int JSONModel::id_seq = 1;

TEST(JSONFieldTest, JsonFieldCreate) {
    JSONModel::reset();
    json obj = {{"item_1", "this is a json blah"}, {"blergh", "hey, hey, hey"}};
    JSONModel model(obj);
    auto* new_obj = JSONModel::get(model.id);
    ASSERT_TRUE(new_obj != nullptr);
    ASSERT_EQ(new_obj->json_val, obj);
}

TEST(JSONFieldTest, StringInJsonField) {
    JSONModel::reset();
    json obj = "blah blah";
    JSONModel model(obj);
    auto* new_obj = JSONModel::get(model.id);
    ASSERT_TRUE(new_obj != nullptr);
    ASSERT_EQ(new_obj->json_val, obj);
}

TEST(JSONFieldTest, FloatInJsonField) {
    JSONModel::reset();
    json obj = 1.23;
    JSONModel model(obj);
    auto* new_obj = JSONModel::get(model.id);
    ASSERT_TRUE(new_obj != nullptr);
    ASSERT_EQ(new_obj->json_val, obj);
}

TEST(JSONFieldTest, IntInJsonField) {
    JSONModel::reset();
    json obj = 1234567;
    JSONModel model(obj);
    auto* new_obj = JSONModel::get(model.id);
    ASSERT_TRUE(new_obj != nullptr);
    ASSERT_EQ(new_obj->json_val, obj);
}

TEST(JSONFieldTest, JsonList) {
    JSONModel::reset();
    json obj = json::array({"my", "list", "of", 1, "objs", json({{"hello", "there"}})});
    JSONModel model(obj);
    auto* new_obj = JSONModel::get(model.id);
    ASSERT_TRUE(new_obj != nullptr);
    ASSERT_EQ(new_obj->json_val, obj);
}

TEST(JSONFieldTest, EmptyObjects) {
    JSONModel::reset();
    std::vector<json> test_cases = {json::object(), json::array(), 0, "", false};
    for(const auto& obj : test_cases) {
        JSONModel model(obj);
        auto* new_obj = JSONModel::get(model.id);
        ASSERT_TRUE(new_obj != nullptr);
        ASSERT_EQ(model.json_val, obj);
        ASSERT_EQ(new_obj->json_val, obj);
    }
}

TEST(JSONFieldTest, IntegerInStringInJsonField) {
    JSONModel::reset();
    json obj = "123";
    JSONModel model(obj);
    auto* new_obj = JSONModel::get(model.id);
    ASSERT_TRUE(new_obj != nullptr);
    ASSERT_EQ(new_obj->json_val, obj);
}

TEST(JSONFieldTest, BooleanInStringInJsonField) {
    JSONModel::reset();
    json obj = "true";
    JSONModel model(obj);
    auto* new_obj = JSONModel::get(model.id);
    ASSERT_TRUE(new_obj != nullptr);
    ASSERT_EQ(new_obj->json_val, obj);
}