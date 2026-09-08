#include <gtest/gtest.h>
#include "obj.h"
#include "serpy/fields.h"
#include "serpy/serializer.h"

class TestFields : public ::testing::Test {};

TEST_F(TestFields, StrField) {
    class Example : public serpy::Serializer {
    public:
        Example(const Obj& o) : serpy::Serializer(o) {
            addField("foo", new serpy::StrField(&Obj::foo));
        }
    };

    Obj o;
    o.foo = "hello";
    Example ex(o);
    auto data = ex.data();
    ASSERT_EQ(data["foo"], "hello");
}

TEST_F(TestFields, IntField) {
    class Example : public serpy::Serializer {
    public:
        Example(const Obj& o) : serpy::Serializer(o) {
            addField("foo", new serpy::IntField(&Obj::foo));
        }
    };

    Obj o;
    o.foo = "23";
    Example ex(o);
    auto data = ex.data();
    ASSERT_EQ(data["foo"], 23);
}

TEST_F(TestFields, FloatField) {
    class Example : public serpy::Serializer {
    public:
        Example(const Obj& o) : serpy::Serializer(o) {
            addField("foo", new serpy::FloatField(&Obj::foo));
        }
    };

    Obj o;
    o.foo = "2";
    Example ex(o);
    auto data = ex.data();
    ASSERT_FLOAT_EQ(data["foo"], 2.0);
}

TEST_F(TestFields, BoolField) {
    class Example : public serpy::Serializer {
    public:
        Example(const Obj& o) : serpy::Serializer(o) {
            addField("foo", new serpy::BoolField(&Obj::foo));
        }
    };

    Obj o;
    o.foo = "1";
    Example ex(o);
    auto data = ex.data();
    ASSERT_EQ(data["foo"], true);
}

TEST_F(TestFields, MethodField) {
    class Example : public serpy::Serializer {
    public:
        Example(const Obj& o) : serpy::Serializer(o) {
            addField("foo", new serpy::MethodField(
                [this](const Obj& obj){ return obj.foo * 2; }
            ));
        }
    };

    Obj o;
    o.foo = "3";
    Example ex(o);
    auto data = ex.data();
    ASSERT_EQ(data["foo"], "33");
}