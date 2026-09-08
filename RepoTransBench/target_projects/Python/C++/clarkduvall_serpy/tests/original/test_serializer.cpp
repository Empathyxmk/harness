#include <gtest/gtest.h>
#include "serpy/serializer.h"
#include "serpy/fields.h"
#include "obj.h"
#include <string>

class TestSerializer : public ::testing::Test {};

TEST_F(TestSerializer, LabelField) {
    class Example : public serpy::Serializer {
    public:
        Example(const Obj& o) : serpy::Serializer(o) {
            addField("foo_out", new serpy::Field(&Obj::foo, "foo_out"));
        }
    };

    Obj o;
    o.foo = "thing";
    Example ex(o);
    auto data = ex.data();
    ASSERT_EQ(data["foo_out"], "thing");
}

TEST_F(TestSerializer, SerializerToValue) {
    class Example : public serpy::Serializer {
    public:
        Example(const Obj& o) : serpy::Serializer(o) {
            addField("one", new serpy::IntField(&Obj::one));
            addField("two", new serpy::IntField(&Obj::two));
        }
    };

    Obj o;
    o.one = 1;
    o.two = 2;
    Example ex(o);
    auto val = ex.to_value(o);
    ASSERT_EQ(val["one"], 1);
    ASSERT_EQ(val["two"], 2);
}

TEST_F(TestSerializer, MissingAttr) {
    class Example : public serpy::Serializer {
    public:
        Example(const Obj& o) : serpy::Serializer(o) {
            addField("foo", new serpy::Field(&Obj::bar));
        }
    };

    Obj o;
    o.bar = "baz";
    Example ex(o);
    auto data = ex.data();
    ASSERT_EQ(data["foo"], "baz");
}