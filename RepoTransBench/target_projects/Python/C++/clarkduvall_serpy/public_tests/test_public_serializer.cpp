#include <gtest/gtest.h>
#include "serpy/serializer.h"
#include "serpy/fields.h"
#include "obj.h"
#include <string>
#include <vector>

class AnotherPublicSerializer : public serpy::Serializer {
public:
    AnotherPublicSerializer(const Obj& o) : serpy::Serializer(o) {
        addField("name", new serpy::StrField(&Obj::name));
        addField("value", new serpy::IntField(&Obj::value));
    }
    AnotherPublicSerializer(const std::vector<Obj>& objs) : serpy::Serializer(objs) {
        addField("name", new serpy::StrField(&Obj::name));
        addField("value", new serpy::IntField(&Obj::value));
    }
};

class MethodPublicSerializer : public serpy::Serializer {
public:
    MethodPublicSerializer(const Obj& o) : serpy::Serializer(o) {
        addField("foo", new serpy::StrField(&Obj::foo));
        addField("double", new serpy::MethodField([](const Obj& obj){
            return obj.foo + obj.foo;
        }));
    }
    MethodPublicSerializer(const std::vector<Obj>& objs) : serpy::Serializer(objs) {
        addField("foo", new serpy::StrField(&Obj::foo));
        addField("double", new serpy::MethodField([](const Obj& obj){
            return obj.foo + obj.foo;
        }));
    }
};

TEST(TestPublicSerializer, SerializerBasic) {
    Obj o;
    o.name = "other";
    o.value = 13;
    AnotherPublicSerializer ser(o);
    auto data = ser.data();
    ASSERT_EQ(data["name"], "other");
    ASSERT_EQ(data["value"], 13);
}

TEST(TestPublicSerializer, SerializerMany) {
    Obj o1, o2;
    o1.name = "x"; o1.value = 2;
    o2.name = "y"; o2.value = 7;
    std::vector<Obj> objs = {o1, o2};
    AnotherPublicSerializer serializer(objs);
    auto res = serializer.data_vector();
    ASSERT_EQ(res.size(), 2);
    ASSERT_EQ(res[0]["name"], "x");
    ASSERT_EQ(res[0]["value"], 2);
    ASSERT_EQ(res[1]["name"], "y");
    ASSERT_EQ(res[1]["value"], 7);
}

TEST(TestPublicSerializer, MethodSerializer) {
    Obj o;
    o.foo = "hello";
    MethodPublicSerializer ser(o);
    auto data = ser.data();
    ASSERT_EQ(data["foo"], "hello");
    ASSERT_EQ(data["double"], "hellohello");
}

TEST(TestPublicSerializer, MethodSerializerMany) {
    Obj o1, o2;
    o1.foo = "abc"; o2.foo = "de";
    std::vector<Obj> objs = {o1, o2};
    MethodPublicSerializer serializer(objs);
    auto res = serializer.data_vector();
    ASSERT_EQ(res.size(), 2);
    ASSERT_EQ(res[0]["foo"], "abc");
    ASSERT_EQ(res[0]["double"], "abcabc");
    ASSERT_EQ(res[1]["foo"], "de");
    ASSERT_EQ(res[1]["double"], "dede");
}