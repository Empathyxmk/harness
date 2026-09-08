#include <gtest/gtest.h>
#include "serpy/serializer.h"
#include "serpy/fields.h"
#include "obj.h"
#include <vector>
#include <string>

class IntegrationPublicSerializer : public serpy::Serializer {
public:
    IntegrationPublicSerializer(const Obj& o) : serpy::Serializer(o) {
        addField("a", new serpy::IntField(&Obj::a));
        addField("b", new serpy::StrField(&Obj::b));
        addField("c", new serpy::MethodField([](const Obj& obj){
            return obj.b + obj.b;
        }));
        addField("d", new serpy::MethodField([](const Obj& obj){
            return obj.has_d ? obj.d : -1;
        }));
    }
    // For "many" API, construct multiple
    IntegrationPublicSerializer(const std::vector<Obj>& objs) : serpy::Serializer(objs) {
        addField("a", new serpy::IntField(&Obj::a));
        addField("b", new serpy::StrField(&Obj::b));
        addField("c", new serpy::MethodField([](const Obj& obj){
            return obj.b + obj.b;
        }));
        addField("d", new serpy::MethodField([](const Obj& obj){
            return obj.has_d ? obj.d : -1;
        }));
    }
};

TEST(TestPublicIntegration, AllFields) {
    Obj obj;
    obj.a = 99;
    obj.b = "foo";
    obj.has_d = true;
    obj.d = 255;
    IntegrationPublicSerializer s(obj);
    auto data = s.data();
    ASSERT_EQ(data["a"], 99);
    ASSERT_EQ(data["b"], "foo");
    ASSERT_EQ(data["c"], "foofoo");
    ASSERT_EQ(data["d"], 255);
}

TEST(TestPublicIntegration, MissingField) {
    Obj obj;
    obj.a = 44;
    obj.b = "echo";
    obj.has_d = false;
    IntegrationPublicSerializer s(obj);
    auto data = s.data();
    ASSERT_EQ(data["a"], 44);
    ASSERT_EQ(data["b"], "echo");
    ASSERT_EQ(data["c"], "echoecho");
    ASSERT_EQ(data["d"], -1);
}

TEST(TestPublicIntegration, ListMany) {
    Obj o1, o2;
    o1.a = 8; o1.b = "a"; o1.has_d = false;
    o2.a = 9; o2.b = "Xx"; o2.has_d = true; o2.d = 777;

    std::vector<Obj> objs = {o1, o2};
    IntegrationPublicSerializer serializer(objs);
    auto res = serializer.data_vector();
    ASSERT_EQ(res.size(), 2);
    ASSERT_EQ(res[0]["a"], 8);
    ASSERT_EQ(res[0]["b"], "a");
    ASSERT_EQ(res[0]["c"], "aa");
    ASSERT_EQ(res[0]["d"], -1);
    ASSERT_EQ(res[1]["a"], 9);
    ASSERT_EQ(res[1]["b"], "Xx");
    ASSERT_EQ(res[1]["c"], "XxXx");
    ASSERT_EQ(res[1]["d"], 777);
}