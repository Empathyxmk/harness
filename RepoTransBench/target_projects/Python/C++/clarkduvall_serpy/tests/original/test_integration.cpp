#include <gtest/gtest.h>
#include "serpy/serializer.h"
#include "serpy/fields.h"
#include "obj.h"
#include <string>

class DummyObj {
public:
    int a;
    int b;
    int method_val;
    std::string c;
    DummyObj(int a_ = 1, int b_ = 2, std::string c_ = "", int method_val_ = 5)
        : a(a_), b(b_), c(c_), method_val(method_val_) {}
    int meth() const { return method_val; }
};

TEST(TestIntegrationSerpySerializer, SimpleSerialization) {
    class Ex : public serpy::Serializer {
    public:
        Ex(const DummyObj& o) : serpy::Serializer(o) {
            addField("a", new serpy::IntField(&DummyObj::a));
            addField("b", new serpy::IntField(&DummyObj::b));
        }
    };

    DummyObj o(4, 5, "", 5);
    Ex ex(o);
    auto data = ex.data();
    ASSERT_EQ(data["a"], 4);
    ASSERT_EQ(data["b"], 5);
}

TEST(TestIntegrationSerpySerializer, MethodAndCustomLabels) {
    class Ex : public serpy::Serializer {
    public:
        Ex(const DummyObj& o) : serpy::Serializer(o) {
            addField("maybe", new serpy::MethodField([this](const DummyObj& obj){ return obj.method_val; }));
        }
    };

    DummyObj o(1, 2, "", 42);
    Ex ex(o);
    auto data = ex.data();
    ASSERT_TRUE(data.find("maybe") != data.end());
    ASSERT_EQ(data["maybe"], 42);
}

TEST(TestIntegrationSerpySerializer, DictSerializer) {
    // Emulate DictSerializer by serializing a std::map
    class DSer : public serpy::Serializer {
    public:
        DSer(const std::map<std::string, int>& d) : serpy::Serializer(d) {
            addField("x", new serpy::IntField("x"));
            addField("y", new serpy::IntField("y"));
        }
    };

    std::map<std::string, int> d = { {"x", 10}, {"y", 21} };
    DSer ex(d);
    auto data = ex.data();
    ASSERT_EQ(data["x"], 10);
    ASSERT_EQ(data["y"], 21);
}

TEST(TestIntegrationSerpySerializer, EdgeCasesAndRepr) {
    class Example : public serpy::Serializer {
    public:
        Example(const Obj& o) : serpy::Serializer(o) {
            addField("foo", new serpy::Field(&Obj::foo));
        }
    };

    Obj o;
    o.foo = "edgecase";
    Example ex(o);
    std::string repr = ex.repr();
    ASSERT_NE(repr.find("Example"), std::string::npos);
}