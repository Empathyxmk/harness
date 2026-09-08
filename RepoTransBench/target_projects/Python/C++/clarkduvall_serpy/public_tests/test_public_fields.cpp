#include <gtest/gtest.h>
#include "serpy/serializer.h"
#include "serpy/fields.h"
#include "obj.h"

TEST(TestPublicFields, StrField) {
    class TestSerializer : public serpy::Serializer {
    public:
        TestSerializer(const Obj& o) : serpy::Serializer(o) {
            addField("foo", new serpy::StrField(&Obj::foo));
        }
    };

    Obj o;
    o.foo = "differentstr";
    TestSerializer ex(o);
    auto data = ex.data();
    ASSERT_EQ(data["foo"], "differentstr");
}

TEST(TestPublicFields, IntField) {
    class TestSerializer : public serpy::Serializer {
    public:
        TestSerializer(const Obj& o) : serpy::Serializer(o) {
            addField("bar", new serpy::IntField(&Obj::bar));
        }
    };

    Obj o;
    o.bar = 100;
    TestSerializer ex(o);
    auto data = ex.data();
    ASSERT_EQ(data["bar"], 100);
}

TEST(TestPublicFields, MethodField) {
    class TestSerializer : public serpy::Serializer {
    public:
        TestSerializer(const Obj& o) : serpy::Serializer(o) {
            // MethodField: convert foo to upper-case string
            addField("special", new serpy::MethodField([](const Obj& obj){ 
                std::string s = obj.foo;
                std::transform(s.begin(), s.end(), s.begin(), ::toupper);
                return s;
            }));
        }
    };

    Obj o;
    o.foo = "public";
    TestSerializer ex(o);
    auto data = ex.data();
    ASSERT_EQ(data["special"], "PUBLIC");
}

TEST(TestPublicFields, MissingValueField) {
    class TestSerializer : public serpy::Serializer {
    public:
        TestSerializer(const Obj& o) : serpy::Serializer(o) {
            addField("bar", new serpy::MethodField([](const Obj& obj){
                // Return bar if present, else some sort of None-equivalent/null value
                return obj.has_bar ? obj.bar : -1;
            }));
        }
    };

    Obj o;
    o.has_bar = false;
    TestSerializer ex(o);
    auto data = ex.data();
    ASSERT_EQ(data["bar"], -1);
}